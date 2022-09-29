#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- (GA SEO)/GSC DATA ALERTS --------------------------------
table_name, script_type = 'ga_gsc_seo_ratio', 'alerts'
url_ids = get_url_ids('gsc','Google Search Console or Analytics',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

dict_colunas = { 
    #first subdivision
    'semantic':{
            'en':{'ga_gsc_ratio':'GA SEO Visits and GSC Clicks Ratio', },
            'pt':{'ga_gsc_ratio':'Razão entre Visitas SEO do GA e Cliques do GSC',},
            },
    'outlier':{'ga_gsc_ratio':1.8,},              
    'format':{'ga_gsc_ratio':float,}
    }
    
file_emailtext = ''

for url_id in url_ids:
    url_dict = {}
    urltext = []
    urltrends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select * from ga_gsc_seo_ratio where url_id = '%s' order by date desc limit 0,10;" %url_id)
    results = cursor.fetchall()
    if len(results) == 0:
        continue
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    logging.info("Analyzing %s" %siteurl)
    coluna = 'ga_gsc_ratio'
    color = 'red'
    traffic_type = ''
    maxdate = 0
    var = []
    dates = []
    own_condition = 1

    #joins each day data in a list to apply statistics
    format_type = float
    for result in results:
        var[:0] = [format_type(result[coluna])]
        dates[:0] = [str(result['date'])]
    try:
        #uses trimmean to get expected value
        trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_colunas['outlier'][coluna], format_type)
        x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
    except:
        continue

        #gets last day value to compare deviation from expected value
    try:
        var1 = format_type(results[0]['ga_gsc_ratio'])
        date1 = results[0]['date']
    except:
        logging.info("No data available for %s in %s. Proceding to next url..." %(siteurl, date1))
        continue

    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select ga_gsc_seo_ratio from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['ga_gsc_seo_ratio']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about GA/GSC SEO Ratio data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                    else:
                        logging.info("There is already an email alert sent to %s about GA/GSC SEO Ratio data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                        continue
            except:
                pass
            
    # ------------------------------ RUNNING THE ANALYSIS ----------------------------------------
    #absdelta and percdelta are the anomaly detectors
    varabsdelta = var1 - trim_var
    try:
        varpercdelta = (var1/trim_var)-1
    except:
        varpercdelta = float("inf")
    #if the test score changes more than 5 points it is considered and anomaly
    if var1 < lowerlimit or var1 > upperlimit:
         type_alert = [coluna, traffic_type, '', False]
         logging.info("Outlier found: %s" %type_alert)
         #classifying the outlier found             
         if var1 < crit_lowerlimit or var1 > crit_upperlimit and lowerlimit != upperlimit:
             type_alert[3] = True
         if varpercdelta > 0:
             type_alert[2] += ' up'
             sign = '+'
         else:
             type_alert[2] += ' down'
             sign = '-'

         outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, dates, trim_var, upperlimit, lowerlimit, 'days', n)
         text = outlier_phrase(dict_colunas['semantic'][language][coluna], type_alert, traffic_type, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, 'dimension_off', 'yes', outliers_over_time)
         text += '<br><img src="cid:Graph%s.png"><br>' %n
         file_emailtext = text

         alerts_summary[url_id].append(type_alert)
         n += 1

if file_emailtext != '':
    dict_urls[url_id] = str(date1)
    analyzed_urls[execute_file[2]] = dict_urls 
    file_emailtext = '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl) + file_emailtext
    
# ------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Analytics - Search Console','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
