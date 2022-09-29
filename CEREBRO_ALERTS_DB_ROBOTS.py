#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- ROBOTS CHECKING --------------------------------
table_name, script_type = 'robots', 'alerts'
url_ids = get_url_ids('robots','robots.txt',str)
url_ids = list(set(url_ids) & set(allowed_url_ids))

dict_texts = {'text1':{
                        'en':'<br><a href="%s/robots.txt">%s</a> robots.txt is showing a <b>%s Status Code</b><br>',
                        'pt':'<br>O robots.txt de <a href="%s/robots.txt">%s</a> está apresentando Status Code <b>%s</b><br>',
                        },
              'text2':{
                        'en':'<br><b><a href="%s/robots.txt">%s</a></b> robots.txt file has changed.<br><br>',
                        'pt':'<br>O robots.txt de <b><a href="%s/robots.txt">%s</a></b> teve uma mudança.<br><br>',
                        },
              'text3':{
                        'en':'<div style="overflow:hidden;"><div style="width: 50%;float:left"><b><i>Robots.txt in {}</i></b><br>{}</div><div style="width: 50%; float:right"><b><i>Robots.txt in {}</i></b><br>{}</div></div>',
                        'pt':'<div style="overflow:hidden;"><div style="width: 50%;float:left"><b><i>Robots.txt em {}</i></b><br>{}</div><div style="width: 50%; float:right"><b><i>Robots.txt em {}</i></b><br>{}</div></div>',
                        },
              'text4':{
                        'en':'<br>The robots.txt is a text file created to instruct web robots (typically search engine robots) how to crawl pages of the website.<br>',
                        'pt':'<br>O robots.txt é um arquivo de texto criado para instruir os robôs da web (normalmente robôs de busca) como passar pelas páginas de um site.<br>',
                        },
             }

file_emailtext = ''

for url_id in url_ids:
    #gets last 2 entries for the specified url
    url_dict = {}
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select * from robots where url_id = '%s' order by datetime desc limit 0,2;" %url_id)
    results = cursor.fetchall()
    if results == ():
        logging.info("No information available for url_id: %s" %url_id)
        continue
    siteurl = results[0]['url']
    siteurl = str(urlparse(siteurl).netloc)
    try:
        day0 = results[1]
        day1 = results[0]
        date0 = day0['datetime']
        date1 = day1['datetime']
        logging.info("Analyzing %s" %siteurl)
    except:
        logging.info("No dates to compare for %s. Proceding to next url..." %siteurl)
        continue

    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select robots from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['robots']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about robots.txt data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour, sent_date))
                        continue
                    else:
                        logging.info("There is already an email alert sent to %s about robots.txt data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour))
                        continue
            except:
                pass

    difference = day1['difference']
    status = day1['status']
    old_status = day0['status']
    type_alert = ['', '', '', False]

    cursor.execute("select url from monitoring_links where id = '%s';" %url_id)
    link_url = cursor.fetchall()[0]['url']

    #if the test score changes more than 5 points it is considered and anomaly
    if difference == 1 and status != 200:
        type_alert = ['robots', 'status', str(status), False]
        alerts_summary[url_id].append(type_alert)
        file_emailtext += dict_texts['text1'][language] %(link_url, siteurl, status)

    elif difference == 1 and status == 200 and old_status == 200:
        logging.info("A difference was found")
        type_alert = ['robots', 'content', '', False]
        alerts_summary[url_id].append(type_alert)
        
        robots0 = day0['rules'].split('\n')
        robots1 = day1['rules'].split('\n')

        robots0_html = []
        robots1_html = []
        for line in robots0:
            if line in robots1:
                robots0_html.append(line+'<br>')
            else:
                robots0_html.append('<span style="color:red"><b>'+line+'</b></span><br>')
        for line in robots1:
            if line in robots0:
                robots1_html.append(line+'<br>')
            else:
                robots1_html.append('<span style="color:green"><b>'+line+'</b></span><br>')
        robots0_html = "".join(robots0_html)
        robots1_html = "".join(robots1_html)

        if dict_texts['text4'][language] not in file_emailtext:
            file_emailtext += dict_texts['text4'][language]
        file_emailtext += dict_texts['text2'][language]  %(link_url, siteurl)
        file_emailtext += dict_texts['text3'][language].format(str(date0), robots0_html, str(date1), robots1_html)

    elif difference == 1 and status == 200 and old_status != 200:
        type_alert = ['robots', 'status', str(status), False]
        alerts_summary[url_id].append(type_alert)
        
        robots1_html = day1['rules'].replace('\r\n','<br>').replace('\n','<br>')

        if dict_texts['text4'][language] not in file_emailtext:
            file_emailtext += dict_texts['text4'][language]
        file_emailtext += dict_texts['text2'][language]  %(link_url, siteurl)
        file_emailtext += dict_texts['text3'][language].format(str(date0), dict_texts['text1'][language] %(link_url, siteurl, old_status), str(date1), robots1_html)

    if type_alert in alerts_summary[url_id]:
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Robots.txt','change')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
