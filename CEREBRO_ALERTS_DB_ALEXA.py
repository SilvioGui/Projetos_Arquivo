#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- ALEXA DATA --------------------------------
table_name, script_type = 'alexa', 'alerts'
url_ids = get_url_ids('alexa','Alexa',str)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#gets all the columns to compare data
colunas = ['global_rank', 'country_rank', 'bounce_rate', 'page_p_visit', 'time_on_site', 'search_visits']

dict_colunas = {'semantic': {'en':{
                                    'global_rank':'Global Rank',
                                    'country_rank':'Country Rank',
                                    'bounce_rate':'Bounce Rate',
                                    'page_p_visit':'Pages per Visit',
                                    'time_on_site':'Time Spent on Site',
                                    'search_visits':'Search Visits (%)',
                                    'how_fast':'Loading Speed (Seconds)',
                                    },
                             'pt':{
                                    'global_rank':'Rank Global',
                                    'country_rank':'Rank no País',
                                    'bounce_rate':'Bounce Rate',
                                    'page_p_visit':'Páginas por Visita',
                                    'time_on_site':'Tempo Gasto no Site',
                                    'search_visits':'Visitas por Busca (%)',
                                    'how_fast':'Tempo de Carregamento (Segundos)',
                                    },
                             },
                            'format':{
                                    'global_rank':int,
                                    'country_rank':int,
                                    'bounce_rate': float,
                                    'page_p_visit':float,
                                    'time_on_site':float,
                                    'search_visits':float,
                                    'how_fast':float,
                                    }

}

file_emailtext = ''

for url_id in url_ids:
    #gets last 2 entries for the specified url
    url_dict = {}
    urltrends = []
    urlprior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select * from alexa where url_id = '%s' order by date desc limit 0,10;" %url_id)
    results = cursor.fetchall()
    siteurl = results[0]['url']
    siteurl2 = results[1]['url']
    if 'http' in siteurl or 'http' in siteurl2:
        logging.info("Wrong data can\'t be analyzed. Proceding to next url...")
        continue
    
    domain = get_domain_name(siteurl)
    traffic_type = ''
    analysis = 'days'
    maxdate = 0
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
    cursor.execute("select alexa from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['alexa']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about Alexa data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                    else:
                        logging.info("There is already an email alert sent to %s about Alexa data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                        continue
            except:
                pass

    # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
    # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
    cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
    last_emails_content = cursor.fetchall()

    for coluna in colunas:
        var = []
        dates = []
        format_type = dict_colunas['format'][coluna]
        for result in results:
            try:
                var[:0] = [format_type(result[coluna])]
                dates[:0] = [str(result['date'])]
            except:
                continue

        while 0 in var and len(var)!= 0:
            exclude_itens = var.index(0)
            var.pop(exclude_itens)
            dates.pop(exclude_itens)
            
        if len(var) >= 5:                        
            #calculate linear regression of the values comparing to a x vector of unitary incremented values (only if there are at least 5 values)
            x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')             
        else:
            logging.info("No sufficient data available for %s %s. Proceding to next url..." %(siteurl, coluna))
            continue
            
        # ------------------------------- TRENDS ANALYSIS --------------------------------
        #Checks if a variable is on a rising or falling trend. Accept criteria is:
        #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
        if r_value > 0.925 and p_value < 0.05:
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
                    if coluna in ['global_rank', 'country_rank','bounce_rate','how_fast']:
                         if own_condition == 1:
                             color = 'green'
                         else:
                             color = 'red'
                    elif coluna in ['page_p_visit', 'time_on_site']:
                         color = 'blue'
                    else:
                         if own_condition == 1:
                             color = 'red'
                         else:
                             color = 'green'
                else:
                    trend_type += ' rising'
                    if coluna in ['global_rank', 'country_rank','bounce_rate','how_fast']:
                         if own_condition == 1:
                             color = 'red'
                         else:
                             color = 'green'
                    elif coluna in ['page_p_visit', 'time_on_site']:
                         color = 'blue'
                    else:
                         if own_condition == 1:
                             color = 'green'
                         else:
                             color = 'red'
                trend = trend_phrase(traffic_type, dict_colunas['semantic'][language][coluna], type_alert, color, trend_type, format_type, 'dimension_off')
                trend += '<br><img src="cid:Graph%s.png"><br>' %n

                alerts_summary[url_id].append(type_alert)    
                urltrends.append(trend)
                urlprior_trends.append(r_value)
                trend_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, dates, vect_reg, r_value, color, analysis, n)                    
                n += 1

    #------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
    #email sending part
    if urltrends != []:
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

        #sorts trends from strongest to weakest
        sorted_trends = sort_email_from_list(urlprior_trends, urltrends,'color:red','color:blue','color:green')

        cursor.execute("select url from monitoring_links where id = '%s';" %url_id)
        link_url = cursor.fetchall()[0]['url']
            
        file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(link_url, link_url)
        file_emailtext += "".join(sorted_trends)

if file_emailtext != '':
    title = title_to_email_section('Alexa','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
