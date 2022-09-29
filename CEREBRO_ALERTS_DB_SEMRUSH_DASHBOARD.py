#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
        
# -------------------------- SEM RUSH DATA --------------------------------
table_name, script_type = 'sem_rush_dashboard', 'alerts'
url_ids = get_url_ids('sem_rush_dashboard','SEM Rush domains',str)
url_ids = list(set(url_ids) & set(allowed_url_ids))

colunas = ['organic_search','paid_search','backlinks','organic_keywords','paid_keywords']
#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection, 3rd section to trend analysis correlation factor
dict_colunas = { 
    #first subdivision
    'semantic':{'en':{
                    'organic_search':'Organic Traffic',
                    'paid_search':'Paid Traffic',
                    'backlinks':'Backlinks',
                    'organic_keywords':'Organic Keywords',
                    'paid_keywords':'Paid Keywords',
                    },
                'pt':{
                    'organic_search':'Tráfego Orgânico',
                    'paid_search':'Tráfego Pago',
                    'backlinks':'Backlinks',
                    'organic_keywords':'Keywords Orgânicas',
                    'paid_keywords':'Keywords Pagas',
                    },
                },
    #second subdivision
    'outlier':{
                'organic_search':1.2,
                'paid_search':1.2,
                'backlinks':1.2,
                },
    #third subdivision
    'correlation':{
                'organic_search':0.9,
                'paid_search':0.9,
                'backlinks':0.925,
    },
    #fourth subdivision
    'format':{
                'organic_search':int,
                'paid_search':int,
                'backlinks':int,
    }

}

#dictionary containing necessary values for every keyword.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection, 3rd section to trend analysis correlation factor
dict_keywords = { 
    #first subdivision
    'semantic':{'en':{
                     'cpc':'CPC',
                     'volume':'Volume',
                     'traffic':'Traffic (%)',
                     'position':'Position',
                    },
                'pt':{
                     'cpc':'CPC',
                     'volume':'Volume',
                     'traffic':'Tráfego (%)',
                     'position':'Posição',
                    },
                },
    #second subdivision
    'outlier':{
                 'cpc':2,
                 'volume':1.5,
                 'traffic':1.5,
                 'position':1.5,
                },
    #third subdivision
    'correlation':{
                 'cpc':0.9,
                 'volume':0.8,
                 'traffic':0.8,
                 'position':0.9,
    },
    #fourth subdivision
    'format':{
                 'cpc':float,
                 'volume':int,
                 'traffic':float,
                 'position':int,
    }
}

dict_texts = {'en':
                  {'text1':'<br><b>%s</b> has changed from <b>%s</b> <i>(%s)</i> to <b>%s</b> <i>(%s)</i>. The expected value was <b>%s</b>',
                   'text2':'<br>Landing page for keyword "%s" has changed from %s <i>(%s)</i> to %s <i>(%s)</i>',
                   'text3':'<br>The keywords <span style="color:red;"><i>%s</i></span> are not present in the Top 10 %s anylonger. They were replaced by <span style="color:green;"><i>%s</i></span>.<br>',
                   'text4':'<br><br><b><span style="font-size:15px;">Top 10 %s Analysis</b><span>',                  
                   },
              'pt':
                  {'text1':'<br><b>%s</b> mudou de <b>%s</b> <i>(%s)</i> para <b>%s</b> <i>(%s)</i>. O valor esperado era <b>%s</b>',
                   'text2':'<br>A Landing page da keyword "%s" mudou de %s <i>(%s)</i> para %s <i>(%s)</i>',
                   'text3':'<br>As keywords <span style="color:red;"><i>%s</i></span> não estão mais presentes entre as Top 10 %s. Elas foram substituídas por <span style="color:green;"><i>%s</i></span>.<br>',
                   'text4':'<br><br><b><span style="font-size:15px;">Análise das Top 10 %s</b><span>',                  
                  },
            }
    
prior_changes = []
file_emailtext = ''

