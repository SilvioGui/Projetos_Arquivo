#imports all the libraries from calling script
from __main__ import *

table_name, script_type = 'keywords', 'reports'

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

dic_texts = {'text1':{
                     'en':'<span style="font-size:20px"><b>Simplex Analytics Internal vs External Keyword Report</b></span><br>',
                     'pt':'<span style="font-size:20px"><b>Simplex Analytics Relatório de Keywords Internas vs Externas</b></span><br>',
                     },
             'text2':{
                     'en':'<b><i>Search Console Keywords Impressions in %s </b></i>',
                     'pt':'<b><i>Impressões de Keywords do Search Console em %s </b></i>',
                     },
             'text3':{
                     'en':'<b><i>Internal Keywords Searches Number in %s </i></b>',
                     'pt':'<b><i>Número de Buscas de Keywords Internas em %s </i></b>',
                     },
             'text4':{
                     'en':'Not available',
                     'pt':'Não disponível',
                     },
             'text5':{
                     'en':'The keywords highlighted in <span style="color:green"><b>green</b></span> are present in both lists below. \
In case a keyword is not highlighted, it is because it appears in only one list.<br>',
                     'pt':'As palavras destacadas em <span style="color:green"><b>verde</b></span> estão presentes em ambas as listas abaixo. \
Caso a palavra não tenha destaque, é porque ela aparece em apenas uma das listas.<br>',
                     },
    }

table_name, script_type = 'keywords', 'reports'
keywords_info = email_to_send['keywords']
if keywords_info == None:
    raise RuntimeError('Report not enabled')
file_emailtext = ''

keywords_info = yaml.load(keywords_info)
for key in keywords_info.keys():
    url_id = str(key)
    days_interval = int(keywords_info[key])

days_interval = 1
date_ga_start = str(datetime.now(pytz.timezone(timezone)).date()- timedelta(days=(days_interval)))
date_ga_end = str(datetime.now(pytz.timezone(timezone)).date()- timedelta(days=1))
date_gsc_start = str(datetime.now(pytz.timezone(timezone)).date()- timedelta(days=(2+days_interval)))
date_gsc_end = str(datetime.now(pytz.timezone(timezone)).date()- timedelta(days=3))
date1 = str(datetime.now(pytz.timezone(timezone)).date())

if days_interval == 1:
    ga_dates = str(date_ga_start)
    gsc_dates = str(date_gsc_start)
else:
    ga_dates = str(date_ga_start) + ' - ' + str(date_ga_end)
    gsc_dates = str(date_gsc_start) + ' - ' + str(date_gsc_end)
                    
# ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
skip = False
cursor.execute("select keywords from reports_analysis_history where url_id = '%s';" %url_id)
last_alert_date = cursor.fetchall()
if last_alert_date != ():
    last_alert_date = last_alert_date[0]['keywords']         #gets the last date from the alerts sent in past
    if last_alert_date != None:
        last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
        try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
            email_alert_id = last_alert_date[email_id].split(':')[0]
            last_analyzed_date = last_alert_date[email_id].split(':')[1]
            if last_analyzed_date == str(date1):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                sent_date = cursor.fetchall()[0]['sent_date']
                skip = True
        except:
            pass

