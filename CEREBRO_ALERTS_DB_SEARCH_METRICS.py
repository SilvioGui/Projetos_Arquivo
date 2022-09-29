#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
        
# -------------------------- SEARCH METRICS DATA --------------------------------
table_name, script_type = 'search_metrics', 'alerts'
url_ids = get_url_ids('search_metrics','Search Metrics',str)
url_ids = list(set(url_ids) & set(allowed_url_ids))

colunas = ['desktop_visibility', 'mobile_visibility', 'paid_visibility', 'image_visibility', \
           'long_tail', 'traffic_value', 'sum_organic_keywords', 'organic_ranking']

#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection,
#3rd section to trend analysis correlation factor, 4th section for variable types
dict_colunas = { 
    #first subdivision
    'semantic':{'en':{
                        'desktop_visibility':'Desktop Visibility',
                        'mobile_visibility':'Mobile Visibility',
                        'paid_visibility':'Paid Visibility',
                        'image_visibility':'Image Visibility',
                        'long_tail':'Long Tail Image Keywords',
                        'traffic_value':'Traffic Value',
                        'sum_organic_keywords':'Sum of Organic Keywords',
                        'organic_ranking':'Organic Ranking',
                     },
                'pt':{
                        'desktop_visibility':'Visibilidade Desktop',
                        'mobile_visibility':'Visibilidade Mobile',
                        'paid_visibility':'Visibilidade Paga',
                        'image_visibility':'Visibilidade de Imagens',
                        'long_tail':'Keywords de Cauda Longa em Imagens',
                        'traffic_value':'Valor do Tráfego',
                        'sum_organic_keywords':'Soma de Keywords Orgânicas',
                        'organic_ranking':'Ranking Orgânico',
                    },
                },
    #second subdivision
    'outlier':{
                'desktop_visibility':1.25,
                'mobile_visibility':1.25,
                'paid_visibility':1.5,
                'image_visibility':1.25,
                'long_tail':1.5,
                'traffic_value':1.5,
                'sum_organic_keywords':1.5
                },
    #third subdivision
    'correlation':{
                'desktop_visibility':0.9,
                'mobile_visibility':0.9,
                'paid_visibility':0.9,
                'image_visibility':0.9,
                'long_tail':0.925,
                'traffic_value':0.925,
                'sum_organic_keywords':0.925,
                },
    #fourth subdivision
    'format':{
                'desktop_visibility':int,
                'mobile_visibility':int,
                'paid_visibility':int,
                'image_visibility':int,
                'long_tail':int,
                'traffic_value':int,
                'sum_organic_keywords':int,
             }
        }
    
#dictionary containing necessary values for every keyword.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection, 3rd section to trend analysis correlation factor
dict_keywords = { 
    #first subdivision
    'semantic':{'en':{
                    'position':'Position',
                     'page':'Page',
                     'url':'Url',
                     'trafficIndex':'Traffic Index',
                     'cpc':'CPC',
                     'searchVolume':'Search Volume'
                    },
                'pt':{
                    'position':'Posição',
                     'page':'Página',
                     'url':'Url',
                     'trafficIndex':'Tráfego Direcionado',
                     'cpc':'CPC',
                     'searchVolume':'Volume de Buscas',
                    },
                },
    #second subdivision
    'outlier':{
                'position':2,
                 'page':2,
                 'url':2,
                 'trafficIndex':1.5,
                 'cpc':2,
                 'searchVolume':1.5,
                },
    #third subdivision
    'correlation':{
                'position':0.9,
                 'page':0.9,
                 'url':0.9,
                 'trafficIndex':0.9,
                 'cpc':0.9,
                 'searchVolume':0.9,
                },
    #fourth subdivision
    'format':{
                'position':int,
                 'page':int,
                 'url':str,
                 'trafficIndex':int,
                 'cpc':float,
                 'searchVolume':int,
                },
    }

