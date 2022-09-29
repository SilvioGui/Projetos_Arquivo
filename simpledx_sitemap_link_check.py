#!/usr/bin/env python
# -*- coding: utf-8 -*-
#imports all the libraries from calling script
import  MySQLdb
from warnings import filterwarnings
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from lib import auth, logger, models
import logging
from datetime import datetime, timedelta

date = str(datetime.now().date())
subject = 'Sitemap Links %s' %date
sending_dict = {}
sending_dict[subject] = {'report':['','','','']}

filterwarnings('ignore', category = MySQLdb.Warning)

#Database credentials
db = auth.getConnection()
cursor = db.cursor(MySQLdb.cursors.DictCursor)

# Determines Time and Day Running
# -------------------------- SEO TAGS ANALYSIS --------------------------------
#leroy fr, leroy it, cobasi, mobly, vivara
simpledx_ids = [#['1','/sitemap-b.html'],
                ['40','/plan-de-site-recherche.html'],
                ['73','/sitemap-p-i.html'],
                ['77','/sitemap-c.html'],
                #['186','/sitemap-sp.html'],
                #['198','/sitemap.sdx'],
                ['234','/sitemap.sdex'],
                ['281','/sitemap-v.html'],
                 ]

emailtext = ''
exec(open('cerebro_chat_options.py', encoding='utf-8').read())
name_greetings = ''
email_issues = 'just_report'
current_send_hour = '00:00'
language = 'pt'
emailtext = ''
toaddr = 'marcos@simplexanalytics.com.br,jonas@simplexanalytics.com.br,florian@simplexanalytics.com.br'
cc = None
bcc = None

for simpledx_id in simpledx_ids:
    url_id = simpledx_id[0]
    sitemap_link = simpledx_id[1]
    cursor.execute('select url,datetime,html from seo_monitoring where (url_id, type) = (%s, "Desktop Javascript Rendered") and html is not null order by datetime desc limit 0,1;', [url_id])
    #gets last date values
    results = cursor.fetchall()
    if results == ():
        logging.info("No data present for url_id %s..." %url_id)
        continue
    else:
        siteurl = results[0]['url']
        dia = str(results[0]['datetime'])
        html = results[0]['html']
    logging.info("Analyzing %s..." %siteurl)
    if sitemap_link in html:
        logging.info("OK: Sitemap link is present in the page %s" %siteurl)
    else:
        logging.error('ERRO: O link do Sitemap SimpleDX %s não está presente na pagina em %s' %(siteurl, dia))
        emailtext += '<br>ERRO: O link do Sitemap SimpleDX %s não está presente na pagina em %s' %(siteurl, dia)

sending_dict[subject]['report'][2] = emailtext
sending_keys = list(sending_dict.keys())
#email sending part
if emailtext != '':
    logging.info("Sending email...")
    exec(open("simplex_send_simple_email.py").read())
    logging.info("Successfully sent")
else:
    logging.info("No data sent to email")