if skip == True:
    logging.info("There is already an email alert sent to %s about Internal and External Searches collected in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, last_analyzed_date, sent_date))
    raise RuntimeError

file_emailtext = ''
analyzed_urls = {}

n = 1
attachment = []

# -------------------------- GOOGLE ANALYTICS AND SEARCH CONSOLE KEYWORDS ALERTS --------------------------------
logging.info("Checking urls data covered by email group id %s" %email_group_id)

# ANALYTICS BLOCK ----------------------
cursor.execute("select * from monitoring_links where ga is not null and active = 1 and id = %s;" %url_id)
website = cursor.fetchall()

if website == ():
    logging.info("There is no Google Analytics website keywords tracking set for the %s" %toaddr)
    ga_email = False
else:
    url = website[0]['url']
    url_id = website[0]['id']
    ga_view = yaml.load(website[0]['ga'])['view']
    ga_ua = yaml.load(website[0]['ga'])['UA']

    logging.info("Extracting Google Analytics keywords for %s in the last %s days..." %(url, days_interval))
    cmdoutput = subprocess.getoutput("python3.6 GA_API_SEARCHES.py ga:{} {} {} {} {}".format(ga_view, url, date_ga_start, date_ga_end, ga_ua))   #get cmd output as a string
    if "there was an API error" not in cmdoutput:
        ga_email = True
        analyze_output_ga = cmdoutput.split('\n')

        compare_output_ga = []
        for line in analyze_output_ga:
            keyword = line.split('\t')[0]
            keyword = keyword.replace('-',' ')
            compare_output_ga.append(keyword.lower())
    else:
        logging.info("There is no keyword data available for Google Analytics on %s in the interval of % days" %(url, days_interval))
        ga_email = False
    if len(compare_output_ga) < 5:
        logging.info("There is no keyword data available for Google Analytics on %s in the interval of % days" %(url, days_interval))
        ga_email = False

# SEARCH CONSOLE BLOCK ----------------------
cursor.execute("select * from monitoring_links where gsc is not null and active = 1 and id = %s;" %url_id)
website = cursor.fetchall()

if website == ():
    logging.info("There is no Google Search Console website keywords tracking set for the %s" %toaddr)
    gsc_email = False
else:
    url = website[0]['url']
    url_id = website[0]['id']
    branded = website[0]['branded_term']    

    logging.info("Extracting Google Search Console keywords for %s in the last %s days..." %(url, days_interval))
    cmdoutput = subprocess.getoutput("python3.6 GSC_API_KEYWORDS.py %s %s %s %s" %(url, date_gsc_start, date_gsc_end, branded))   #get cmd output as a string
    if "there was an API error" not in cmdoutput:
        gsc_email = True
        analyze_output_gsc = cmdoutput.split('\n')

        compare_output_gsc = []
        for line in analyze_output_gsc:
            keyword = line.split('\t')[0]
            keyword = keyword.replace('-',' ')
            compare_output_gsc.append(keyword.lower())
    else:
        logging.info("There is no keyword data available for Google Search Console on %s in the interval of % days" %(url, days_interval))
        gsc_email = False
    if len(compare_output_gsc) < 5:
        logging.info("There is no keyword data available for Google Search Console on %s in the interval of % days" %(url, days_interval))
        ga_email = False

# EMAIL CONSTRUCTING BLOCK --------------------
# There are 3 cases of construction, when date is available only on GA, only on GSC or in both of them
if ga_email == True and gsc_email == True:
    keywords_ga_html = []
    keywords_gsc_html = []
    for line in analyze_output_ga:
        if line == analyze_output_ga[0]:
            size = len(str(line.split('\t')[1]))
        keyword = line.split('\t')[0].lower().replace('-',' ')
        searches = line.split('\t')[1]
        if keyword in compare_output_gsc:
            keywords_ga_html.append('<span style="color:green"><b>'+searches+'&emsp;&emsp;&emsp;'+keyword+'</b></span><br>')
        else:
            keywords_ga_html.append(searches+'&emsp;&emsp;&emsp;'+keyword+'<br>')

    for line in analyze_output_gsc:
        if line == analyze_output_gsc[0]:
            size = len(str(line.split('\t')[1]))
        keyword = line.split('\t')[0].lower().replace('-',' ')
        impressions = line.split('\t')[1]
        if keyword in compare_output_ga:
            keywords_gsc_html.append('<span style="color:green"><b>'+impressions+'&emsp;&emsp;&emsp;'+keyword+'</b></span><br>')
        else:
            keywords_gsc_html.append(impressions+'&emsp;&emsp;&emsp;'+keyword+'<br>')

    keywords_ga_html = "".join(keywords_ga_html)
    keywords_gsc_html = "".join(keywords_gsc_html)

    file_emailtext = dic_texts['text1'][language]
    file_emailtext += dic_texts['text5'][language]
    file_emailtext += '<br><div style="overflow:hidden;"><div style="width: 50%;float:left">'+dic_texts['text3'][language] %str(ga_dates)+'<br>'+keywords_ga_html+'</div>\
<div style="width: 50%; float:right">'+ dic_texts['text2'][language] %str(gsc_dates)+'<br>' +keywords_gsc_html+'</div></div>'

elif ga_email == True and gsc_email == False:
    keywords_ga_html = []
    for line in analyze_output_ga:
        keyword = line.split('\t')[0].lower().replace('-',' ')
        searches = line.split('\t')[1]
        keywords_ga_html.append(searches+'&emsp;&emsp;'+keyword+'<br>')
    keywords_ga_html = "".join(keywords_ga_html)
    keywords_gsc_html = dic_texts['text4'][language]

    file_emailtext = dic_texts['text1'][language]
    file_emailtext += '<br><div style="overflow:hidden;"><div style="width: 50%;float:left">'+dic_texts['text3'][language] %str(ga_dates)+'<br>'+keywords_ga_html+'</div>\
<div style="width: 50%; float:right">'+ dic_texts['text3'][language] %str(gsc_dates)+'<br>' +keywords_gsc_html+'</div></div>'

elif gsc_email == True and ga_email == False:
    keywords_gsc_html = []
    for line in analyze_output_gsc:
        keyword = line.split('\t')[0].lower().replace('-',' ')
        impressions = line.split('\t')[1]
        keywords_gsc_html.append(impressions+'&emsp;&emsp;'+keyword+'<br>')
    keywords_ga_html = dic_texts['text4'][language]
    keywords_gsc_html = "".join(keywords_gsc_html)

    file_emailtext = dic_texts['text1'][language]
    file_emailtext += '<br><div style="overflow:hidden;"><div style="width: 50%;float:left">'+dic_texts['text3'][language] %str(ga_dates)+'<br>'+keywords_ga_html+'</div>\
<div style="width: 50%; float:right">'+ dic_texts['text2'][language] %str(gsc_dates)+'<br>' +keywords_gsc_html+'</div></div>'

else:
    logging.error("There are no keywords available both in Google Analytics and Google Search Console for %s" %url)

if file_emailtext != '':
    # --------------------------------- EMAIL ALERTS HISTORY DATABASE MANIPULATION -----------------------------
    dict_urls[url_id] = str(date1)
    analyzed_urls[execute_file[2]] = dict_urls 
else:
    logging.info("No data sent to email")
