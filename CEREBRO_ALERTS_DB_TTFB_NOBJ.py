#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- TTFB - NOBJ ANALYSIS --------------------------------
dict_colunas = {'semantic':{'en':{
                                 'ttfb':'Time to First Byte',
                                 'number_obj':'Number of Objects on Page'
                                 },
                             'pt':{
                                 'ttfb':'Time to First Byte',
                                 'number_obj':'Número de Objetos na Página'
                                 },
                            },
                'subtitles':{'en':{
                                 'ttfb':'<br><span style="font-size:14px"><b>Changes in Time to First Byte</b></span>',
                                 'number_obj':'<br><span style="font-size:14px"><b>Changes in Number of Objects</b></span>'
                                 },
                             'pt':{
                                 'ttfb':'<br><span style="font-size:14px"><b>Mudanças no Time to First Byte</b></span>',
                                 'number_obj':'<br><span style="font-size:14px"><b>Mudanças no Número de Objetos</b></span>'
                                 },
                            }
                }

dict_texts = {'text1':{
                        'en':'<br>The TTFB metric captures how long it takes your browser to receive the first byte of a response from a web server when you \
                             request a particular website URL. It is an important metric for SEO because it has impact in the SERP position.<br>',                        
                        'pt':'<br>O TTFB é uma métrica que captura quanto tempo o navegador leva para receber o primeiro byte de resposta de um servidor quando \
                             uma URL particular é requisitada. É uma métrica importante para SEO porque impacta na posição apresentada nos resultados de busca.<br>',
                        },
                }

table_name, script_type = 'ttfb', 'alerts'
url_ids = get_url_ids('ttfb','TTFB')
url_ids = list(set(url_ids) & set(allowed_url_ids))

ttfbprior_changes = []
nobjprior_changes = []
ttfbfile_emailtext = []
nobjfile_emailtext = []
file_emailtext = ''

