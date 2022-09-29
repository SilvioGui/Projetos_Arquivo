#imports all the libraries from calling script
from __main__ import *

def criterias_graph(reasons_graph):
    criteria_names = []
    criteria_values = []
    for key in reasons_graph:
        criteria_names.append(dict_colunas['semantic'][key])
        criteria_values.append(float(reasons_graph[key]))
    graph_title = get_graph_values('', '', '', [], 'days', 0, 'security')

    mean_length = int(numpy.mean([len(i) for i in criteria_names])*0.5)      #gets every column name length to define a mean column length as integer value
    wrapped_text = ["\n".join(textwrap.wrap(i,mean_length)) for i in criteria_names]    #breaks text in the column length defined above to make the axis good to read

    plt.figure(figsize=(len(criteria_names)*0.9, 2)) #fig size in x and y direction
    plt.margins(0.01, 0.05)

    #plots bar graph of criteria_name and its values. x is created as a list from 0 to len(criteria_names) to make it work as x axis
    x = numpy.arange(len(criteria_names))
    plt.bar(x, criteria_values, width = 0.4, color = 'red')  #uses red for graph
    plt.xticks(x, wrapped_text, rotation = 45, ha ='right', rotation_mode = 'anchor', fontsize = 7)    #enables ploting float vs string
    plt.title(graph_title , color = 'black', fontsize = 10, fontweight='bold')

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- OBSERVATORY ANALYSIS --------------------------------
table_name, script_type = 'observatory', 'alerts'
url_ids = get_url_ids('observatory','Observatory',str)
url_ids = list(set(url_ids) & set(allowed_url_ids))

colunas = ['content_security_policy','contribute','cookies','cross_origin_resource_sharing','public_key_pinning','redirection','referrer_policy',
'strict_transport_security','subresource_integrity','x_content_type_options','x_frame_options','x_xss_protection']

dict_colunas = {'semantic':
                        {'content_security_policy':'Content Security Policy',
                         'contribute':'Contribute.json',
                           'cookies':'Cookies',
                           'cross_origin_resource_sharing':'Cross-origin Resource Sharing',
                           'public_key_pinning':'HTTP Public Key Pinning',
                           'redirection':'Redirection',
                          'referrer_policy':'Referrer Policy',
                           'strict_transport_security':'HTTP Strict Transport Security',
                           'subresource_integrity':'Subresource Integrity',
                           'x_content_type_options':'X-Content-Type-Options',
                           'x_frame_options':'X-Frame-Options',
                           'x_xss_protection':'X-XSS-Protection',
                         },
                'subsections':{'text1':{
                                      'en':'Status changes were detected in <b>%s</b>. Details are explained below:<p style="padding-left:18px">',
                                      'pt':'Mudanças foram encontradas em <b>%s</b>. Detalhes estão explicados abaixo:<p style="padding-left:18px">',
                                     },
                               'text2':{
                                      'en':'Check the graph below to analyzed further security issues which can still be improved<br>',
                                      'pt':'Verifique o gráfico abaixo para analisar questões de segurança que ainda podem ser melhoradas<br>',
                                     },
                               'text3':{
                                      'en':'</b> and <b>',
                                      'pt':'</b> e <b>',
                                     },
                          }
           }

dict_links = {'content_security_policy':'https://infosec.mozilla.org/guidelines/web_security#content-security-policy',
              'contribute':'https://infosec.mozilla.org/guidelines/web_security#contributejson',
           'cookies':'https://infosec.mozilla.org/guidelines/web_security#cookies',
           'cross_origin_resource_sharing':'https://infosec.mozilla.org/guidelines/web_security#cross-origin-resource-sharing',
           'public_key_pinning':'https://infosec.mozilla.org/guidelines/web_security#http-public-key-pinning',
           'redirection':'https://infosec.mozilla.org/guidelines/web_security#http-redirections',
           'referrer_policy':'https://infosec.mozilla.org/guidelines/web_security#referrer-policy',
           'strict_transport_security':'https://infosec.mozilla.org/guidelines/web_security#http-strict-transport-security',
           'subresource_integrity':'https://infosec.mozilla.org/guidelines/web_security#subresource-Integrity',
           'x_content_type_options':'https://infosec.mozilla.org/guidelines/web_security#x-content-type-options',
           'x_frame_options':'https://infosec.mozilla.org/guidelines/web_security#x-frame-options',
           'x_xss_protection':'https://infosec.mozilla.org/guidelines/web_security#x-xss-protection',
           }

prior_changes = []
file_emailtext = []

