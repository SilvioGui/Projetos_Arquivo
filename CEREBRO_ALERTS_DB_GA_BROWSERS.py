#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
    
# -------------------------- GOOGLE ANALYTICS DATA ALERTS --------------------------------
table_name, script_type = 'ga_browsers', 'alerts'
url_ids = get_url_ids('ga','Google Analytics Browsers',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#set columns which should be analyzing comparing the last 10 days (in general, rates and percentual values)
lastdays = ['bounceRate', 'avgSessionDuration','avgTimeOnPage']
#set columns which should be analyzing comparing the last 10 similar weekdays (in general, absolute values metrics)
lastweekdays = ['bounceRate', 'avgSessionDuration','avgTimeOnPage','sessions','users','pageviews', 'newUsers', 'transactionRevenue','transactions','conversion']

#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection,
#3rd section to trend analysis correlation factor, 4th section for variable types
dict_colunas = { 
    #first subdivision
    'semantic':{
            'en':{
                'sessions':'Sessions',
                'pageviews':'Pageviews',
                'pageviewsPerSession':'Pageviews per Session',
                'bounceRate':'Bounce Rate',
                'users':'Users',
                'newUsers':'New Users',
                'avgTimeOnPage':'Average Time on Page',
                'avgSessionDuration':'Average Session Duration',
                'transactionRevenue':'Revenue',
                'transactions':'Transactions',
                'conversion':'Conversion',
                },
            'pt':{
                'sessions':'Sessões',
                'pageviews':'Pageviews',
                'pageviewsPerSession':'Pageviews por Session',
                'bounceRate':'Bounce Rate',
                'users':'Usuários',
                'newUsers':'Novos Usuários',
                'avgTimeOnPage':'Tempo Médio na Pág.',
                'avgSessionDuration':'Duração Média da Sessão',
                'transactionRevenue':'Receita',
                'transactions':'Pedidos',
                'conversion':'Conversão',
                },
            },
    #second subdivision
    'outlier':{
                'sessions':2.25,
                'pageviews':2.25,
                'pageviewsPerSession':2.75,
                'bounceRate':2.25,
                'users':2.75,
                'newUsers':2.75,
                'avgTimeOnPage': 3.25,
                'avgSessionDuration':3.25,
                'transactionRevenue':2.75,
                'transactions':2.25,
                'conversion':2.25,
                },              
    #third subdivision
    'correlation':{
                'sessions':0.91,
                'pageviews':0.91,
                'pageviewsPerSession':0.95,
                'bounceRate':0.91,
                'users':0.91,
                'newUsers':0.91,
                'avgTimeOnPage':0.925,
                'avgSessionDuration':0.925,
                'transactionRevenue':0.925,
                'transactions':0.91,
                'conversion':0.91,
                },
    #fourth subdivision
    'format':{
                'sessions':int,
                'pageviews':int,
                'pageviewsPerSession':float,
                'bounceRate':float,
                'users':int,
                'newUsers':int,
                'avgTimeOnPage':float,
                'avgSessionDuration':float,
                'transactionRevenue':float,
                'transactions':int,
                'conversion':float,
                }
    }

config_dict = yaml.load(email_to_send['ga'])
file_emailtext = ''

for url_id in url_ids:
    if config_dict[url_id]['browsers'] == [] or config_dict[url_id]['metrics'] == []:
        logging.info('Browsers not checked for url_id %s' %url_id)
        continue

    #get all the columns to be analyzed for the corresponding url
    colunas = config_dict[url_id]['metrics']
    traffic_types = config_dict[url_id]['browsers']
    ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit = 0, 0, 0, 0, 0

    if 'aggregation' in config_dict[url_id]:
        aggregation = config_dict[url_id]['aggregation']
    else:
        aggregation = 'days'

    cursor.execute("select weekday(max(date)) from ga_browsers where url_id = %s;" %url_id)
    maxdate = cursor.fetchall()[0]['weekday(max(date))']

    url_break = False
    url_dict = {}
    url_trends = []
    url_outliers = []
    url_prior_outliers = []
    url_prior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []
    
    cursor.execute("select url from ga_browsers where url_id = %s order by date desc limit 1;" , [url_id])
    results = cursor.fetchall()
    if len(results) == 0:
        logging.info('{}: there are no rows in ga_browsers table for url_id = {}'.format(__file__, url_id))
        continue
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    logging.info("Analyzing %s" %siteurl)
    own_condition = 1

    for traffic_type in traffic_types:
        if url_break == True:
            break
        traffic_type_sessions = 0
        #get values for each metric analyzed
        for coluna in colunas:
            if aggregation == 'weeks':
                #gets last 10 weeks, the sum of each them, entries for the specified site, 9 for statistic analysis and 1 to be checked
                today = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                cursor.execute("set @today = '%s',@url_id = '%s', @browser = '%s';" %(today, url_id, traffic_type))
                if coluna in lastdays:
                    if coluna == 'bounceRate' or coluna == 'avgSessionDuration':
                        sql = "select 1 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 0 day) and date>=date_sub(@today, interval 7 day) and (url_id, browser) = (@url_id, @browser) union select 2 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 7 day) and date>=date_sub(@today, interval 14 day) and (url_id, browser) = (@url_id, @browser) union select 3 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 14 day) and date>=date_sub(@today, interval 21 day) and (url_id, browser) = (@url_id, @browser) union select 4 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 21 day) and date>=date_sub(@today, interval 28 day) and (url_id, browser) = (@url_id, @browser) union select 5 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 28 day) and date>=date_sub(@today, interval 35 day) and (url_id, browser) = (@url_id, @browser) union select 6 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 35 day) and date>=date_sub(@today, interval 42 day) and (url_id, browser) = (@url_id, @browser) union select 7 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 42 day) and date>=date_sub(@today, interval 49 day) and (url_id, browser) = (@url_id, @browser) union select 8 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 49 day) and date>=date_sub(@today, interval 56 day) and (url_id, browser) = (@url_id, @browser) union select 9 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 56 day) and date>=date_sub(@today, interval 63 day) and (url_id, browser) = (@url_id, @browser) union select 10 as week, sum(" + coluna + "*sessions)/sum(sessions) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 63 day) and date>=date_sub(@today, interval 70 day) and (url_id, browser) = (@url_id, @browser);"
                    elif coluna == 'avgTimeOnPage':
                        sql = "select 1 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 0 day) and date>=date_sub(@today, interval 7 day) and (url_id, browser) = (@url_id, @browser) union select 2 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 7 day) and date>=date_sub(@today, interval 14 day) and (url_id, browser) = (@url_id, @browser) union select 3 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 14 day) and date>=date_sub(@today, interval 21 day) and (url_id, browser) = (@url_id, @browser) union select 4 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 21 day) and date>=date_sub(@today, interval 28 day) and (url_id, browser) = (@url_id, @browser) union select 5 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 28 day) and date>=date_sub(@today, interval 35 day) and (url_id, browser) = (@url_id, @browser) union select 6 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 35 day) and date>=date_sub(@today, interval 42 day) and (url_id, browser) = (@url_id, @browser) union select 7 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 42 day) and date>=date_sub(@today, interval 49 day) and (url_id, browser) = (@url_id, @browser) union select 8 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 49 day) and date>=date_sub(@today, interval 56 day) and (url_id, browser) = (@url_id, @browser) union select 9 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 56 day) and date>=date_sub(@today, interval 63 day) and (url_id, browser) = (@url_id, @browser) union select 10 as week, sum(" + coluna + "*pageviews)/sum(pageviews) as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 63 day) and date>=date_sub(@today, interval 70 day) and (url_id, browser) = (@url_id, @browser);"
                    else:
                        sql = "select 1 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 0 day) and date>=date_sub(@today, interval 7 day) and (url_id, browser) = (@url_id, @browser) union select 2 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 7 day) and date>=date_sub(@today, interval 14 day) and (url_id, browser) = (@url_id, @browser) union select 3 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 14 day) and date>=date_sub(@today, interval 21 day) and (url_id, browser) = (@url_id, @browser) union select 4 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 21 day) and date>=date_sub(@today, interval 28 day) and (url_id, browser) = (@url_id, @browser) union select 5 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 28 day) and date>=date_sub(@today, interval 35 day) and (url_id, browser) = (@url_id, @browser) union select 6 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 35 day) and date>=date_sub(@today, interval 42 day) and (url_id, browser) = (@url_id, @browser) union select 7 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 42 day) and date>=date_sub(@today, interval 49 day) and (url_id, browser) = (@url_id, @browser) union select 8 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 49 day) and date>=date_sub(@today, interval 56 day) and (url_id, browser) = (@url_id, @browser) union select 9 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 56 day) and date>=date_sub(@today, interval 63 day) and (url_id, browser) = (@url_id, @browser) union select 10 as week, avg(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 63 day) and date>=date_sub(@today, interval 70 day) and (url_id, browser) = (@url_id, @browser);"
                else:
                    sql = "select 1 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 0 day) and date>=date_sub(@today, interval 7 day) and (url_id, browser) = (@url_id, @browser) union select 2 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 7 day) and date>=date_sub(@today, interval 14 day) and (url_id, browser) = (@url_id, @browser) union select 3 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 14 day) and date>=date_sub(@today, interval 21 day) and (url_id, browser) = (@url_id, @browser) union select 4 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 21 day) and date>=date_sub(@today, interval 28 day) and (url_id, browser) = (@url_id, @browser) union select 5 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 28 day) and date>=date_sub(@today, interval 35 day) and (url_id, browser) = (@url_id, @browser) union select 6 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 35 day) and date>=date_sub(@today, interval 42 day) and (url_id, browser) = (@url_id, @browser) union select 7 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 42 day) and date>=date_sub(@today, interval 49 day) and (url_id, browser) = (@url_id, @browser) union select 8 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 49 day) and date>=date_sub(@today, interval 56 day) and (url_id, browser) = (@url_id, @browser) union select 9 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 56 day) and date>=date_sub(@today, interval 63 day) and (url_id, browser) = (@url_id, @browser) union select 10 as week, sum(" + coluna + ") as " + coluna + ", min(date) as initial_date, max(date) as date from ga_browsers where date<date_sub(@today, interval 63 day) and date>=date_sub(@today, interval 70 day) and (url_id, browser) = (@url_id, @browser);"
                analysis = 'weeks'
            elif aggregation == 'days':
                if coluna in lastweekdays:
                    #gets last 10 weekday entries for the specified site, 9 for statistic analysis and 1 to be checked
                    sql = "select * from ga_browsers where (weekday(date),url_id,browser)=('%s', '%s', '%s') order by date desc limit 0,10;" %(str(maxdate), url_id, traffic_type)
                    analysis = 'weekdays'
                elif coluna in lastdays:
                    #gets last 10 day entries for the specified site, 9 for statistic analysis and 1 to be checked
                    sql = "select * from ga_browsers where (url_id,browser)=('%s', '%s') order by date desc limit 0,11;" %(url_id, traffic_type)
                    analysis = 'days'
                else:
                    logging.info("ERROR - Analysis period not defined for website or variable %s" %coluna)
            else:
                logging.error("Invalid 'aggregation' value for url id: %s" %str(url_id))
                url_break = True
                break
            cursor.execute(sql)
            results = cursor.fetchall()
            var = []
            dates = []
            format_type = dict_colunas['format'][coluna]

            #joins each day data in a list to apply statistics
            k = len(results)
            for result in results:
                if result[coluna] == None:
                    var[:0] = [0]
                else:
                    var[:0] = [format_type(result[coluna])]
                if analysis == 'weeks':
                    dates[:0] = [str(result['date']) + '\nWeek ' + str(k)]
                    k -= 1
                else:
                    dates[:0] = [str(result['date'])]

            if len(var) >= 5:
                #uses trimmean to get expected value
                trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_colunas['outlier'][coluna], format_type)
                x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
            else:
                logging.info("No data available for %s %s. Proceding to next browser..." %(siteurl, traffic_type))
                break

            #gets last day value to compare deviation from expected value
            try:
                var1 = format_type(results[0][coluna])
                date1 = results[0]['date']
                if coluna == 'sessions':
                    traffic_type_sessions = var1
            except:
                logging.info("No data available for %s %s. Proceding to next browser..." %(siteurl, traffic_type))
                continue

            # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
            # It checks the last date analyzed which had an email sent because in case the extraction scripts crash, it is necessary not to send the same alert again
            url_break = False
            cursor.execute("select ga_browsers from alerts_analysis_history where url_id = '%s';" %url_id)
            last_alert_date = cursor.fetchall()
            if last_alert_date != ():
                last_alert_date = last_alert_date[0]['ga_browsers']         #gets the last date from the alerts sent in past
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
                                logging.info("There is already an email alert sent to %s about Google Analytics Browsers data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                                url_break = True
                                break
                            else:
                                logging.info("There is already an email alert sent to %s about Google Analytics Browsers data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                                url_break = True
                                break
                    except:
                        pass

            # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
            # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
            cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
            last_emails_content = cursor.fetchall()
            
            # ------------------------------- TRENDS ANALYSIS --------------------------------
            #Checks if a variable is on a rising or falling trend. Accept criteria is:
            #R² > correlation coefficient
            #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
            if r_value > dict_colunas['correlation'][coluna] and p_value < 0.05:
                type_alert = [coluna, traffic_type, '', False]
                semantic_var, dimension_condition = get_semantic_dimention(type_alert)
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
                        if coluna in ['bounces', 'bounceRate']:
                            color = 'green'
                        elif coluna in ['pageviewsPerSession', 'avgTimeOnPage', 'avgSessionDuration']:
                            color = 'blue'
                        else:
                            color = 'red'
                    else:
                        trend_type += ' rising'
                        if coluna in ['bounces', 'bounceRate']:
                            color = 'red'
                        elif coluna in ['pageviewsPerSession', 'avgTimeOnPage', 'avgSessionDuration']:
                            color = 'blue'
                        else:
                            color = 'green'
                    trend = trend_phrase(semantic_var, dict_colunas['semantic'][language][coluna], type_alert, color, trend_type, format_type, 'dimension_on')
                    trend += '<br><img src="cid:Graph%s.png"><br>' %n

                    alerts_summary[url_id].append(type_alert)
                    url_trends.append(trend)
                    url_prior_trends.append(r_value)
                    trend_graph(maxdate, dict_colunas['semantic'][language][coluna], traffic_type, x, var, dates, vect_reg, r_value, color, analysis, n)
                    n += 1  

            # ------------------------------- OUTLIERS ANALYSIS --------------------------------
            #absdelta and percdelta are the anomaly detectors
            varabsdelta = var1 - trim_var
            try:
                varpercdelta = (var1/trim_var)-1
            except:
                varpercdelta = float("inf")
            
            #checks the variable being analyzed to determine the conditions to send email
            if var1 < lowerlimit or var1 > upperlimit:
                type_alert = [coluna, traffic_type, '', False]
                semantic_var, dimension_condition = get_semantic_dimention(type_alert)
                #classifying the outlier found             
                if varpercdelta > 0:
                    type_alert[2] = 'up'
                else:
                    type_alert[2] = 'down'
                if var1 < crit_lowerlimit or var1 > crit_upperlimit and lowerlimit != upperlimit:
                    type_alert[3] = True
                logging.info("Outlier found: %s" %type_alert)           

                # -------------- EMAIL CONSTRUCTING BLOCK (OUTLIER) --------------
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    if varabsdelta < 0:
                        sign = '-'
                        if coluna in ['bounces', 'bounceRate']:
                            color = 'green'
                        elif coluna in ['pageviewsPerSession', 'avgTimeOnPage', 'avgSessionDuration']:
                            color = 'blue'
                        else:
                            color = 'red'
                    else:
                        sign = '+'                   
                        if coluna in ['bounces', 'bounceRate']:
                            color = 'red'
                        elif coluna in ['pageviewsPerSession', 'avgTimeOnPage', 'avgSessionDuration']:
                            color = 'blue'
                        else:
                            color = 'green'
                    outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], semantic_var, x, var, dates, trim_var, upperlimit, lowerlimit, analysis, n)
                    if varpercdelta != float("inf"):
                        text = outlier_phrase(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, dimension_condition, 'yes', outliers_over_time)
                        text += '<br><img src="cid:Graph%s.png"><br>' %n
                        n += 1
                    #if every item in list is equal to zero, or the 25 and 75 percentile are zero, it will create a non critical alert, otherwise skips it
                    else:
                        type_alert = [coluna, traffic_type, type_alert[2], False]
                        if any(item != 0 for item in var[:-1]) == False:
                            text = outlier_phrase_zero(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, sign, format_type, dimension_condition, 'yes', 'zero')
                            text += '<br><img src="cid:Graph%s.png"><br>' %n
                            n += 1
                        else:
                            if [ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit] == [0, 0, 0, 0, 0]:
                                if aggregation == 'weeks':
                                    sql = "select 1 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 0 day) and date>=date_sub(@today, interval 7 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 2 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 7 day) and date>=date_sub(@today, interval 14 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 3 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 14 day) and date>=date_sub(@today, interval 21 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 4 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 21 day) and date>=date_sub(@today, interval 28 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 5 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 28 day) and date>=date_sub(@today, interval 35 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 6 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 35 day) and date>=date_sub(@today, interval 42 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 7 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 42 day) and date>=date_sub(@today, interval 49 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 8 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 49 day) and date>=date_sub(@today, interval 56 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 9 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 56 day) and date>=date_sub(@today, interval 63 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices') union select 10 as week, sum(sessions) as sessions, min(date) as initial_date, max(date) as date from ga_channels where date<date_sub(@today, interval 63 day) and date>=date_sub(@today, interval 70 day) and (url_id, channel, device) = (@url_id, 'Overall', 'All Devices');"
                                else:
                                    sql = "select sessions from ga_channels where (weekday(date),url_id,channel,device)=(%s,%s,'Overall','All Devices') order by date desc limit 0,10;" %(maxdate, url_id)
                                cursor.execute(sql)
                                reference_results = cursor.fetchall()
                                reference_var = []
                                for reference_result in reference_results:
                                    try:
                                        reference_var[:0] = [format_type(reference_result['sessions'])]
                                    except:
                                        continue

                                if len(var) >= 5:
                                    ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit = get_stats_values(reference_var, dict_colunas['outlier'][coluna], format_type)
                                else:
                                    continue

                            #checks if outlier appears in a significant variable (at least 2% of the normal or expected value not zero) otherwise it is ignored
                            if ref_trim_var == 0:
                                logging.info("The outlier won\'t be mentioned in alert because the traffic type mentioned is usually negligible")
                                continue                                
                            if traffic_type_sessions/ref_trim_var < 0.02:
                                logging.info("The outlier won\'t be mentioned in alert because the traffic type mentioned is usually negligible")
                                continue
                            else:
                                text = outlier_phrase_zero(dict_colunas['semantic'][language][coluna], type_alert, semantic_var, var1, date1, color, sign, format_type, dimension_condition, 'yes', 'close_to_zero')
                                text += '<br><img src="cid:Graph%s.png"><br>' %n
                                n += 1

                    alerts_summary[url_id].append(type_alert)
                    url_outliers.append(text)
                    if coluna in ['bounces', 'bounceRate']:
                        url_prior_outliers.append(-varpercdelta)
                    else:
                        url_prior_outliers.append(varpercdelta)                    

    # --------------------------------- EMAIL ALERTS HISTORY DATABASE MANIPULATION -----------------------------
    #if it makes sense to send url information to email, the email alert record is stored. The commit is only made inside the email script, which avoids errors
    if url_trends != [] or url_outliers != []:
        auxiliar_alerts_summary = {'outlier':{},'trends':{}}
        url_outliers, url_prior_outliers, outlier_additional_text = drop_similar_dim_alerts(url_outliers, url_prior_outliers, 'outlier', 'browsers', 2, traffic_types, str)
        url_trends, url_prior_trends, trends_additional_text = drop_similar_dim_alerts(url_trends, url_prior_trends, 'trends', 'browsers', 2, traffic_types, str)

        if url_id in auxiliar_alerts_summary['trends'] and url_id in auxiliar_alerts_summary['outlier']:
            alerts_summary[url_id] = auxiliar_alerts_summary['trends'][url_id] + auxiliar_alerts_summary['outlier'][url_id]
        elif url_id in auxiliar_alerts_summary['trends'] and url_id not in auxiliar_alerts_summary['outlier']:
            alerts_summary[url_id] = auxiliar_alerts_summary['trends'][url_id]
        elif url_id not in auxiliar_alerts_summary['trends'] and url_id in auxiliar_alerts_summary['outlier']:
            alerts_summary[url_id] = auxiliar_alerts_summary['outlier'][url_id]

        
        if url_trends != [] or url_outliers != [] or outlier_additional_text != [] or trends_additional_text != []:
            metric_comments = {'outlier':[],'trends':[]}
            kpi_connections(alerts_summary[url_id])
            
            #sorts changes from most negative to most positive
            dict_urls[url_id] = str(date1)
            analyzed_urls[execute_file[2]] = dict_urls

            # --------- EMAIL TOPICS SORTING BLOCK -----------
            file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
            sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green')

            file_emailtext += "".join(sorted_email)
            if outlier_additional_text != []:
                file_emailtext += "".join(outlier_additional_text)
            if metric_comments['outlier'] != []:
                file_emailtext += "<br>".join(metric_comments['outlier'])

            sorted_trends = sort_email_from_list(url_prior_trends, url_trends,'color:red','color:blue','color:green')
            file_emailtext += "".join(sorted_trends)
            if outlier_additional_text != []:
                file_emailtext += "".join(trends_additional_text)
            if metric_comments['trends'] != []:
                file_emailtext += "<br>".join(metric_comments['trends'])
                
# ------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Google Analytics Browsers','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