for url_id in url_ids:
    url_dict = {}
    url_trends = []
    url_outliers = []
    url_prior_outliers = []
    url_prior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    org_keywordstext_email = ''
    paid_keywordstext_email = ''
    #gets last 10 weekday entries for the specified url
    cursor.execute("select weekday((select max(date) from sem_rush_dashboard where url_id = %s));" %url_id)
    maxdate = cursor.fetchall()[0]['weekday((select max(date) from sem_rush_dashboard where url_id = %s))' %url_id]

    cursor.execute("select * from sem_rush_dashboard where (weekday(date),url_id) = ('%s','%s') order by date desc limit 0,10;" %(maxdate, url_id))
    results = cursor.fetchall()
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    traffic_type = ''
    analysis = 'weekdays'
    try:
        day0 = results[1]
        day1 = results[0]
        date0 = day0['date']
        date1 = day1['date']
    except:
        logging.info("No dates to compare for %s. Proceding to next url..." %siteurl)
        continue

    logging.info("Analyzing %s" %siteurl)
    cursor.execute("select own_url from monitoring_links where id = %s and owner_id = %s;" , [url_id, owner_id])
    own_condition = cursor.fetchall()[0]['own_url']

    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select sem_rush_dashboard from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['sem_rush_dashboard']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about SEM Rush data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                        logging.info("There is already an email alert sent to %s about SEM Rush data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                        continue
            except:
                pass

    # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
    # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
    cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
    last_emails_content = cursor.fetchall()

    for coluna in colunas:
        if coluna in ['organic_keywords','paid_keywords']:
            #in case the 'coluna' analyzed is a json of organic and paid keywords, it has a specialized analysis for every kind of division
            keywords_db = json.loads(results[0][coluna])
            old_keywords_db = json.loads(results[1][coluna])
            # turns the dict returned into a string ordering the keywords by 'trafficIndex'
            keywords_db = sorted(keywords_db.items(), key=lambda v: float(v[1]['traffic']), reverse=True)
            old_keywords_db = sorted(old_keywords_db.items(), key=lambda v: float(v[1]['traffic']), reverse=True)

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
            dates = []

            # splits variables in different type so they can be analyzed in different ways
            var_types = ['cpc','volume','traffic','position']

            # Rearranges stored data grouping keyword metrics and time in which they occur
            for result in results:
                dict_results = {}
                analyze_date = result['date']
                dates[:0] = [analyze_date]
                json_result = json.loads(result[coluna])
                for keyword in analyze_keywords:
                    keyword_dict = {}
                    if keyword in json_result.keys():
                        for var in var_types:
                            keyword_dict[var] = json_result[keyword][var]
                    else:
                        for var in var_types:
                            keyword_dict[var] = 'Not present in top 100 keywords'
                    dict_results[keyword] = keyword_dict
                dict_analysis[analyze_date] = dict_results

            for keyword in analyze_keywords:
                table_html = ''
                table_header = ''                
                table_rows = ''
                keywordstext = ''
                for var_type in var_types:
                    format_type = dict_keywords['format'][var_type]
                    kw_dates = dates
                    var = []
                    for analyze_date in kw_dates:
                        var.append(dict_analysis[analyze_date][keyword][var_type])
                    while 'Not present in top 100 keywords' in var:
                        exclude_itens = var.index('Not present in top 100 keywords')
                        var.pop(exclude_itens)
                        kw_dates.pop(exclude_itens)
                        
                    if len(var) < 2:
                        logging.info('There is no suficient history to analyze the keyword: "%s". Proceding to the next keyword...' %keyword)
                        break

                    newer_var = format_type(var[len(var)-1])
                    old_var = var[len(var)-2]
                    newer_analyze_date = kw_dates[len(kw_dates)-1]
                    old_analyze_date = kw_dates[len(kw_dates)-2]
                    # KEYWORD CONTINUOUS VARIABLE ANALYSIS   
                    if len(var) >= 4:
                        #uses trimmean to get expected value
                        npvar = numpy.array(var)
                        var = npvar.astype(numpy.float)
                        trim_var = format_type(round(stats.trim_mean(var, 0.25),2))
                        #uses interquartile range to estimate if values are outliers or not
                        q75 = numpy.percentile(var, 75)
                        q25 = numpy.percentile(var, 25)
                        iqr = q75 - q25
                        upperlimit = q75 + 1.5*iqr
                        lowerlimit = q25 - 1.5*iqr
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
                            logging.info("trend found: %s" %keyword)
                            
                            var_email = avoid_same_content(last_emails_content, type_alert)
                            if var_email == True:
                                if keywordstext == '':
                                    keywordstext = '<span style="color:blue"><br><b>%s</b></span>' %keyword
                                if slope < 0:
                                    if var_type in ['cpc','position']:
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
                                    if var_type in ['cpc','position']:
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
                                    table_header += '<tr><th style="table-layout: fixed;color: white;background-color: black;text-align:center;border: 1px solid black;">Metric\Date</th>'
                                    for analyze_date in kw_dates:
                                        table_header += '<th style="table-layout: fixed;color: white; background-color: black;text-align:center;border: 1px solid black;">'+str(analyze_date)+'</th>'
                                    table_header += '<th style="table-layout: fixed;color: white;background-color: black;text-align:center;border: 1px solid black;">Trend</th></tr>'
                                # body
                                table_rows += '<tr><td style="table-layout: fixed;text-align:center;border: 1px solid black;">'+dict_keywords['semantic'][language][var_type]+'</td>'
                                for var_value in var:
                                    table_rows += '<td style="table-layout: fixed;text-align:center;border: 1px solid black;">'+str(format_type(var_value))+'</td>'
                                table_rows += '<td style="table-layout: fixed;text-align:center;border: 1px solid black;color:%s"> %s </td></tr>' %(color, slope)
                                alerts_summary[url_id].append(type_alert)
                                                                                           
                        if table_header != '' and var_type == var_types[len(var_types)-1]:
                            table_html += '<table style="table-layout: fixed; border: 1px solid black;border-collapse:collapse;width:100%;font-size:10px;">'+table_header+table_rows+'</table>'

                        # KEYWORD OUTLIER ANALYSIS
                        if newer_var > upperlimit or newer_var < lowerlimit:
                            try:
                                var_change = newer_var/trim_var - 1
                            except:
                                var_change = float("inf")
                            type_alert = ["keyword %s" %keyword, var_type, '', False]
                            if var_change > 0:
                                type_alert[2] = 'up'
                            else:
                                type_alert[2] = 'down'

                            var_email = avoid_same_content(last_emails_content, type_alert)                               
                            if var_email == True:
                                if var_change > 0:
                                    if var_type in ['cpc','position']:
                                        sign = '+'
                                        if own_condition == 1:
                                            color = 'red'
                                        else:
                                            color = 'green'
                                    else:
                                        sign = '+'
                                        if own_condition == 1:
                                            color = 'green'
                                        else:
                                            color = 'red'
                                else:
                                    if var_type in ['cpc','position']:
                                        sign = '-'
                                        if own_condition == 1:
                                            color = 'green'
                                        else:
                                            color = 'red'
                                    else:
                                        sign = '-'
                                        if own_condition == 1:
                                            color = 'red'
                                        else:
                                            color = 'green'                                      
                                if keywordstext == '':
                                    keywordstext = '<span style="color:blue"><br><b>%s</b></span>' %keyword
                                keywordstext += outlier_phrase(dict_keywords['semantic'][language][var_type], type_alert, traffic_type, newer_var, newer_analyze_date, color, abs(var_change), trim_var, sign, format_type, 'dimension_off', 'no', [0, 1])
                                alerts_summary[url_id].append(type_alert)
                    else:
                        logging.info('There is no suficient history to analyze trends for the keyword: "%s"' %keyword)
                        break

                if table_html != '':
                    if coluna == 'organic_keywords':
                        org_keywordstext_email += keywordstext + '<br>' + table_html
                    elif coluna == 'paid_keywords':
                        paid_keywordstext_email += keywordstext + '<br>' + table_html
                
            if set(analyze_keywords) != set(old_analyze_keywords):
                type_alert = ['ranking', coluna, '', False]
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    dif_in = list(set(analyze_keywords) - set(old_analyze_keywords))
                    dif_out = list(set(old_analyze_keywords) - set(analyze_keywords))                
                    dif_html = dict_texts[language]['text3'] %(", ".join(dif_out), dict_colunas['semantic'][language][coluna],", ".join(dif_in))
                    if coluna == 'organic_keywords':
                        org_keywordstext_email = dif_html + org_keywordstext_email
                    elif coluna == 'paid_keywords':
                        paid_keywordstext_email = dif_html + paid_keywordstext_email

                    if coluna == 'organic_keywords' and org_keywordstext_email != '':
                        org_keywordstext_email = dict_texts[language]['text4'] %dict_colunas['semantic'][language][coluna] + org_keywordstext_email
                    elif coluna == 'paid_keywords' and paid_keywordstext_email != '':
                        paid_keywordstext_email = dict_texts[language]['text4'] %dict_colunas['semantic'][language][coluna] + paid_keywordstext_email
                    if org_keywordstext_email != '' or paid_keywordstext_email != '':
                        alerts_summary[url_id].append(type_alert)
                        logging.info("Change found: top %s ranking" %coluna)

        # ------------------------------------------------------- NON KEYWORDS ANALYSIS BLOCK -----------------------------------------------------------------------
        else:   #the following block checks only number distortion, not the keywords
            var = []
            dates = []
            format_type = dict_colunas['format'][coluna]
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
                logging.info("No data available for %s %s. Proceding to next metric..." %(siteurl, coluna))
                continue

            # ------------------------------- TRENDS ANALYSIS --------------------------------
            #Checks if a variable is on a rising or falling trend. Accept criteria is:
            #R² > correlation coefficient
            #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
            if r_value > dict_colunas['correlation'][coluna] and p_value < 0.05:
                type_alert = [coluna, '', '', False]
                #classifying the trend found             
                if slope < 0:
                    type_alert[2] = 'falling'                               
                else:
                    type_alert[2] =  'rising'
                if r_value > 0.99:
                    type_alert[3] = True
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
                    trend_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, dates, vect_reg, r_value, color, analysis, n)
                    n += 1

            # ------------------------------ OUTLIERS ANALYSIS ----------------------------------------
            var0 = day0[coluna]
            var1 = format_type(day1[coluna])

            #absdelta and percdelta are the anomaly detectors
            varabsdelta = var1 - trim_var
            try:
                varpercdelta = (var1/trim_var)-1
            except:
                varpercdelta = float("inf")

            #checks the variable being analyzed to determine the conditions to send email
            if var1 < lowerlimit or var1 > upperlimit:
                 type_alert = [coluna, '', '', False]
                 if varabsdelta < 0:
                     type_alert[2] = 'down'
                 else:
                     type_alert[2] = 'up'
                 if var1 < crit_lowerlimit or var1 > crit_upperlimit and lowerlimit != upperlimit:
                     type_alert[3] = True
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
                     outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, dates, trim_var, upperlimit, lowerlimit, analysis, n)
                     if varpercdelta != float("inf"):
                         text = outlier_phrase(dict_colunas['semantic'][language][coluna], type_alert, traffic_type, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, 'dimension_on', 'yes', outliers_over_time)
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

    if url_trends != [] or url_outliers != [] or org_keywordstext_email != '' or paid_keywordstext_email != '':
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

        sorted_trends = sort_email_from_list(url_prior_trends, url_trends,'color:red','color:blue','color:green')
        sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green','Top 10')

        file_emailtext += '<br><br><span style="font-size:15px"><b><a href="%s">%s</a></b></span>' %(siteurl, siteurl)
        file_emailtext += "".join(sorted_email)
        file_emailtext += "".join(sorted_trends) + org_keywordstext_email + paid_keywordstext_email + '<br>'

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Simplex Search Base','change')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
