#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- GOOGLE SEARCH CONSOLE DATA ALERTS --------------------------------
table_name, script_type = 'gsc_kpis', 'alerts'
url_ids = get_url_ids('gsc','Google Search Console KPIS',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection,
#3rd section to trend analysis correlation factor, 4th section for variable types
dict_colunas = { 
    #first subdivision
    'semantic':{'en':{
                    'clicks':'Clicks',
                    'impressions':'Impressions',
                    'ctr':'CTR',
                    'position':'Position',
                    },
                'pt':{
                    'clicks':'Cliques',
                    'impressions':'Impressões',
                    'ctr':'CTR',
                    'position':'Posição',
                    },
                },
    #second subdivision
    'outlier':{
                'clicks':2.2,
                'impressions':2.2,
                'ctr':3,
                'position':2.2},
    #third subdivision
    'correlation':{
                'clicks':0.91,
                'impressions':0.91,
                'ctr':0.91,
                'position':0.91,},
    #fourth subdivision
    'format':{
                'clicks':int,
                'impressions':int,
                'ctr':float,
                'position':float,}
    }

dict_types = {'en':{'Overall':'Overall',
                    'Image':'Image',
                    'Non Branded':'Non Branded',
                    'Branded':'Branded',
                    },
              'pt':{'Overall':'Overall',
                    'Image':'Imagens',
                    'Non Branded':'Non Branded',
                    'Branded':'Branded',
                    }
              } 

config_dict = yaml.load(email_to_send['gsc'])    
file_emailtext = ''

for url_id in url_ids:
    if [] in config_dict[url_id]['kpis'][2]:
        logging.info('KPIs not checked for url_id %s' %url_id)
        continue

    traffic_types = config_dict[url_id]['kpis'][0]
    devices = config_dict[url_id]['kpis'][1]
    colunas = config_dict[url_id]['kpis'][2]
    ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit = 0, 0, 0, 0, 0

    cursor.execute("select weekday((select max(date) from gsc_kpis where url_id = %s));" %url_id)
    maxdate = cursor.fetchall()[0]['weekday((select max(date) from gsc_kpis where url_id = %s))' %url_id]
    url_break = False
    url_dict = {}
    url_trends = []
    url_outliers = []
    url_prior_outliers = []
    url_prior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []
    own_condition = 1

    #gets last 10 entries for the specified url, 9 for statistic analysis and 1 to be checked
    for traffic_type in traffic_types:
        if url_break == True:
            break
        for device in devices:
            if url_break == True:
                break
            cursor.execute("select * from gsc_kpis where (weekday(date),url_id,type,device)=(%s,%s,%s,%s) order by date desc limit 0,10;" , (maxdate,url_id,traffic_type,device))
            results = cursor.fetchall()
            if len(results) == 0:
                logging.error('{}: there are no rows in gsc_kpis table for url_id: {} device: {} and type: {}'.format(__file__, url_id, device, traffic_type))
                continue
            siteurl = results[0]['url']
            domain = get_domain_name(siteurl)
            analysis = 'weekdays'

            logging.info("Analyzing %s %s %s" %(siteurl, traffic_type, device))
            
            #get values for each metric analyzed
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
                    logging.info("No data available for %s %s. Proceding to next traffic type..." %(siteurl, traffic_type))
                    break

                #gets last day value
                try:
                    var1 = format_type(results[0][coluna])
                    date1 = results[0]['date']
                except:
                    logging.info("No dates available for %s. Proceding to next url..." %siteurl)
                    continue
            
                # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
                # It checks the last date analyzed which had an email sent because in case the extraction scripts crash, it is necessary not to send the same alert again
                cursor.execute("select gsc_kpis from alerts_analysis_history where url_id = '%s';" %url_id)
                last_alert_date = cursor.fetchall()
                if last_alert_date != ():
                    last_alert_date = last_alert_date[0]['gsc_kpis']         #gets the last date from the alerts sent in past
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
                                    logging.info("There is already an email alert sent to %s about Google Search Console KPIs data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                                    url_break = True
                                    break
                                else:
                                    logging.info("There is already an email alert sent to %s about Google Search Console KPIs data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                                    url_break = True
                                    break
                        except:
                            pass
            
                # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
                # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
                cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
                last_emails_content = cursor.fetchall()
                
                # ------------------------------- TRENDS ANALYSIS --------------------------------
                #Checks if a variable is on a rising or falling trend. Accept criteria is:
                #R² > correlation coefficient
                #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
                if r_value > dict_colunas['correlation'][coluna] and p_value < 0.05:
                    type_alert = [coluna, [traffic_type, device], '', False]
                    semantic_var, dimension_condition = get_semantic_dimention(type_alert)
                    #classifying the trend found             
                    if r_value > 0.99:
                        type_alert[3] = True
                    if slope < 0:
                        type_alert[2] = 'falling'
                    else:
                        type_alert[2] = 'rising'
                    logging.info("Trend found: %s" %type_alert)
                    
                    # -------------- EMAIL CONSTRUCTING BLOCK (TRENDS) --------------
                    var_email = avoid_same_content(last_emails_content, type_alert)
                    if var_email == True:                    
                        if slope < 0:
                            trend_type += ' falling'
                            if coluna == 'position':
                                 color = 'green'
                            else:
                                 color = 'red'
                        else:
                            trend_type += ' rising'
                            if coluna == 'position':
                                 color = 'red'
                            else:
                                 color = 'green'
                        trend = trend_phrase(semantic_var, dict_colunas['semantic'][language][coluna], type_alert, color, trend_type, format_type, 'dimension_on')
                        trend += '<br><img src="cid:Graph%s.png"><br>' %n

                        alerts_summary[url_id].append(type_alert)
                        url_trends.append(trend)
                        url_prior_trends.append(r_value)
                        trend_graph(maxdate, dict_colunas['semantic'][language][coluna], semantic_var, x, var, dates, vect_reg, r_value, color, analysis, n)
                        n += 1

                # ------------------------------ OUTLIERS ANALYSIS ----------------------------------------
                #absdelta and percdelta are the anomaly detectors
                varabsdelta = var1 - trim_var
                try:
                    varpercdelta = (var1/trim_var)-1
                except:
                    varpercdelta = float("inf")

                #checks the variable being analyzed to determine the conditions to send email
                if var1 < lowerlimit or var1 > upperlimit:
                    type_alert = [coluna, [device, traffic_type], '', False]
                    semantic_var, dimension_condition = get_semantic_dimention(type_alert)
                    #classifying the outlier found             
                    if var1 < crit_lowerlimit or var1 > crit_upperlimit and lowerlimit != upperlimit:
                        type_alert[3] = True
                    if varpercdelta > 0:
                        type_alert[2] = 'up'
                    else:
                        type_alert[2] = 'down'
                    logging.info("Outlier found: %s" %type_alert)

                    # -------------- EMAIL CONSTRUCTING BLOCK (OUTLIER) --------------
                    var_email = avoid_same_content(last_emails_content, type_alert)
                    if var_email == True:
                        if varabsdelta < 0:
                            sign = '-'
                            if coluna == 'position':
                                color = 'green'
                            else:
                                color = 'red'
                        else:
                            sign = '+'
                            if coluna == 'position':
                                color = 'red'
                            else:
                                color = 'green'

                        outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], semantic_var, x, var, dates, trim_var, upperlimit, lowerlimit, analysis, n)
                        if varpercdelta != float("inf"):
                            text = outlier_phrase(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, dimension_condition, 'yes', outliers_over_time)
                            text += '<br><img src="cid:Graph%s.png"><br>' %n
                            n += 1
                        #if every item in list is equal to zero, or the 25 and 75 percentile are zero, it will create a non critical alert, otherwise skips it
                        else:
                            type_alert = [coluna, [device, traffic_type], type_alert[2], False]
                            if any(item != 0 for item in var[:-1]) == False:
                                text = outlier_phrase_zero(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, sign, format_type, dimension_condition, 'yes', 'zero')
                                text += '<br><img src="cid:Graph%s.png"><br>' %n
                                n += 1
                            else:
                                if [ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit] == [0, 0, 0, 0, 0]:
                                    cursor.execute("select * from gsc_kpis where (weekday(date),url_id,type,device)=(%s,%s,'Overall','All Devices') order by date desc limit 0,10;" , (maxdate,url_id))
                                    reference_results = cursor.fetchall()
                                    reference_var = []
                                    for reference_result in reference_results:
                                        reference_var[:0] = [format_type(reference_result[coluna])]

                                    if len(var) >= 5:
                                        ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit = get_stats_values(reference_var, dict_colunas['outlier'][coluna], format_type)
                                    else:
                                        continue

                                #checks if outlier appears in a significant variable (at least 2% of the normal or expected value not zero) otherwise it is ignored
                                if ref_trim_var == 0:
                                    logging.info("The outlier won\'t be mentioned in alert because the traffic type mentioned is usually negligible")
                                    continue
                                if var1/ref_trim_var < 0.02:
                                    logging.info("The outlier won\'t be mentioned in alert because the traffic type mentioned is usually negligible")
                                    continue
                                else:
                                    text = outlier_phrase_zero(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, sign, format_type, dimension_condition, 'yes', 'close_to_zero')
                                    text += '<br><img src="cid:Graph%s.png"><br>' %n
                                    n += 1

                        alerts_summary[url_id].append(type_alert)
                        url_outliers.append(text)
                        if coluna == 'position':
                            url_prior_outliers.append(-varpercdelta)
                        else:
                            url_prior_outliers.append(varpercdelta)

    # --------------------------------- EMAIL ALERTS HISTORY DATABASE MANIPULATION -----------------------------
    #if it makes sense to send url information to email, the email alert record is stored. The commit is only made inside the email script, which avoids errors
    if url_trends != [] or url_outliers != []:
        auxiliar_alerts_summary = {'outlier':{},'trends':{}}
        url_outliers, url_prior_outliers = consolidate_devices_alerts(url_outliers, url_prior_outliers, 'outlier')
        url_trends, url_prior_trends = consolidate_devices_alerts(url_trends, url_prior_trends, 'trends')
        
        if url_id in auxiliar_alerts_summary['trends'] and url_id in auxiliar_alerts_summary['outlier']:
            alerts_summary[url_id] = auxiliar_alerts_summary['trends'][url_id] + auxiliar_alerts_summary['outlier'][url_id]
        elif url_id in auxiliar_alerts_summary['trends'] and url_id not in auxiliar_alerts_summary['outlier']:
            alerts_summary[url_id] = auxiliar_alerts_summary['trends'][url_id]
        elif url_id not in auxiliar_alerts_summary['trends'] and url_id in auxiliar_alerts_summary['outlier']:
            alerts_summary[url_id] = auxiliar_alerts_summary['outlier'][url_id]

        if url_trends != [] or url_outliers != []:
            auxiliar_alerts_summary = {'outlier':{},'trends':{}}
            url_outliers, url_prior_outliers, outlier_additional_text = drop_similar_dim_alerts(url_outliers, url_prior_outliers, 'outlier', 'traffic types', 4, traffic_types, list)
            url_trends, url_prior_trends, trends_additional_text = drop_similar_dim_alerts(url_trends, url_prior_trends, 'trends', 'traffic types', 4, traffic_types, list)

            if url_id in auxiliar_alerts_summary['trends'] and url_id in auxiliar_alerts_summary['outlier']:
                alerts_summary[url_id] = auxiliar_alerts_summary['trends'][url_id] + auxiliar_alerts_summary['outlier'][url_id]
            elif url_id in auxiliar_alerts_summary['trends'] and url_id not in auxiliar_alerts_summary['outlier']:
                alerts_summary[url_id] = auxiliar_alerts_summary['trends'][url_id]
            elif url_id not in auxiliar_alerts_summary['trends'] and url_id in auxiliar_alerts_summary['outlier']:
                alerts_summary[url_id] = auxiliar_alerts_summary['outlier'][url_id]            

            if url_trends != [] or url_outliers != [] or outlier_additional_text != [] or trends_additional_text != []:
                metric_comments = {'outlier':[],'trends':[]}
                kpi_connections(alerts_summary[url_id])

                dict_urls[url_id] = str(date1)
                analyzed_urls[execute_file[2]] = dict_urls 

                # --------- EMAIL TOPICS SORTING BLOCK -----------
                file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
                sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green')

                file_emailtext += "".join(sorted_email)
                if outlier_additional_text != []:
                    file_emailtext += "".join(outlier_additional_text)
                if metric_comments['outlier'] != []:
                    file_emailtext += "<br>".join(metric_comments['outlier'])

                sorted_trends = sort_email_from_list(url_prior_trends, url_trends,'color:red','color:blue','color:green')
                file_emailtext += "".join(sorted_trends)
                if outlier_additional_text != []:
                    file_emailtext += "".join(trends_additional_text)
                if metric_comments['trends'] != []:
                    file_emailtext += "<br>".join(metric_comments['trends'])


# ------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Google Search Console','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")

