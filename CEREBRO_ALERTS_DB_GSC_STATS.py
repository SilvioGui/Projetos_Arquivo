#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
    
# -------------------------- GOOGLE SEARCH CONSOLE DATA ALERTS --------------------------------
table_name, script_type = 'gsc_stats', 'alerts'
url_ids = get_url_ids('gsc','Google Search Console Statistics',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

colunas = ['crawled','kb_day','time_download']

#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection, 3rd section to trend analysis correlation factor
dict_colunas = { 
    #first subdivision
    'semantic':{'en':
                    {'crawled':'Pages Crawled Per Day',
                    'kb_day':'Kilobytes Downloaded Per Day',
                    'time_download':'Time Spent Downloading a Page'
                    },
                'pt':
                    {'crawled':'Páginas Rastreadas por Dia',
                    'kb_day':'Kilobytes Baixados por Dia',
                    'time_download':'Tempo Gasto Baixando uma Página'
                    }
                },
    #second subdivision
    'outlier':
            {'crawled':1.2,
            'kb_day':1.2,
            'time_download':1.2
            },
    #third subdivision
    'correlation':
            {'crawled':0.85,
            'kb_day':0.9,
            'time_download':0.9
            },
    #fourth subdivision
    'format':
            {'crawled':int,
            'kb_day':int,
            'time_download':int,
            },
    }

config_dict = yaml.load(email_to_send['gsc'])            
file_emailtext = ''

for url_id in url_ids:
    if config_dict[url_id]['stats'] == 0:
        logging.info('Statistics not checked for url_id %s' %url_id)
        continue

    url_dict = {}
    url_trends = []
    url_outliers = []
    url_prior_outliers = []
    url_prior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []
    own_condition = 1

    cursor.execute("select * from gsc_stats where url_id = '%s' order by date desc limit 0,10;" %url_id)
    results = cursor.fetchall()
    if len(results) == 0:
        continue
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    analysis = 'days'
    traffic_type = ''
    maxdate = 0

    logging.info("Analyzing %s" %siteurl)
    for coluna in colunas:
        var = []
        dates = []
        format_type = dict_colunas['format'][coluna]
        #joins each day data in a list to apply statistics
        for result in results:
            var[:0] = [format_type(result[coluna])]
            dates[:0] = [str(result['date'])]

        if len(var) >= 5:
            try:
                #uses trimmean to get expected value
                trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_colunas['outlier'][coluna], format_type)
                x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
                        
            except Exception as e:
                logging.info(e)
                continue
        else:
            logging.info("No data available for %s. Proceding to next url..." %(siteurl))
            break

        #gets last day value to compare deviation from expected value
        try:
            var1 = format_type(results[0][coluna])
            date1 = results[0]['date']
        except:
            logging.info("No data available for %s %s in %s. Proceding to next url..." %(siteurl, coluna, date1))
            continue

        # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
        cursor.execute("select gsc_stats from alerts_analysis_history where url_id = '%s';" %url_id)
        last_alert_date = cursor.fetchall()
        if last_alert_date != ():
            last_alert_date = last_alert_date[0]['gsc_stats']         #gets the last date from the alerts sent in past
            if last_alert_date != None:
                last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
                try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                    email_alert_id = last_alert_date[email_group_id].split('|')[0]
                    last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                    if last_analyzed_date == str(date1):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                        cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                        sent_date = cursor.fetchall()
                        if sent_date != ():
                            sent_date = sent_date[0]['sent_date']
                            logging.info("There is already an email alert sent to %s about Google Search Console Crawl Statistics data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                            break
                        else:
                            sent_date = sent_date[0]['sent_date']
                            logging.info("There is already an email alert sent to %s about Google Search Console Crawl Statistics data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                except:
                    pass

        # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
        # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
        cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
        last_emails_content = cursor.fetchall()

        #Checks if a variable is on a rising or falling trend. Accept criteria is:
        #R² > correlation coefficient
        #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
        if r_value > dict_colunas['correlation'][coluna] and p_value < 0.05:
            type_alert = [coluna, traffic_type, '', False]
            #classifying the trend found             
            if slope < 0:
                type_alert[2] = 'falling'
            else:
                type_alert[2] = 'rising'
            if r_value > 0.99:
                type_alert[3] = True
            logging.info("Trend found: %s" %type_alert)

            # -------------- EMAIL CONSTRUCTING BLOCK (TRENDS) --------------
            var_email = avoid_same_content(last_emails_content, type_alert)
            if var_email == True:                    
                if slope < 0:
                    trend_type += ' falling'
                    if coluna in ['time_download']:
                         color = 'green'
                    else:
                         color = 'red'
                else:
                    trend_type += ' rising'
                    if coluna in ['time_download']:
                         color = 'red'
                    else:
                         color = 'green'
                trend = trend_phrase(traffic_type, dict_colunas['semantic'][language][coluna], type_alert, color, trend_type, format_type, 'dimension_off')
                trend += '<br><img src="cid:Graph%s.png"><br>' %n

                alerts_summary[url_id].append(type_alert)
                url_trends.append(trend)
                url_prior_trends.append(r_value)
                trend_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, dates, vect_reg, r_value, color, analysis, n)
                n += 1


        # ------------------------------ RUNNING THE ANALYSIS ----------------------------------------
        #absdelta and percdelta are the anomaly detectors
        varabsdelta = var1 - trim_var
        try:
            varpercdelta = (var1/trim_var)-1
        except:
            varpercdelta = float("inf")
        #if the test score changes more than 5 points it is considered and anomaly
        if var1 < lowerlimit or var1 > upperlimit:
            type_alert = [coluna, traffic_type, '', False]
            #classifying the outlier found             
            if varpercdelta > 0:
                type_alert[2] = 'up'
            else:
                type_alert[2] = 'down'
            if var1 < crit_lowerlimit or var1 > crit_upperlimit and lowerlimit != upperlimit:
                type_alert[3] = True
            logging.info("Outlier found: %s" %type_alert)

            # -------------- EMAIL CONSTRUCTING BLOCK (OUTLIER) --------------
            var_email = avoid_same_content(last_emails_content, type_alert)
            if var_email == True:
                if varabsdelta < 0:
                    sign = '-'
                    if coluna in ['time_download']:
                         color = 'green'
                    else:
                         color = 'red'
                else:
                    sign = '+'
                    if coluna in ['time_download']:
                         color = 'red'
                    else:
                         color = 'green'

                outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, dates, trim_var, upperlimit, lowerlimit, analysis, n)
                text = outlier_phrase(dict_colunas['semantic'][language][coluna], type_alert, traffic_type, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, 'dimension_on', 'yes', outliers_over_time)
                text += '<br><img src="cid:Graph%s.png"><br>' %n
                
                alerts_summary[url_id].append(type_alert)
                url_outliers.append(text)
                url_prior_outliers.append(varpercdelta)
                n += 1

    if url_trends != [] or url_outliers != []:
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls

        # --------- EMAIL TOPICS SORTING BLOCK -----------
        #sorts changes from most negative to most positive
        sorted_trends = sort_email_from_list(url_prior_trends, url_trends,'color:red','color:blue','color:green')
        sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green')

        file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
        file_emailtext += "".join(sorted_email) + '<br>'
        file_emailtext += "".join(sorted_trends) + '<br>'

# ------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Google Search Console Statitics','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