for url_id in url_ids:
    #gets last 2 entries for the specified url
    url_dict = {}
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select * from observatory where url_id = '%s' order by datetime desc limit 0,2;" %url_id)
    results = cursor.fetchall()
    if results == ():
        logging.info("No information avalailable for url_id: %s" %url_id)
        continue
    siteurl = results[0]['url']
    siteurl2 = results[1]['url']

    if 'http' in siteurl or 'http' in siteurl2:
        logging.info("Wrong data can\'t be analyzed. Proceding to next url...")
        continue
    
    siteurl = str(urlparse(siteurl).netloc)
    format_type = int
    if siteurl == '':
        siteurl = results[0]['url']
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
    cursor.execute("select observatory from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['observatory']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about Mozilla Observatory data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                    else:
                        logging.info("There is already an email alert sent to %s about Mozilla Observatory data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                        continue
            except:
                pass

    cursor.execute("select url from monitoring_links where id = '%s';" %url_id)
    link_url = cursor.fetchall()[0]['url']

    score0 = day0['score']
    score1 = day1['score']
    text = ''

    # ------------------------------ RUNNING THE ANALYSIS ----------------------------------------
    #absdelta and percdelta are the anomaly detectors
    absdelta = score1 - score0
    try:
        percdelta = (score1/score0)-1
    except:
        percdelta = float("inf")

    #if the test score changes more than 5 points it is considered and anomaly
    try:
        details = json.loads(day1['details'])
    except:
        pass

    if abs(absdelta) >= 5:
        type_alert = ["observatory scan", '', '', False]
        #classifying the change found             
        if absdelta < 0:
            sign = '-'
            type_alert[2] = 'down'
        else:
            sign = '+'
            type_alert[2] = 'up'
        if abs(absdelta) > 30:
            type_alert[3] = True
        logging.info("Change found in observatory scan")

        changes = []
        changes_links = []
        changes_description = []
        reasons = {}
        reasons_graph = {}
        for coluna in colunas:
            rulescore0 = day0[coluna]
            rulescore1 = day1[coluna]
            try:
                value = rulescore1 - rulescore0
                reasons[coluna] = value
                reasons_graph[coluna] = rulescore1
                if value != 0:
                    detail = details[coluna].replace('_','-')
                    changes_description.append(detail)
                    changes_links.append(dict_links[coluna])
                    changes.append(dict_colunas['semantic'][coluna])
            except:
                pass
        if absdelta < 0:
            sign = '-'
            color = 'red'
        else:
            sign = '+'
            color = 'green'

        if percdelta != float("inf"):
            text = get_comparison_phrases(link_url, 'Observatory Scan Score', score0, date0, score1, date1, sign, color, abs(percdelta), type_alert, format_type, 'singular')
        else:
            text += get_comparison_phrases_zero(link_url, 'Observatory Scan Score', date0, score1, date1, color, format_type)                     

        #in case there are changes, it reports the status of each parameter changed. Try/except is necessary to avoid comparison to empty (for new entered websites)
        try:
            if len(changes) == 1:
                text += dict_colunas['subsections']['text1'][language] %changes[0]
            elif len(changes) == 2:
                text += dict_colunas['subsections']['text1'][language] %(changes[0] + dict_colunas['subsections']['text3'][language] + changes[1])
            else:
                text += dict_colunas['subsections']['text1'][language] %(', '.join(changes[0:(len(changes)-1)]) + dict_colunas['subsections']['text3'][language] + changes[len(changes)-1])
            line_count = 1
            for detail,link in zip(changes_description, changes_links):
                if line_count == 1:
                    text += '%s. <i><a href="%s">%s</a></i>' %(line_count, link, detail)
                else:
                    text += '<br>%s. <i><a href="%s">%s</a></i>' %(line_count, link, detail)
                line_count += 1
            text += '</p>'
        except:
            pass
        if score1 != 100:
            mainreason = min(reasons, key=reasons.get)
            criterias_graph(reasons_graph)
            text += dict_colunas['subsections']['text2'][language]
            text += '<br><img src="cid:Graph%s.png"><br>' %n
            n += 1
        file_emailtext.append(text)
        alerts_summary[url_id].append(type_alert)
        prior_changes.append(percdelta)

    if text != '':
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != []:
    file_emailtext = sort_email_from_list(prior_changes, file_emailtext)
    file_emailtext = "".join(file_emailtext)

    title = title_to_email_section('Observatory Scan','change')
    file_emailtext = title + file_emailtext
else:
    file_emailtext = ''
    logging.info("No data sent to email")