dict_texts = {'en':
                  {'text1':'<br><b>%s</b> has changed from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. The expected value was <b>%s</b>',
                   'text2':'<br>Landing page for keyword "%s" has changed from %s <i>(%s)</i> to %s <i>(%s)</i>',
                   'text3':'<br>The keywords <span style="color:red;"><i>%s</i></span> are not present in the Top 10 Organic Keywords anylonger. They were replaced by <span style="color:green;"><i>%s</i></span>.<br>',
                   'text4':'<br><br><b><span style="font-size:15px;">Top 10 Organic Keywords Analysis</b><span>',                  
                   },
              'pt':
                  {'text1':'<br><b>%s</b> mudou de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. O valor esperado era <b>%s</b>',
                   'text2':'<br>A Landing page da keyword "%s" mudou de %s <i>(%s)</i> para %s <i>(%s)</i>',
                   'text3':'<br>As keywords <span style="color:red;"><i>%s</i></span> não estão mais presentes entre as Top 10 Keywords Orgânicas. Elas foram substituídas por <span style="color:green;"><i>%s</i></span>.<br>',
                   'text4':'<br><br><b><span style="font-size:15px;">Análise das Top 10 Keywords Orgânicas</b><span>',                  
                  },
            }

prior_changes = []
file_emailtext = ''

