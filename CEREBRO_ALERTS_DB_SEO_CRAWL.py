#!/usr/bin/env python
# -*- coding: utf-8 -*-
#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
date_minus_1 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:00:00")

def escape_characters(str1):
    str1 = str1.replace("&","&amp;")
    str1 = str1.replace("<","&lt;")
    str1 = str1.replace(">","&gt;")
    str1 = str1.replace('"',"&quot;")
    str1 = str1.replace("'","&#039;")
    return str1

def git_strings(str1, str2):
    compared_strings = difflib.SequenceMatcher(None, str1, str2)
    compared_strings.get_opcodes()
    compared_strings.get_matching_blocks

    character_matches = compared_strings.matching_blocks

    similar_parts = []
    for character_matche in character_matches:
        
        equal_characters_index = character_matche[0]
        equal_characters_size = character_matche[2]

        matched_string = str1[equal_characters_index:(equal_characters_index+equal_characters_size)]
        if len(matched_string) > 1:
            similar_parts.append(matched_string)

    str1 = escape_characters(str1)
    str2 = escape_characters(str2)
    for similar_part in similar_parts:
        if similar_part not in '<span style="background-color: white;"></span>':
            similar_part = escape_characters(similar_part)
            str1 = str1.replace(similar_part,'<span style="background-color: white;">%s</span>' %similar_part)
            str2 = str2.replace(similar_part,'<span style="background-color: white;">%s</span>' %similar_part)
    return str1, str2

