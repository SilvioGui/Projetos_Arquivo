#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
    
# -------------------------- GOOGLE ANALYTICS DATA ALERTS --------------------------------
table_name, script_type = 'ga_campaigns', 'alerts'
url_ids = get_url_ids('gads','Google Adwords Campaigns',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#set columns which should be analyzing comparing the last 10 days (in general, rates and percentual values)
lastdays = ['bounceRate', 'avgSessionDuration','avgTimeOnPage']
#set columns which should be analyzing comparing the last 10 similar weekdays (in general, absolute values metrics)
lastweeks = ['bounceRate', 'avgSessionDuration','avgTimeOnPage','sessions','users','pageviews', 'newUsers', 'transactionRevenue','transactions','conversion','roi','cpc','adCost','adClicks','impressions']

#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection,
#3rd section to trend analysis correlation factor, 4th section for variable types
dict_colunas = { 
    #first subdivision
    'semantic':{
            'en':{
                'sessions':'Sessions',
                'pageviews':'Pageviews',
                'bounceRate':'Bounce Rate',
                'avgSessionDuration':'Average Session Duration',
                'cpc':'Cost per Click',
                'adCost':'Cost',
                'adClicks':'Ad Cost',
                'impressions':'Impressions',
                'transactionRevenue':'Revenue',
                'transactions':'Transactions',
                'conversion':'Conversion',
                'roi':'ROI',
                },
            'pt':{
                'sessions':'Sessões',
                'pageviews':'Pageviews',
                'bounceRate':'Bounce Rate',
                'avgSessionDuration':'Duração Média da Sessão',
                'cpc':'Custo por Clique',
                'adCost':'Custo',
                'adClicks':'Custo de Anúncio',
                'impressions':'Impressões',
                'transactionRevenue':'Receita',
                'transactions':'Pedidos',
                'conversion':'Conversão',
                'roi':'ROI',
                },
            },
    #second subdivision
    'outlier':{
                'sessions':2,
                'pageviews':2,
                'bounceRate':2,
                'avgSessionDuration':2,
                'cpc':2,
                'adCost':2,
                'adClicks':2,
                'impressions':2,
                'transactionRevenue':2,
                'transactions':2,
                'conversion':2,
                'roi':2,
                },              
    #third subdivision
    'correlation':{
                'sessions':0.9,
                'pageviews':0.9,
                'bounceRate':0.9,
                'avgSessionDuration':0.9,
                'cpc':0.9,
                'adCost':0.9,
                'adClicks':0.9,
                'impressions':0.9,
                'transactionRevenue':0.9,
                'transactions':0.9,
                'conversion':0.9,
                'roi':0.9,
                },
    #fourth subdivision
    'format':{
                'sessions':int,
                'pageviews':int,
                'bounceRate':float,
                'avgSessionDuration':int,
                'cpc':float,
                'adCost':float,
                'adClicks':int,
                'impressions':int,
                'transactionRevenue':float,
                'transactions':int,
                'conversion':float,
                'roi':float,
                },
    'limits':{
                #'sessions':0.9,
                #'pageviews':0.9,
                'bounceRate':80,
                #'avgSessionDuration':0.9,
                'cpc':1,
                #'adCost':0.9,
                #'adClicks':0.9,
                #'impressions':0.9,
                #'transactionRevenue':0.9,
                #'transactions':0.9,
                'conversion':-0.05,
                'roi':-0.1,
                },
    }

config_dict = yaml.load(email_to_send['gads'])
file_emailtext = ''

for url_id in url_ids:
    if config_dict[url_id]['metrics'] == []:
        logging.info('campaigns not checked for url_id %s' %url_id)
        continue

    if 'roi' in config_dict[url_id]:
        logging.info('Setting custom ROI limit for url_id %s: %s' %(url_id, config_dict[url_id]['roi']))

    #get all the columns to be analyzed for the corresponding url
    colunas = config_dict[url_id]['metrics']

    cursor.execute("select weekday(max(date)) from ga_campaigns where url_id = %s;" %url_id)
    maxdate = cursor.fetchall()[0]['weekday(max(date))']

    traffic_types = []
    cursor.execute("select distinct(campaign) from ga_campaigns where url_id = %s and date >= date(curdate()-1);" %url_id)
    results = cursor.fetchall()
    if len(results) == 0:
        logging.info('{}: there are no rows in ga_campaigns table for url_id = {}'.format(__file__, url_id))
        continue

    for result in results:
        traffic_types.append(result['campaign'])

    url_break = False
    url_dict = {}
    url_trends = []
    url_outliers = []
    url_prior_outliers = []
    url_prior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []
    
    cursor.execute("select url from ga_campaigns where url_id = %s order by date desc limit 1;" , [url_id])
    results = cursor.fetchall()
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    logging.info("Analyzing %s" %siteurl)
    own_condition = 1

    for traffic_type in traffic_types:
        if url_break == True:
            break
        #get values for each metric analyzed
        for coluna in colunas:
            if coluna in lastweeks:
                #gets last 10 weekday entries for the specified site, 9 for statistic analysis and 1 to be checked
                cursor.execute("select * from ga_campaigns where (weekday(date),url_id,campaign)=(%s,%s,%s) order by date desc limit 0,10;" , (maxdate,url_id,traffic_type))
                analysis = 'weekdays'
            elif coluna in lastdays:
                #gets last 10 day entries for the specified site, 9 for statistic analysis and 1 to be checked
                cursor.execute("select * from ga_campaigns where (url_id,campaign)=(%s,%s) order by date desc limit 0,11;" , (url_id,traffic_type))
                analysis = 'days'
            else:
                logging.info("Variable %s analysis period not defined" %coluna)
                continue
            results = cursor.fetchall()
            var = []
            dates = []
            format_type = dict_colunas['format'][coluna]
            #joins each day data in a list to apply statistics
            for result in results:
                var[:0] = [format_type(result[coluna])]
                dates[:0] = [str(result['date'])]

            if len(var) >= 5:
                #uses trimmean to get expected value
                trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_colunas['outlier'][coluna], format_type)
                x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
            else:
                logging.info("No data available for %s %s. Proceding to next campaign..." %(siteurl, traffic_type))
                break

            #gets last day value to compare deviation from expected value
            try:
                var1 = format_type(results[0][coluna])
                date1 = results[0]['date']
            except:
                logging.info("No data available for %s %s. Proceding to next campaign..." %(siteurl, traffic_type))
                continue

            # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
            # It checks the last date analyzed which had an email sent because in case the extraction scripts crash, it is necessary not to send the same alert again
            url_break = False
            cursor.execute("select ga_campaigns from alerts_analysis_history where url_id = '%s';" %url_id)
            last_alert_date = cursor.fetchall()
            if last_alert_date != ():
                last_alert_date = last_alert_date[0]['ga_campaigns']         #gets the last date from the alerts sent in past
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
                                logging.info("There is already an email alert sent to %s about Google Analytics Campaigns data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                                url_break = True
                                break
                            else:
                                logging.info("There is already an email alert sent to %s about Google Analytics Campaigns data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                                url_break = True
                                break
                    except:
                        pass

            # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
            # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
            #cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
            #last_emails_content = cursor.fetchall()
            last_emails_content = ()

            # ------------------------------- OUTLIERS ANALYSIS --------------------------------
            #absdelta and percdelta are the anomaly detectors
            varabsdelta = var1 - trim_var
            try:
                varpercdelta = (var1/trim_var)-1
            except:
                varpercdelta = float("inf")

            trigger = None
            #checks the variable being analyzed to determine the conditions to send email
            if (var1 < lowerlimit or var1 > upperlimit) and abs(varpercdelta) > 0.05:
                trigger = 'outlier-by-sample'
            if coluna in dict_colunas['limits'] and trigger != 'outlier-by-sample':
                if 'roi' in config_dict[url_id] and coluna == 'roi':
                    limit_value = config_dict[url_id]['roi']
                else:
                    limit_value = dict_colunas['limits'][coluna]
                if limit_value > 0 and var1 > limit_value:
                    trigger = 'high-value'
                if limit_value < 0 and var1 < abs(limit_value):
                    trigger = 'low-value'
                    limit_value = abs(limit_value)
            if trigger != None:
                type_alert = [coluna, traffic_type, '', False]
                semantic_var, dimension_condition = get_semantic_dimention(type_alert)
                semantic_var = '[' + semantic_var + ']'
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
                    if trigger == 'outlier-by-sample':
                        if varabsdelta < 0:
                            sign = '-'
                            if coluna in ['bounces', 'bounceRate','cpc']:
                                color = 'green'
                            elif coluna in ['adCost', 'impressions', 'avgSessionDuration']:
                                color = 'blue'
                            else:
                                color = 'red'
                        else:
                            sign = '+'                   
                            if coluna in ['bounces', 'bounceRate','cpc']:
                                color = 'red'
                            elif coluna in ['adCost', 'impressions', 'avgSessionDuration']:
                                color = 'blue'
                            else:
                                color = 'green'
                    elif trigger == 'high-value':
                        sign = '+'
                        color = 'red'
                    elif trigger == 'low-value':
                        sign = '-'
                        color = 'red'
                        
                    if trigger == 'outlier-by-sample':
                        outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], semantic_var, x, var, dates, trim_var, upperlimit, lowerlimit, analysis, n)
                    else:
                        outliers_over_time = extreme_value_graph(maxdate, dict_colunas['semantic'][language][coluna], semantic_var, x, var, dates, limit_value, trigger, analysis, n)
                    if varpercdelta != float("inf"):
                        text = outlier_phrase_campaign(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, trigger, 'yes', outliers_over_time)
                        text += '<br><img src="cid:Graph%s.png"><br>' %n
                        n += 1
                    #if every item in list is equal to zero, or the 25 and 75 percentile are zero, it will create a non critical alert, otherwise skips it
                    else:
                        type_alert = [coluna, traffic_type, type_alert[2], False]
                        if any(item != 0 for item in var[:-1]) == False:
                            text = outlier_phrase_zero(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, sign, format_type, dimension_condition, 'yes', 'zero')
                            text += '<br><img src="cid:Graph%s.png"><br>' %n
                            n += 1
                        else:
                            cursor.execute("select * from ga_channels where (weekday(date),url_id,channel,device)=(%s,%s,'Overall','All Devices') order by date desc limit 0,10;" , (maxdate,url_id))
                            reference_results = cursor.fetchall()
                            reference_var = []
                            for reference_result in reference_results:
                                reference_var[:0] = [format_type(reference_result[coluna])]

                            if len(var) >= 5:
                                ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit = get_stats_values(reference_var, dict_colunas['outlier'][coluna], format_type)
                            else:
                                continue

                            #check if outlier appears in a significant variable (at least 2% of the normal) otherwise it is ignored
                            if var1/ref_trim_var < 0.02:
                                logging.info("The outlier won\'t be mentioned in alert because the traffic type mentioned is usually negligible")
                                continue
                            else:
                                text = outlier_phrase_zero(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, sign, format_type, dimension_condition, 'yes', 'close_to_zero')
                                text += '<br><img src="cid:Graph%s.png"><br>' %n
                                n += 1

                    alerts_summary[url_id].append(type_alert)
                    url_outliers.append(text)
                    if coluna in ['bounces', 'bounceRate','cpc']:
                        url_prior_outliers.append(-varpercdelta)
                    else:
                        url_prior_outliers.append(varpercdelta)                    

    # --------------------------------- EMAIL ALERTS HISTORY DATABASE MANIPULATION -----------------------------
    #if it makes sense to send url information to email, the email alert record is stored. The commit is only made inside the email script, which avoids errors
    if url_trends != [] or url_outliers != []:
        #sorts changes from most negative to most positive
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls

        # --------- EMAIL TOPICS SORTING BLOCK -----------
        file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
        sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green')

        file_emailtext += "".join(sorted_email)

                
# ------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Google Adwords Campaigns','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