for url_id in url_ids:
    url_email = False
    url_dict = {}
    url_trends = []
    url_outliers = []
    url_prior_outliers = []
    url_prior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    keywordstext_email = ''
    #gets last 10 weekday entries for the specified url
    cursor.execute("select weekday((select max(period_end) from search_metrics where url_id = %s));" %url_id)
    maxdate = cursor.fetchall()[0]['weekday((select max(period_end) from search_metrics where url_id = %s))' %url_id]

    cursor.execute("select * from search_metrics where (weekday(period_end),url_id) = ('%s','%s') order by period_end desc limit 0,10;" %(maxdate, url_id))
    results = cursor.fetchall()
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    analysis = 'weekdays'
    traffic_type = ''
    try:
        day0 = results[1]
        day1 = results[0]
        date0 = day0['period_end']
        date1 = day1['period_end']
    except:
        logging.info("No dates to compare for %s. Proceding to next url..." %siteurl)
        continue

    logging.info("Analyzing %s" %siteurl)
    cursor.execute("select own_url from monitoring_links where id = %s and owner_id = %s;" , [url_id, owner_id])
    own_condition = cursor.fetchall()[0]['own_url']

    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select search_metrics from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['search_metrics']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about Search Metrics data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                    else:
                        logging.info("There is already an email alert sent to %s about Search Metrics data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
            except:
                pass

    # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
    # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
    cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
    last_emails_content = cursor.fetchall()

    for coluna in colunas:
        # ------------------------------------------------ KEYWORDS ANALYSIS BLOCK --------------------------------------------------
        if coluna in ['organic_ranking']:
            logging.info("Running Top 10 Organic Keywords analysis")
            keywords_db = json.loads(results[0]['organic_ranking'])
            old_keywords_db = json.loads(results[1]['organic_ranking'])
            # turns the dict returned into a string ordering the keywords by 'trafficIndex'
            keywords_db = sorted(keywords_db.items(), key=lambda v: int(v[1]['trafficIndex']), reverse=True)
            old_keywords_db = sorted(old_keywords_db.items(), key=lambda v: int(v[1]['trafficIndex']), reverse=True)

            #gets the top 10 keywords from the top 100 in the database. Only top 10 is analyzed            
            pre_analyze_keywords = keywords_db[:10]
            analyze_keywords = []
            for keyword in pre_analyze_keywords:
                analyze_keywords.append(keyword[0])

            #gets the top 10 keywords from the top 100 in the database. Only top 10 is analyzed            
            old_pre_analyze_keywords = old_keywords_db[:10]
            old_analyze_keywords = []
            for old_keyword in old_pre_analyze_keywords:
                old_analyze_keywords.append(old_keyword[0])

            dict_analysis = {}
            period_ends = []

            # splits variables in different type so they can be analyzed in different ways
            var_types = ['position','page','url','trafficIndex','cpc','searchVolume']
            var_continuous = ['position','page','trafficIndex','cpc','searchVolume']
            var_discrete = ['url']

            # Rearranges stored data grouping keyword metrics and time in which they occur
            for result in results:
                dict_results = {}
                period_end = result['period_end']
                period_ends[:0] = [period_end]
                json_result = json.loads(result['organic_ranking'])
                for keyword in analyze_keywords:
                    keyword_dict = {}
                    if keyword in json_result.keys():
                        for var in var_types:
                            keyword_dict[var] = json_result[keyword][var]
                    else:
                        for var in var_types:
                            keyword_dict[var] = 'Not present in top 100 keywords'
                    dict_results[keyword] = keyword_dict
                dict_analysis[period_end] = dict_results

            for keyword in analyze_keywords:
                table_html = ''
                table_header = ''                
                table_rows = ''
                keywordstext = ''
                for var_type in var_types:
                    format_type = dict_keywords['format'][var_type]
                    kw_period_ends = period_ends
                    var = []
                    for period_end in kw_period_ends:
                        var.append(dict_analysis[period_end][keyword][var_type])
                    while 'Not present in top 100 keywords' in var:
                        exclude_itens = var.index('Not present in top 100 keywords')
                        var.pop(exclude_itens)
                        kw_period_ends.pop(exclude_itens)
                        
                    if len(var) <= 4:
                        logging.info('There is no suficient history to analyze the keyword: "%s". Proceding to the next keyword...' %keyword)
                        break

                    newer_var = format_type(var[len(var)-1])
                    old_var = format_type(var[len(var)-2])
                    newer_period_end = kw_period_ends[len(kw_period_ends)-1]
                    old_period_end = kw_period_ends[len(kw_period_ends)-2]
                    # KEYWORD CONTINUOUS VARIABLE ANALYSIS   
                    if var_type in var_continuous:
                        old_var = format_type(old_var)
                        newer_var = format_type(newer_var)
                        #print(keyword, var_type)
                        if len(var) >= 4:
                            #uses trimmean to get expected value
                            npvar = numpy.array(var)
                            var = npvar.astype(numpy.float)
                            trim_var = format_type(round(stats.trim_mean(var, 0.25),2))
                            #uses interquartile range to estimate if values are outliers or not
                            q75 = numpy.percentile(var, 75)
                            q25 = numpy.percentile(var, 25)
                            iqr = q75 - q25
                            upperlimit = q75 + dict_keywords['outlier'][var_type]*iqr
                            lowerlimit = q25 - dict_keywords['outlier'][var_type]*iqr
                            x = numpy.arange(len(var))
                            #calculate linear regression of the values comparing to a x vector of unitary incremented values (only if there are at least 5 values)
                            slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, var)
                            slope = round(slope, 3)

                            # KEYWORD TRENDS
                            if r_value**2 > dict_keywords['correlation'][var_type]:
                                type_alert = ["keyword %s" %keyword, var_type, '', False]
                                if slope > 0:
                                    type_alert[2] = 'rising'
                                else:
                                    type_alert[2] = 'falling'
                                logging.info("Trend found: %s" %type_alert)
                                    
                                var_email = avoid_same_content(last_emails_content, type_alert)
                                if var_email == True:
                                    if keywordstext == '':
                                        keywordstext = '<span style="color:blue"><br><b>%s</b></span>' %keyword
                                    if slope < 0:
                                        if var_type in ['position','page','cpc']:
                                            trend = 'falling'
                                            if own_condition == 1:
                                                color = 'green'
                                            else:
                                                color = 'red'
                                        else:
                                            trend = 'growing'
                                            if own_condition == 1:
                                                color = 'red'
                                            else:
                                                color = 'green'
                                    else:
                                        if var_type in ['position','page','cpc']:
                                            trend = 'growing'
                                            if own_condition == 1:
                                                color = 'red'
                                            else:
                                                color = 'green'
                                        else:
                                            trend = 'falling'
                                            if own_condition == 1:
                                                color = 'green'
                                            else:
                                                color = 'red'
                                    # table construction
                                    # header
                                    if table_header == '':
                                        table_header += '<tr><th style="table-layout: fixed;color:white;background-color: black;text-align:center;border: 1px solid black;">Metric\Date</th>'
                                        for period_end in kw_period_ends:
                                            table_header += '<th style="table-layout: fixed;color:white;background-color: black;text-align:center;border: 1px solid black;">'+str(period_end)+'</th>'
                                        table_header += '<th style="table-layout: fixed;color:white;background-color: black;text-align:center;border: 1px solid black;">Trend</th></tr>'
                                    # body
                                    table_rows += '<tr><td style="table-layout: fixed;text-align:center;border: 1px solid black;">'+dict_keywords['semantic'][language][var_type]+'</td>'
                                    for var_value in var:
                                        table_rows += '<td style="table-layout: fixed;text-align:center;border: 1px solid black;">'+str(format_type(var_value))+'</td>'
                                    table_rows += '<td style="table-layout: fixed;text-align:center;border: 1px solid black;color:%s"> %s </td></tr>' %(color, slope)
                                    alerts_summary[url_id].append(type_alert)
                                                                                       
                            if table_header != '' and var_type == var_continuous[len(var_continuous)-1]:
                                table_html += '<table style="table-layout: fixed; border: 1px solid black;border-collapse:collapse;width:100%;font-size:10px;">'+table_header+table_rows+'</table>'

                            # KEYWORD OUTLIER ANALYSIS
                            try:
                                var_change = newer_var/trim_var - 1
                            except:
                                var_change = float("inf")
                            if (newer_var > upperlimit or newer_var < lowerlimit) and abs(var_change) > 0.03:
                                type_alert = ["keyword %s" %keyword, var_type, '', False]
                                if var_change > 0:
                                    type_alert[2] = ' up'
                                else:
                                    type_alert[2] = ' down'

                                var_email = avoid_same_content(last_emails_content, type_alert)                               
                                if var_email == True:
                                    if var_change > 0:
                                        if var_type in ['position','page','cpc']:
                                            sign = '+'
                                            color = "red"
                                        else:
                                            sign = '+'
                                            color = "green"
                                    else:
                                        if var_type in ['position','page','cpc']:
                                            sign = '-'
                                            color = "green"
                                        else:
                                            sign = '-'
                                            color = "red"                                        
                                    if keywordstext == '':
                                        keywordstext = '<span style="color:blue"><br><b>%s</b></span>' %keyword
                                    keywordstext += outlier_phrase(dict_keywords['semantic'][language][var_type], type_alert, traffic_type, newer_var, newer_period_end, color, abs(var_change), trim_var, sign, format_type, 'dimension_off', 'no', [0, 1])
                                    alerts_summary[url_id].append(type_alert)
                        else:
                            logging.info('There is no suficient history to analyze trends for the keyword: "%s"' %keyword)
                            break

                    # KEYWORD DISCRETE VARIABLE ANALYSIS   
                    else:
                        if newer_var != old_var:
                            type_alert = ["keyword %s" %keyword, var_type, '', False]
                            var_email = avoid_same_content(last_emails_content, type_alert)
                            if var_email == True:
                                if keywordstext == '':
                                    keywordstext = '<span style="color:blue"><br><b>%s</b></span>' %keyword
                                keywordstext += dict_texts[language]['text2']  %(keyword, old_var, old_period_end, newer_var, newer_period_end)
                                alerts_summary[url_id].append(type_alert)
                if table_html != '':
                    keywordstext_email += keywordstext + '<br>' + table_html
                else:
                    keywordstext_email += keywordstext

            if set(analyze_keywords) != set(old_analyze_keywords):
                type_alert = ['organic ranking','','',False]
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    dif_in = list(set(analyze_keywords) - set(old_analyze_keywords))
                    dif_out = list(set(old_analyze_keywords) - set(analyze_keywords))                
                    dif_html = dict_texts[language]['text3'] %(", ".join(dif_out), ", ".join(dif_in))
                    keywordstext_email = dif_html + keywordstext_email

                    if "Top Organic Keywords" not in keywordstext_email and keywordstext_email != '':
                        keywordstext_email = dict_texts[language]['text4'] + keywordstext_email
                        alerts_summary[url_id].append(type_alert)
                        logging.info("Change found: top organic ranking")
                 

        # ------------------------------------------------------- NON KEYWORDS ANALYSIS BLOCK -----------------------------------------------------------------------
        else:   #the following block checks only number distortion, not the keywords
            var = []
            period_ends = []
            format_type = dict_colunas['format'][coluna]
            for result in results:
                var[:0] = [format_type(result[coluna])]
                period_ends[:0] = [str(result['period_end'])]

            if len(var) >= 5:
                try:
                    #uses trimmean to get expected value
                    trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_colunas['outlier'][coluna], format_type)
                    x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
                        
                except Exception as e:
                    logging.info(e)
                    continue
            else:
                logging.info("No data available for %s %s. Proceding to next metric..." %(siteurl, coluna))
                continue

            # ------------------------------ OUTLIERS ANALYSIS ----------------------------------------
            var0 = day0[coluna]
            var1 = format_type(day1[coluna])
            if var1 < 1:
                continue

            #absdelta and percdelta are the anomaly detectors
            varabsdelta = var1 - trim_var
            try:
                varpercdelta = (var1/trim_var)-1
            except:
                varpercdelta = float("inf")
            #checks the variable being analyzed to determine the conditions to send email
            if (var1 < lowerlimit or var1 > upperlimit) and abs(varpercdelta) > 0.03:
                 type_alert = [coluna, '', '', False]
                 if var1 < crit_lowerlimit or var1 > crit_upperlimit  and lowerlimit != upperlimit:
                     type_alert[3] = True
                 if varabsdelta < 0:
                     type_alert[2] = 'down'
                 else:
                     type_alert[2] = 'up'
                 logging.info("Outlier found: %s" %type_alert)

                 # -------------- EMAIL CONSTRUCTING BLOCK (TRENDS) --------------
                 var_email = avoid_same_content(last_emails_content, type_alert)
                 if var_email == True:
                     if varabsdelta < 0:
                         sign = '-'
                         if coluna == 'position':
                             if own_condition == 1:
                                 color = 'green'
                             else:
                                 color = 'red'
                         else:
                             if own_condition == 1:
                                 color = 'red'
                             else:
                                 color = 'green'
                     else:
                         sign = '+'
                         if coluna == 'position':
                             if own_condition == 1:
                                 color = 'red'
                             else:
                                 color = 'green'
                         else:
                             if own_condition == 1:
                                 color = 'green'
                             else:
                                 color = 'red'
                     outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, period_ends, trim_var, upperlimit, lowerlimit, analysis, n)
                     if varpercdelta != float("inf"):
                         text = outlier_phrase(dict_colunas['semantic'][language][coluna], type_alert, traffic_type, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, 'dimension_off', 'yes', outliers_over_time)
                         text += '<br><img src="cid:Graph%s.png"><br>' %n
                     elif any(item != 0 for item in var[:-1]) == False:
                         text = outlier_phrase_zero(dict_colunas['semantic'][language][coluna], type_alert, traffic_type, var1, date1, color, sign, format_type, 'dimension_off', 'yes', 'zero')
                         text += '<br><img src="cid:Graph%s.png"><br>' %n
                     else:
                         continue
                     
                     url_prior_outliers.append(varpercdelta)
                     alerts_summary[url_id].append(type_alert)
                     url_outliers.append(text)
                     n += 1

            # ------------------------------- TRENDS ANALYSIS --------------------------------
            #Checks if a variable is on a rising or falling trend. Accept criteria is:
            #R² > correlation coefficient
            #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
            if r_value > dict_colunas['correlation'][coluna] and p_value < 0.05:
                type_alert = [coluna, '', '', False]
                #classifying the trend found             
                if r_value > 0.99:
                    type_alert[3] = True
                if slope < 0:
                    type_alert[2] = 'falling'                               
                else:
                    type_alert[2] =  'rising'
                logging.info("Trend found: %s" %type_alert)

                # -------------- EMAIL CONSTRUCTING BLOCK (TRENDS) --------------
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    if slope < 0:
                        trend_type += ' falling'
                        if coluna == 'position':
                            if own_condition == 1:
                                 color = 'green'
                            else:
                                 color = 'red'
                        else:
                            if own_condition == 1:
                                 color = 'red'
                            else:
                                 color = 'green'                                     
                    else:
                        trend_type += ' rising'
                        if coluna == 'position':
                            if own_condition == 1:
                                 color = 'red'
                            else:
                                 color = 'green'
                        else:
                            if own_condition == 1:
                                 color = 'green'
                            else:
                                 color = 'red'
                    trend = trend_phrase(traffic_type, dict_colunas['semantic'][language][coluna], type_alert, color, trend_type, format_type, 'dimension_off')
                    trend += '<br><img src="cid:Graph%s.png"><br>' %n

                    alerts_summary[url_id].append(type_alert)
                    url_trends.append(trend)
                    url_prior_trends.append(r_value)
                    trend_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, period_ends, vect_reg, r_value, color, analysis, n)
                    n += 1


    if url_trends != [] or url_outliers != [] or keywordstext_email != '' and alerts_summary[url_id] != []:
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

        #sorts changes from most negative to most positive
        sorted_trends = sort_email_from_list(url_prior_trends, url_trends,'color:red','color:blue','color:green')
        sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green','Top 10')
            
        file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span>' %(siteurl, siteurl)
        file_emailtext += "".join(sorted_email)
        file_emailtext += "".join(sorted_trends) + keywordstext_email + '<br>'
        
#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Simplex Search Data','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