# -------------------------- SEO TAGS ANALYSIS --------------------------------
table_name, script_type = 'seo_crawl', 'alerts'
url_ids = get_url_ids('seo_crawl','SEO Tags',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#dictionary used to make the email more semantic
dict_changes = {'semantic':{'en':{
                                'url':'Url',
                                'status':'Status',
                                'prev':'Relative Prev Link',
                                'next':'Relative Next Link',
                                'canonical':'Canonical',
                                'amp':'Amp Canonical Link',
                                'alternate':'Alternate Link',
                                'nalternate':'Number of Alternate Link',
                                'ntitle':'Number of Titles',
                                'title':'Title',
                                'nh1':'Number of H1s',
                                'nh2':'Number of H2s',
                                'nh3':'Number of H3s',
                                'nh4':'Number of H4s',
                                'nh5':'Number of H5s',
                                'nh6':'Number of H6s',
                                'h1':'H1',
                                'h2':'H2',
                                'h3':'H3',
                                'h4':'H4',
                                'h5':'H5',
                                'h6':'H6',
                                'description':'Meta Description',
                                'keywords':'Meta Keywords',
                                'robots':'Meta Robots',
                                'nlinks':'Number of Links',
                                'nimgs':'Number of Images',
                                'nimgsalt':'Number of Images Containing Alt',
                                'njavascript':'Number of Javascripts',
                                'ncss':'Number of CSS',
                                    },
                            'pt':{
                                'url':'Url',
                                'status':'Status',
                                'prev':'Link Relativo Prev',
                                'next':'Link Next Relativo',
                                'canonical':'Canonical',
                                'amp':'Amp Canonical Link',
                                'alternate':'Link Alternativo',
                                'nalternate':'Número de Links Alternativos',                                
                                'ntitle':'Número de Titles',
                                'title':'Title',
                                'nh1':'Número de H1s',
                                'nh2':'Número de H2s',
                                'nh3':'Número de H3s',
                                'nh4':'Número de H4s',
                                'nh5':'Número de H5s',
                                'nh6':'Número de H6s',
                                'h1':'H1',
                                'h2':'H2',
                                'h3':'H3',
                                'h4':'H4',
                                'h5':'H5',
                                'h6':'H6',
                                'description':'Meta Description',
                                'keywords':'Meta Keywords',
                                'robots':'Meta Robots',
                                'nlinks':'Número de Links',
                                'nimgs':'Número de Images',
                                'nimgsalt':'Número de Imagens Contendo Alt',
                                'njavascript':'Número de Javascripts',
                                'ncss':'Número de CSS',
                                },
                            },
                }

dict_details = {'semantic':{'en':{
                                'prev':'The rel="prev" atribute is important for the SEO of pages that have a continuous content spread over different urls',
                                'next':'The rel="next" atribute is important for the SEO of pages that have a continuous content spread over different urls',
                                'canonical':'Canonical tag points to search engines what page should be indexed when the bot access an URL',
                                'amp':'The rel="amphtml" points to a AMP version of the page',
                                'title':'Title tag describes concisely the content of a page',
                                'h1':'H1 tag describes the main topic of a page',
                                'h2':'H2 tag describes subtopics related to H1. It\'s relative weaker than H1 for SEO purposes',
                                'h3':'H3 tag describes subtopics related to H2',
                                'h4':'H4 tag describes subtopics related to H3',
                                'h5':'H5 tag describes subtopics related to H4',
                                'h6':'H6 tag describes subtopics related to H5. It has a very small significance in SEO',
                                'alternate':'The alternate link can point to different versions of a page such as mobile/desktop versions',
                                'description':'Meta description describes with some details the content of a page',
                                'robots':'Meta robots points whether the search engines should index this page or not, and follow its link or not',
                                'nimgsalt':'The images alt atribute is considered for image indexation on search engines',
                                'summary':'Check the summary below for details of the changes',                                
                                'Desktop Javascript Rendered':'Desktop Javascript Rendered',
                                'Desktop Not Rendered':'Desktop Not Rendered',
                                'Mobile Javascript Rendered':'Mobile Javascript Rendered',
                                'Mobile Not Rendered':'Mobile Not Rendered',
                                'Status 200':'Status 200 means the page works normally',
                                'Status 301':'Status 301 means the page was redirected permanently. The page will be deindexed and replaced by the destination page',
                                'Status 302':'Status 302 means the page was redirected temporarily. The page won\'t be deindexed and will keep showing in search results',
                                'Status 403':'Status 403 means the page access was not allowed',
                                'Status 404':'Status 404 means the url address doesn\'t exist',
                                'Status 429':'Status 429 means the url was called too many times in a short period, so it couldn\'t answer',
                                'Status 500':'Status 500 means there was some kind of server error in the moment of the access',
                                'Status 502':'Status 502 means the proxy server received an invalid answer from the server the origin server who received the final request',
                                'Status 503':'Status 503 means the server is in maintenance. This won\'t affect the page indexation',
                                    },
                            'pt':{
                                'prev':'O atributo rel="prev" é importante para o SEO de páginas que tem conteúdo espalhado por diferentes urls',
                                'next':'O atributo rel="next" é importante para o SEO de páginas que tem conteúdo espalhado por diferentes urls',
                                'canonical':'A tag Canonical aponta para os mecanismos de busca qual página deve ser indexada quando ele acessa uma URL',
                                'amp':'O atributo rel="amphtml" aponta para uma versão AMP da página',
                                'title':'A tag Title descreve concisamente o conteúdo de uma página',
                                'h1':'A tag H1 descreve o principal tópico de uma página',
                                'h2':'A tag H2 descreve subtópicos relacionados ao H1. É relativamente mais fraca que o H1 para propósitos de SEO',
                                'h3':'A tag H3 descreve subtópicos relacionados ao H2',
                                'h4':'A tag H4 descreve subtópicos relacionados ao H3',
                                'h5':'A tag H5 descreve subtópicos relacionados ao H4',
                                'h6':'A tag H6 descreve subtópicos relacionados ao H5. Tem significância muito baixa em SEO',
                                'alternate':'O link alternativo pode apontar versões diferentes de uma pagina, como versões mobile/desktop',
                                'description':'A meta description descreve com alguns detalhes o conteúdo de uma página',
                                'robots':'A meta robots indica se os buscadores devem indexar uma página ou não, e se devem seguir os links dela',
                                'nimgsalt':'O atributo alt das imagens é considerado para indexação de imagens em buscadores',
                                'summary':'Verifique o resumo abaixo para ver detalhes das mudanças',                                
                                'Desktop Javascript Rendered':'Desktop com Javascript Renderizado',
                                'Desktop Not Rendered':'Desktop sem Javascript Renderizado',
                                'Mobile Javascript Rendered':'Mobile com Javascript Renderizado',
                                'Mobile Not Rendered':'Mobile sem Javascript Renderizada',
                                'Status 200':'O Status 200 significa que a página funciona normalmente',
                                'Status 301':'O Status 301 significa que a página foi redirecionada de forma permanente. Ela será desindexada do Google e trocada pela página de destino',
                                'Status 302':'O Status 302 significa que a página foi redirecionada de forma temporária. Ela se manterá indexada no Google',
                                'Status 403':'O Status 403 significa que não houve permissão de acesso para a página chamada',
                                'Status 404':'O Status 404 significa que a página foi chamada não existe mais',
                                'Status 429':'O Status 429 significa que a página foi chamada muitas vezes em um curto período e não pôde responder',
                                'Status 500':'O Status 500 significa que houve algum tipo de erro do servidor no momento de acesso da página',
                                'Status 502':'O Status 502 significa que o servidor proxy recebeu uma resposta inválida do servidor para qual sua requisição foi encaminhada',
                                'Status 503':'O Status 503 significa que o servidor está em manutenação. Isso não deve alterar a indexação da página',
                                },
                            },
                }


dict_texts = {'text1':{
                            'en':'<p style="font-size:18px"><b>The following URLs had changes detected from last Simplex SEO Crawl to %s</b></p>',
                            'pt':'<p style="font-size:18px"><b>As URLs seguintes tiveram alterações se compararmos o último rastreamento da Simplex com %s</b></p>',
                           },
                   'text2':{
                            'en':'<b><a href="%s">%s</a> <i>(%s to %s)</i></b><br>',
                            'pt':'<b><a href="%s">%s</a> <i>(%s para %s)</i></b><br>',
                           },
                   'text3':{
                            'en':'The url keeps showing Status Code <b>%s</b><br><br>',
                            'pt':'A url segue apresentando Status Code <b>%s</b><br><br>',
                           },
                   'text4':{
                            'en':'Not Present',
                            'pt':'Não Presente',
                           },
                   'text5':{
                            'en':'<b>%s</b> has changed. The last value was <i>%s</i> and now it doesn\'t exist any longer <br>',
                            'pt':'O valor de <b>%s</b>. Seu valor anterior era <i>%s</i> e agora ele não existe mais<br>',
                           },
                   'text6':{
                            'en':'<b>%s</b> has changed. There were %s different values which are available on Simplex Database, now they doesn\'t exist any longer <br>',
                            'pt':'O valor de <b>%s</b> mudou. Haviam %s valores diferentes, que estão disponíveis no Banco de Dados da Simplex, agora não exite mais nenhum <br>',
                           },
                   'text7':{
                            'en':'<b>%s</b> has changed from <span style="background-color:#F08080"><i>%s</i></span> to <span style="background-color:#90EE90"><i>%s</i></span><br>',
                            'pt':'O valor de <b>%s</b> mudou de <span style="background-color:#F08080"><i>%s</i></span> para <span style="background-color:#90EE90"><i>%s</i></span><br>',
                           },
                   'text8':{
                            'en':'<b>%s</b> has changed. There were %s different values, which are available on Simplex Database. The new values are <i>%s</i><br>',
                            'pt':'O valor de <b>%s</b> mudou. Haviam %s valores diferentes, que estão disponíveis no Banco de Dados da Simplex. Os novos valores são <i>%s</i><br>',
                           },
                   'text9':{
                            'en':'<b>%s</b> has changed. The last value was <i>%s</i> and now there are %ss different values, which are available on Simplex Database<br>',
                            'pt':'O valor de <b>%s</b>. O último valor era <i>%s</i> e agora existem %s valores diferentes, que estão disponíveis no Banco de Dados da Simplex<br>',
                           },
                   'text10':{
                            'en':'<b>%s</b> has changed. There were %s different values, now there are %s. All of them are available on Simplex Database<br>',
                            'pt':'O valor de <b>%s</b> mudou. Haviam %s valores diferentes, agora existem %s. Todos eles estão disponíveis no banco de dados da Simplex<br>',
                           },
                   'text11':{
                            'en':'<b>%s</b> has changed. There are still %s different values, but some have changed. All of them are available on Simplex Database<br>',
                            'pt':'O valor de <b>%s</b> mudou. Ainda existem %s valores, mas alguns mudaram. Todos eles estão disponíveis no banco de dados da Simplex<br>',
                           },
                   'text12':{
                            'en':'<b>%s</b> has changed from <i>%s</i> to <i>%s</i><br>',
                            'pt':'O valor de <b>%s</b> mudou de <i>%s</i> para <i>%s</i><br>',
                           },
                   'text13':{
                            'en':'<span style="font-size:12px;color:blue;"><b>The following information concern a crawl made in a %s version of the page</b></span><br>',
                            'pt':'<span style="font-size:12px;color:blue;"><b>As informações seguintes se referem a um rastreamento da página feito em uma versão %s</b></span><br>',
                           },
                   'text14':{
                            'en':'This url is always showing Status Code since the tracking beginning<br><br>',
                            'pt':'A url segue apresentando sempre Status Code desde o começo das medições<br><br>',
                           },
                   'text15':{
                            'en':'Datetime',
                            'pt':'Hora do Dia',
                           },
                   'text16':{
                            'en':'Changes',
                            'pt':'Mudanças',
                           },
                   'text17':{
                            'en':'Checkout the summary of the changes detected in the followed urls in the last 24 hours. Please, know that not every tag may be included in this summary.<br>',
                            'pt':'Verifique abaixo o resumo das mudanças detectadas nas urls monitoradas nas últimas 24 horas. Saiba que nem todas as tags podem ser incluídas nesse resumo.<br>',
                           },
                    }
                
dict_emails = {"Desktop Javascript Rendered": '',
                       "Desktop Not Rendered": '',
                       "Mobile Javascript Rendered": '',
                       "Mobile Not Rendered": '',
            }

file_emailtext = ''
details_text = ''
config_dict = yaml.load(email_to_send[table_name])

for url_id in url_ids:
    check_aggregation = config_dict['aggregation']
    analyzing_tags = config_dict['Check']
    cursor.execute("select template from monitoring_links where id = %s;" %url_id)
    template = cursor.fetchall()[0]['template']
    if template == None:
        template = ''
    if check_aggregation == 'hour':
        #gets the changes in the last 2 entries
        url_dict = {}
        if url_id not in alerts_summary:
            alerts_summary[url_id] = []

        rendering_types = []
        if 'DR' in config_dict[url_id]:
            rendering_types.append("Desktop Javascript Rendered")
        if 'DN' in config_dict[url_id]:
            rendering_types.append("Desktop Not Rendered")
        if 'MR' in config_dict[url_id]:
            rendering_types.append("Mobile Javascript Rendered")
        if 'MN' in config_dict[url_id]:
            rendering_types.append("Mobile Not Rendered")
        
        if rendering_types == []:
            logging.error("There isn't any configured rendering type for the url id %s in the email id %s" %(url_id, email_id))
            continue

        for rendering_type in rendering_types:
            url_skip = False        
            cursor.execute('select url,datetime,status,nchanges from seo_monitoring where (url_id, type) = (%s, %s) order by datetime desc limit 0,2;', [url_id, rendering_type])
            #gets last date values
            results = cursor.fetchall()
            if results == ():
                logging.info("No data present for url_id %s on %s..." %(url_id, rendering_type))
                continue
            siteurl = results[0]['url']
            logging.info("Analyzing %s on %s..." %(siteurl, rendering_type))
            try:
                current_hour = results[0]['datetime']
                last_hour = results[1]['datetime']
            except:
                logging.info("No dates to compare for %s on %s. Proceding to next url..." %(siteurl, rendering_type))
                continue

            # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
            cursor.execute("select seo_crawl from alerts_analysis_history where url_id = '%s';" %url_id)
            last_alert_date = cursor.fetchall()
            if last_alert_date != ():
                last_alert_date = last_alert_date[0]['seo_crawl']         #gets the last date from the alerts sent in past
                if last_alert_date != None:
                    last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
                    try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                        email_alert_id = last_alert_date[email_group_id].split('|')[0]
                        last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                        if last_analyzed_date == str(current_hour):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                            cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                            sent_date = cursor.fetchall()
                            if sent_date != ():
                                sent_date = sent_date[0]['sent_date']
                                logging.info("There is already an email alert sent to %s about SEO data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour, sent_date))
                                continue
                            else:
                                logging.info("There is already an email alert sent to %s about SEO data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour))
                                continue
                    except:
                        pass

            #if there are no changes proceeds to next url right away
            nchanges = results[0]['nchanges']
            status = str(results[0]['status'])
            last_status = str(results[1]['status'])
            date1 = results[0]['datetime']
            if int(status) == 400 or int(status) == 403 or int(last_status) == 400 or int(last_status) == 403:
                logging.info("ERROR - Emails won\'t be sent concerning 400 and 403 status code because it implies the data collection had an error on Cerebro side!")
                continue
            if nchanges == 0 and int(status) == 200:
                continue
            elif nchanges == 0 and int(status) != 200:
                cursor.execute("select status from seo_monitoring where (url_id, type) = (%s, '%s') and datetime = '%s';" %(url_id, rendering_type, current_hour))
                currentstatus = cursor.fetchall()[0]['status']
                #type_alert = ['status', rendering_type, 'hour_check', False]

                # ------------------------------- AVOIDING REPETITIVE STATUS ALERTS -----------------------------------
                # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 1 day
                cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, date_minus_1))
                last_emails_content = cursor.fetchall()

                var_email = avoid_same_content(last_emails_content, 'status')
                if var_email == True:                       
                    cursor.execute('select datetime from seo_monitoring where (url_id, type, nchanges, changes) = (%s, %s, 1, "status") order by datetime desc limit 1;', [url_id, rendering_type])
                    past_results = cursor.fetchall()
                    if past_results == ():
                        continue
                        if file_emailtext == '':
                            file_emailtext = dict_texts['text1'][language] %current_hour
                            dict_emails[rendering_type] += dict_texts['text14'][language]
                    else:
                        if file_emailtext == '':
                            file_emailtext = dict_texts['text1'][language] %current_hour
                        last_hour = past_results[0]['datetime']
                        dict_emails[rendering_type] += dict_texts['text2'][language] %(siteurl, siteurl, last_hour, current_hour)
                        dict_emails[rendering_type] += dict_texts['text3'][language] %currentstatus
                    alerts_summary[url_id].append('status')

            else:
                cursor.execute("select datetime from seo_monitoring where (url_id, type, status) = (%s, '%s', 200) order by datetime desc limit 2;" %(url_id, rendering_type))
                last_compare_hour = cursor.fetchall()[1]['datetime']
                cursor.execute("select datetime from seo_monitoring where (url_id, type) = (%s, '%s') order by datetime desc limit 2;" %(url_id, rendering_type))
                last_compare_hour_status = cursor.fetchall()[1]['datetime']
                
                cursor.execute("select changes from seo_monitoring where (url_id, type) = (%s, '%s') order by datetime desc limit 1;" %(url_id, rendering_type))
                alertchanges = cursor.fetchall()[0]['changes'].split(',')
                alertchanges = [x for x in analyzing_tags if x in alertchanges]

                #check if all of the itens of "alertchanges" are inside "emailcheck". If so, it doens't send email, if there are different terms, it sends
                emailcheck = all(n in ['html'] for n in alertchanges)

                if emailcheck == False:
                    if file_emailtext == '':
                        file_emailtext = dict_texts['text1'][language] %current_hour
                    if dict_details['semantic'][language][rendering_type] not in dict_emails[rendering_type]:
                        dict_emails[rendering_type] += dict_texts['text13'][language] %dict_details['semantic'][language][rendering_type]
                    dict_emails[rendering_type] += dict_texts['text2'][language] %(siteurl, siteurl, last_hour, current_hour)

                    for change in alertchanges:
                        if change in dict_details['semantic'][language].keys() and dict_details['semantic'][language][change] not in details_text:
                            details_text += dict_details['semantic'][language][change] + '<br>'
                        
                    for change in alertchanges:
                        if template != '':
                            type_alert = [change, rendering_type + " " + template, 'hour_check', False]
                        else:
                            type_alert = [change, rendering_type, 'hour_check', False]
                        if change not in ['html','h2','h3','h4','h5','h6','nh2','nh3','nh4','nh5','nh6']:  #writes the changes in email, but not the ones on the pointed list
                            if change == 'status':
                                cursor.execute("select %s from seo_monitoring where (url_id, type) = (%s, '%s') and datetime = '%s';" %(change, url_id, rendering_type, last_compare_hour_status))
                            else:
                                cursor.execute("select %s from seo_monitoring where (url_id, type) = (%s, '%s') and datetime = '%s';" %(change, url_id, rendering_type, last_compare_hour))
                            lastvalue = cursor.fetchall()[0][change]
                            cursor.execute("select %s from seo_monitoring where (url_id, type) = (%s, '%s') and datetime = '%s';" %(change, url_id, rendering_type, current_hour))
                            currentvalue = cursor.fetchall()[0][change]

                            #gets difference between strings using function to highlight them
                            if currentvalue != None and lastvalue != None and type(currentvalue) == str and type(lastvalue) == str:
                                currentvalue, lastvalue = git_strings(currentvalue, lastvalue)
                           
                            # if values don't exist they will be printed in red as 'Not Present'
                            if currentvalue == None:
                                currentvalue = dict_texts['text4'][language]
                            if lastvalue == None:
                                lastvalue = dict_texts['text4'][language]

                            if change in ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:  #writes the changes in email, but doesn't show the values
                                nchange = 'n' + change
                                cursor.execute("select %s from seo_monitoring where (url_id, type) = (%s, '%s') and datetime = '%s';" %(nchange, url_id, rendering_type, last_compare_hour))
                                nlastvalue = cursor.fetchall()[0][nchange]
                                nlastvalue = 0 if nlastvalue is None else int(nlastvalue)
                                cursor.execute("select %s from seo_monitoring where (url_id, type) = (%s, '%s') and datetime = '%s';" %(nchange, url_id, rendering_type, current_hour))
                                ncurrentvalue = cursor.fetchall()[0][nchange]
                                ncurrentvalue = 0 if ncurrentvalue is None else int(ncurrentvalue)
                           
                                if ncurrentvalue == 0 and nlastvalue <= 5:
                                   dict_emails[rendering_type] += dict_texts['text5'][language] %(dict_changes['semantic'][language][change], lastvalue)
                                elif ncurrentvalue == 0 and nlastvalue > 5:
                                   dict_emails[rendering_type] += dict_texts['text6'][language] %(dict_changes['semantic'][language][change], nlastvalue)                         
                                elif ncurrentvalue <= 5 and nlastvalue <= 5:
                                    dict_emails[rendering_type] += dict_texts['text7'][language] %(dict_changes['semantic'][language][change], lastvalue, currentvalue)
                                elif ncurrentvalue <= 5 and nlastvalue > 5:
                                    dict_emails[rendering_type] += dict_texts['text8'][language] %(dict_changes['semantic'][language][change], ncurrentvalue, currentvalue)
                                elif ncurrentvalue > 5 and nlastvalue <= 5:
                                    dict_emails[rendering_type] += dict_texts['text9'][language] %(dict_changes['semantic'][language][change], lastvalue, ncurrentvalue)
                                elif ncurrentvalue > 5 and nlastvalue > 5 and ncurrentvalue != nlastvalue:
                                    dict_emails[rendering_type] += dict_texts['text10'][language] %(dict_changes['semantic'][language][change], nlastvalue, ncurrentvalue)
                                elif ncurrentvalue > 5 and nlastvalue > 5 and ncurrentvalue == nlastvalue:
                                    dict_emails[rendering_type] += dict_texts['text11'][language] %(dict_changes['semantic'][language][change], nlastvalue)
                            elif type(currentvalue) == str and type(lastvalue) == str:
                               dict_emails[rendering_type] += dict_texts['text7'][language] %(dict_changes['semantic'][language][change], lastvalue, currentvalue)
                            else:
                               dict_emails[rendering_type] += dict_texts['text12'][language] %(dict_changes['semantic'][language][change], lastvalue, currentvalue)
                            alerts_summary[url_id].append(type_alert)
                    if url_skip == True:
                        continue
                    dict_emails[rendering_type] += '<br>'

        if dict_emails[rendering_type] != '':
            dict_urls[url_id] = str(date1)
            analyzed_urls[execute_file[2]] = dict_urls 

    elif check_aggregation == 'day' and time_check == 'hour':
        logging.info("Url %s: The consolidated day analysis will be made onlyat %s for email group %s" %(url_id, send_hour, email_group_id))

    elif check_aggregation == 'day' and time_check == 'day':
        #gets last 24 entries and send every change found in a table
        url_dict = {}
        if url_id not in alerts_summary:
            alerts_summary[url_id] = []

        rendering_types = []
        if 'DR' in config_dict[url_id]:
            rendering_types.append("Desktop Javascript Rendered")
        if 'DN' in config_dict[url_id]:
            rendering_types.append("Desktop Not Rendered")
        if 'MR' in config_dict[url_id]:
            rendering_types.append("Mobile Javascript Rendered")
        if 'MN' in config_dict[url_id]:
            rendering_types.append("Mobile Not Rendered")
        analyzing_tags = config_dict['Check']

        if rendering_types == []:
            logging.error("There isn't any configured rendering type for the url id %s in the email id %s" %(url_id, email_id))
            continue

        for rendering_type in rendering_types:
            cursor.execute("select url,datetime from seo_monitoring where (url_id, type) = (%s, %s) order by id desc limit 1;", [url_id, rendering_type])
            results = cursor.fetchall()
            if results == ():
                logging.info("No data present for url_id %s on %s..." %(url_id, rendering_type))
                continue
            else:
                siteurl = results[0]['url']
                last_day_end = results[0]['datetime']
                current_hour = str(last_day_end.date())
                last_day_begin = last_day_end - timedelta(days=23/24)
            
            cursor.execute("select url,datetime,status,nchanges,changes from seo_monitoring where (url_id, type) = (%s, %s) and datetime between %s and %s order by id desc limit 24;", [url_id, rendering_type, last_day_begin, last_day_end])
            #gets last date values
            results = cursor.fetchall()            
            if len(results) < 2:
                logging.info("No data present for url_id %s on %s..." %(url_id, rendering_type))
                continue
            date1 = results[0]['datetime']
            logging.info("Analyzing %s on %s..." %(siteurl, rendering_type))

            # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
            cursor.execute("select seo_crawl from alerts_analysis_history where url_id = '%s';" %url_id)
            last_alert_date = cursor.fetchall()
            if last_alert_date != ():
                last_alert_date = last_alert_date[0]['seo_crawl']         #gets the last date from the alerts sent in past
                if last_alert_date != None:
                    last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
                    try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                        email_alert_id = last_alert_date[email_group_id].split('|')[0]
                        last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                        if last_analyzed_date == str(current_hour):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                            cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                            sent_date = cursor.fetchall()[0]['sent_date']
                            logging.info("There is already an email alert sent to %s about SEO data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour, sent_date))
                            continue
                    except:
                        pass

        table_header = '<tr><th style="table-layout: fixed;color: white; background-color: black;text-align:center;border: 1px solid black;padding-left:30px;padding-right:30px">' + dict_texts['text15'][language] + '</th>'
        table_header += '<th style="table-layout: fixed;color: white;background-color: black;text-align:center;border: 1px solid black;">' + dict_texts['text16'][language] + '</th></tr>'
        table_rows = ''

        for result in results[:-1]: #decresing order of data (excludes last term because it can't be compared to the previous one
            n_changes = result['nchanges']
            status = str(result['status'])
            if n_changes == 0 and int(status) == 200:
                continue
            else:
                try:
                    changes = result['changes'].split(',')
                except:
                    changes = ['status']
                occurence_time = result['datetime']
                alert_changes = []  
                for change in changes:
                    logging.info('Change found on %s at %s' %(change, occurence_time))
                    if change not in analyzing_tags:
                        continue
                    else:
                        if dict_changes['semantic'][language][change] not in alert_changes:
                            if change == 'status':
                                alert_changes.append('<b>' + dict_changes['semantic'][language][change] + ' ' + status + '</b>')
                            else:
                                alert_changes.append(dict_changes['semantic'][language][change])
                        if template != '':
                            type_alert = [change, rendering_type + " " + template, 'day_check', False]
                        else:
                            type_alert = [change, rendering_type, 'day_check', False]
                        if type_alert not in alerts_summary[url_id]:
                            alerts_summary[url_id].append(type_alert)

                        if change in dict_details['semantic'][language].keys() and dict_details['semantic'][language][change] not in details_text:
                            details_text += dict_details['semantic'][language][change] + '<br>'

                if alert_changes != []:                   
                    table_rows += '<tr><td style="table-layout: fixed;text-align:center;border: 1px solid black;">' + str(occurence_time) + '</td>'
                    table_rows += '<td style="table-layout: fixed;text-align:center;border: 1px solid black;padding-left:10px;padding-right:10px">' + ' | '.join(alert_changes) + '</td></tr>'
                else:
                    continue
        table_html = '<table style="table-layout: fixed; border: 1px solid black;border-collapse:collapse;font-size:11px;white-space:nowrap;">' + table_header + table_rows + '</table>'

        if file_emailtext == '' and alerts_summary[url_id] != []:
            file_emailtext = dict_texts['text1'][language] %current_hour

        if alerts_summary[url_id] != [] and dict_texts['text17'][language] not in dict_emails[rendering_type]:
            dict_emails[rendering_type] += dict_texts['text17'][language]

        if alerts_summary[url_id] != []:
            if dict_details['semantic'][language][rendering_type] not in dict_emails[rendering_type]:
                dict_emails[rendering_type] += dict_texts['text13'][language] %dict_details['semantic'][language][rendering_type]
            dict_emails[rendering_type] += '<br><b><a href="%s">%s</a></b><br>' %(siteurl, siteurl)
            dict_emails[rendering_type] += table_html

        if dict_emails[rendering_type] != '':
            dict_urls[url_id] = str(date1)
            analyzed_urls[execute_file[2]] = dict_urls 

for key in dict_emails.keys():
    if dict_emails[key] != '':
        file_emailtext += dict_emails[key]

if details_text != '':
    file_emailtext += '<b><span style="font-size:15px;color:blue;"><br>' + dict_details['semantic'][language]['summary'] + '</span></b><br>' + details_text

#email sending part
if file_emailtext != '':
    title = title_to_email_section('Simplex Crawl','change')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