for url_id in url_ids:
    url_dict = {}
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select url,ttfb from monitoring_links where id = '%s';" %url_id)
    results = cursor.fetchall()
    traffic_types = results[0]['ttfb']
    siteurl = results[0]['url']
    cursor.execute("select own_url from monitoring_links where id = %s and owner_id = %s;" , [url_id, owner_id])
    own_condition = cursor.fetchall()[0]['own_url']

    filters = traffic_types.split(',')
    for traffic_type in filters:
        text = ''
        #gets last 10 entries for the specified url and type. TTFB uses 10 values due to statistisc, Number of Objects just compare the last 2 points
        cursor.execute("select * from ttfb_nobj where (url_id,filter_type) = ('%s','%s') order by date desc limit 0,10;" %(url_id, traffic_type))
        results = cursor.fetchall()
        if len(results) < 5:
            logging.info("No dates to compare for %s %s. Proceding to next url..." %(siteurl, traffic_type))
            continue            
        try:
            ttfb_values = []
            for result in results:
                ttfb_values[:0] = [float(result['ttfb'])]

            day0 = results[1]
            day1 = results[0]
            graph_date0 = results[len(results)-1]['date']
            date0 = day0['date']
            date1 = day1['date']
        except:
            logging.info("No dates to compare for %s %s. Proceding to next url..." %(siteurl, traffic_type))
            continue

        # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
        cursor.execute("select ttfb from alerts_analysis_history where url_id = '%s';" %url_id)
        last_alert_date = cursor.fetchall()
        if last_alert_date != ():
            last_alert_date = last_alert_date[0]['ttfb']         #gets the last date from the alerts sent in past
            if last_alert_date != None:
                last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
                try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                    email_alert_id = last_alert_date[email_group_id].split('|')[0]
                    last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                    if last_analyzed_date == str(date1):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                        cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                        sent_date = cursor.fetchall()[0]['sent_date']
                        logging.info("There is already an email alert sent to %s about TTFB and Number of Objects data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                except:
                    pass
        logging.info("Analyzing %s %s" %(siteurl, traffic_type))

        #excludes from analysis days which had 0 as value
        i = 0
        while i < len(ttfb_values):
            value = ttfb_values[i]
            if value == 0:
                ttfb_values.pop(i)
                i -= 1
                #this script doesn't produce graphs, so there is no dates list to exclude data from
            i += 1        

        # ------------------------------ RUNNING THE ANALYSIS ----------------------------------------
        # ---------------- TTFB Block ----------------
        try:
            #uses trimmean to get expected value
            ttfb0 = float(day0['ttfb'])
            ttfb1 = float(day1['ttfb'])
            format_type = float
            trim_mean_ttfb = format_type(round(stats.trim_mean(ttfb_values[:-1], 0.25),2))
            #uses interquartile range to estimate if values are outliers or not
            q75 = numpy.percentile(ttfb_values, 75)
            q25 = numpy.percentile(ttfb_values, 25)
            iqr = q75 - q25
            upperlimit = q75 + 1.5*iqr
            lowerlimit = q25 - 1.5*iqr

            ttfbabsdelta = ttfb1 - trim_mean_ttfb
            try:
                ttfbpercdelta = (ttfb1/trim_mean_ttfb)-1
            except:
                ttfbpercdelta = float("inf")
                
            #For TTFB, if the changes are greater than 50 points and more than 10%, it is considered and anomaly
            if (ttfb0 == ttfb1 == 0) == True:
                logging.info("TTFB is not captured for the domain %s" %siteurl)
            else:
                if ttfb1 < lowerlimit or ttfb1 > upperlimit and ttfb1 != ttfb0:
                    type_alert = ['TTFB', traffic_type, '', False]
                    #classifying the outlier found             
                    if ttfbabsdelta < 0:
                        type_alert[2] = 'up'
                    else:
                        type_alert[2] = 'down'
                    if abs(ttfbpercdelta) > 0.3:
                        type_alert[3] = True
                    logging.info("Outlier found: %s" %type_alert)
                        
                    ttfb_url = 'http://vps97572.ovh.net/linkchecker/display_stat.php?url=%s&filter_name=%s&line=2&from=%s&to=%s' %(siteurl, traffic_type, graph_date0, date1)
                    if ttfbabsdelta < 0:
                        sign = '-'
                        if own_condition == 1:
                            color = 'green'
                        else:
                            color = 'red'
                    else:
                        sign = '+'
                        if own_condition == 1:
                            color = 'red'
                        else:
                            color = 'green'
                    traffic_type2 = '<a href="%s">%s</a> ' %(siteurl,siteurl) + traffic_type
                    text = outlier_phrase(dict_colunas['semantic'][language]['ttfb'], type_alert, traffic_type2, ttfb1, date1, color, abs(ttfbpercdelta), trim_mean_ttfb, sign, format_type, 'dimension_on', 'no', [0, 1])
                    if language == 'en':
                        text += 'TTFB graphic is available in this <a href="%s">link</a> <br>'  %ttfb_url
                    elif language == 'pt':
                        text += 'O gráfico de TTFB está disponível neste <a href="%s">link</a><br>'  %ttfb_url

                    alerts_summary[url_id].append(type_alert)
                    ttfbfile_emailtext.append(text)
                    ttfbprior_changes.append(ttfbpercdelta)

        except:
            logging.error("Error while processing TTFB analysis of %s %s" %(siteurl, traffic_type))

        # -------------- Number of Objects Block -----------------
        #absdelta and percdelta are the anomaly detectors
        try:
            nobj0 = day0['number_obj']
            nobj1 = day1['number_obj']
            if nobj1 == 0 or nobj0 == 0:
                logging.info('There is no suficient date to analyze the "%s %s"...' %(siteurl, traffic_type))
                continue
            nobjabsdelta = nobj1 - nobj0
            try:
                nobjpercdelta = (nobj1/nobj0)-1
            except:
                nobjpercdelta = float("inf")

            #For Number of objects, if the the number changes more than 10 points and more than 10%, it is considered and anomaly
            if (nobj0 == nobj1 == 0) == True:
                logging.info("Number of objects is not captured for the domain %s" %siteurl)
            else:
                if abs(nobjabsdelta) > 10 and abs(nobjpercdelta) > 0.10:
                    format_type = int
                    type_alert = ['Number Obj', traffic_type, '', False]
                    #classifying the change found             
                    if nobjabsdelta < 0:
                        sign = '-'
                        type_alert[2] = 'down'
                    else:
                        sign = '+'
                        type_alert[2] = 'up'
                    if abs(nobjabsdelta) > 200:
                        type_alert[3] = True
                    logging.info("Change found: %s" %type_alert)
                    color = 'blue'

                    nobj_url = 'http://vps97572.ovh.net/linkchecker/display_stat.php?url=%s&filter_name=%s&line=3&from=%s&to=%s' %(siteurl, traffic_type, graph_date0, date1)
                    if nobjabsdelta < 0:
                        sign = '-'
                    else:
                        sign = '+'

                    text = get_comparison_phrases(siteurl, dict_colunas['semantic'][language]['number_obj'] + " " + traffic_type, nobj0, date0, nobj1, date1, sign, color, abs(nobjpercdelta), type_alert, format_type, 'singular')
                    if language == 'en':
                        text += 'Number of objects graphic is available in this <a href="%s">link</a> <br>'  %nobj_url
                    elif language == 'pt':
                        text += 'O gráfico do número de objetos na página está disponível neste <a href="%s">link</a> <br>'  %nobj_url

                    alerts_summary[url_id].append(type_alert)
                    nobjfile_emailtext.append(text)
                    nobjprior_changes.append(nobjpercdelta)
        except:
            logging.error("Error while processing Number oj Objects analysis of %s %s" %(siteurl, traffic_type))

        if text != '':
            dict_urls[url_id] = str(date1)
            analyzed_urls[execute_file[2]] = dict_urls 

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if ttfbfile_emailtext != [] or nobjfile_emailtext != []:
    #sorting TTFB and NOBJ
    ttfbfile_emailtext = sort_email_from_list(ttfbprior_changes, ttfbfile_emailtext)    
    nobjfile_emailtext = sort_email_from_list(nobjprior_changes, nobjfile_emailtext)    

    if ttfbfile_emailtext != []:
        file_emailtext += dict_colunas['subtitles'][language]['ttfb'] + dict_texts['text1'][language] + "".join(ttfbfile_emailtext)
    if nobjfile_emailtext != []:
        file_emailtext += dict_colunas['subtitles'][language]['number_obj'] + "".join(nobjfile_emailtext)
    title = title_to_email_section('TTFB Server','change')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
