#imports all the libraries from calling script
from __main__ import *
from TEST_INFO import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
logging.info("Running %s on %s" %(str(os.path.basename(__file__)), date))

#function to create png images with graphics
def outlier_graph(weekday, variable, var_type, x, y, dates, trim, up, down, analysis, n):
    if language in ['en']:
        variable = var_type + " " + variable
    elif language in ['pt']:
        variable = variable + " " + var_type
    graph_title, expected_value, upper_limit, lower_limit = get_graph_values(domain, variable, dates, analysis, weekday, 'outlier')
       
    font0 = FontProperties()
    font0.set_family('arial')
    font0.set_size(12)
    font0.set_style('italic')        
    font0.set_weight('bold')        
    
    font1 = FontProperties()
    font1.set_family('arial')
    font1.set_size(15)
    font1.set_weight('bold')        

    plt.figure(figsize=(len(x)-0.5, 3.5))
    plt.rcParams['axes.facecolor'] = 'w'

    plt.xticks(range(len(x)), dates, rotation = 20)    #enables ploting float vs string
    #graph information
    plt.title(graph_title , color = 'navy' , fontproperties = font1)

    y_varriations = []
    for value in y:
        try:
            y_varriation = (value/trim_var)-1
        except:
            y_varriation = float("inf")
        y_varriations.append(abs(y_varriation))        
    if down/up > 0.975 or max(y_varriations) > 5 or down == up:
    #Text in graph
        plt.annotate(expected_value, color = 'forestgreen', xy = ((len(x))/3, trim), fontproperties = font0)
        plt.axhline(y = trim, color = 'forestgreen', linewidth = 2, linestyle='--') #trimean
    else:
        plt.axhline(y = trim, color = 'forestgreen', linewidth = 2, linestyle='--') #trimean
        plt.axhline(y = up, color = 'red', linewidth = 2,linestyle='-.') #upper limit
        plt.axhline(y = down, color = 'red', linewidth = 2,linestyle='-.') #lower limit
        plt.annotate(expected_value, color = 'forestgreen', xy = ((len(x))/3, trim+(up-trim)/10), fontproperties = font0)
        plt.annotate(upper_limit, color = 'red', xy = ((len(x))/3, up-((up-trim)/10)), fontproperties=font0)
        plt.annotate(lower_limit, color = 'red', xy = ((len(x))/3, down+((trim-down)/10)), fontproperties=font0)

    #plots the points in black as diamonds
    plt.plot(x,y,'d', color = 'orange')
    for number in y:
        if number > up or number < down:
            plt.plot(y.index(number), number, 'D', color = 'red')

    #formats the axis to display big numbers with coma separating every 3 values. This also excludes scientific notation use 
    ax = plt.subplot()
    if format_type == float:
        ax.set_yticklabels(['{:0,.2f}'.format(format_type(x)) for x in ax.get_yticks().tolist()])
    elif format_type == int:
        ax.set_yticklabels(['{:0,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one


# -------------------------- log_analysis ANALYSIS --------------------------------
table_name, script_type = 'log_analysis', 'alerts'
url_ids = get_url_ids('log_analysis','log_analysis')
url_ids = list(set(url_ids) & set(allowed_url_ids))

#gets all the columns to compare data
user_agents = ['General','Googlebot']

dict_colunas = {'semantic':{'user-agent':{'en':{
                                            'General':'General',
                                            'Googlebot':'Googlebot',
                                            },
                                          'pt':{
                                            'General':'Geral',
                                            'Googlebot':'Googlebot',
                                            },
                                          },
                            'page':     {'en':{
                                            'All Pages':'All Pages',
                                            },
                                          'pt':{
                                            'All Pages':'Todas as Páginas',
                                            },
                                          },
                            'type':     {'en':{
                                            'Total Entries':'Total Entries',
                                            'Avg Load Time':'Avg Load Time',
                                            'Avg Load Time 2XX':'Avg Load Time 2XX',
                                            'Avg Load Time 3XX':'Avg Load Time 3XX',
                                            'Avg Load Time 4XX':'Avg Load Time 4XX',
                                            'Avg Load Time 5XX':'Avg Load Time 5XX',
                                            },
                                          'pt':{
                                            'Total Entries':'Total',
                                            'Avg Load Time':'Tempo Médio de Carregamento',
                                            'Avg Load Time 2XX':'Tempo Médio de Carregamento 2XX',
                                            'Avg Load Time 3XX':'Tempo Médio de Carregamento 3XX',
                                            'Avg Load Time 4XX':'Tempo Médio de Carregamento 4XX',
                                            'Avg Load Time 5XX':'Tempo Médio de Carregamento 5XX',
                                            },
                                          },
                            'colunas':  {'en':{
                                            'count':'Count',
                                            'avg_time':'Avg Load Time',
                                            },
                                          'pt':{
                                            'count':'Contagem',
                                            'avg_time':'Tempo Médio de Carregamento',
                                            },
                                          },
                            },
                'outlier':{'user-agent':{'General':1,
                                         'Googlebot':1.2,
                                          },
                                 'page':{'All Pages':1},
                                 'type':{'Total Entries':1,
                                         'Avg Load Time':1.5,
                                         'Avg Load Time 2XX':1.5,
                                         'Avg Load Time 3XX':1.5,
                                         'Avg Load Time 4XX':1.5,
                                         'Avg Load Time 5XX':1.5,
                                         },
                              'colunas':{'count':1.5,
                                         'avg_time':1.7,
                                          },
                },
                'format':{
                              'count':int,
                              'avg_time':float,
                              },
}             
#dict_texts = {'text1':{
#                        'en':'<span style="font-size:12px"><i><b>%s</b> Score had a major change of <span style="color:%s;">%s</span> points</i></span>',
#                        'pt':'<span style="font-size:12px"><i>O score da regra <b>%s</b> teve a maior mudança, de <span style="color:%s;">%s</span> pontos</i></span></i></span>',
#                      },



email_id = '5'
analysis = 'weeks'

prior_changes = []
file_emailtext = []

for url_id in url_ids:
    #get all the columns to be analyzed for the corresponding url
    cursor.execute("select log_pages,log_types from email_delivery where id = %s;" %email_id)
    results = cursor.fetchall()[0]
    page_types = results['log_pages']
    traffic_types = results['log_types']

    page_types = page_types.split(',')
    traffic_types = traffic_types.split(',')

    #gets weekday and hour to make the analysis    
    cursor.execute('select weekday(max(date_hour)) from ftp_logs where url_id = %s;' %url_id)
    maxdate = cursor.fetchall()[0]['weekday(max(date_hour))']
    cursor.execute('select hour(max(date_hour)) from ftp_logs where url_id = %s;' %url_id)
    maxhour = cursor.fetchall()[0]['hour(max(date_hour))']

    #cheks if there is actually data to analyze
    cursor.execute("select url from ftp_logs where url_id = %s limit 1;" , [url_id])
    results = cursor.fetchall()
    if len(results) == 0:
        logging.error('{}: there are no rows in ga_browsers table for url_id = {}'.format(__file__, url_id))
        continue
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    logging.info("Analyzing %s" %siteurl)

   url_break = False
    url_dict = {}
    urltrends = []
    urltext = []
    urlprior_changes = []
    urlprior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    for user_agent in user_agents:
        for page_type in page_types:
            for traffic_type in traffic_types:
                if 'Avg Load Time' in traffic_type:
                    coluna = 'avg_time'
                else:
                    coluna = 'count'
               # cursor.execute("select * from ftp_logs where (weekday(date_hour),hour(date_hour),url_id,url,user_agent,page,type) = \
    #(%s,%s,%s,%s,%s,%s,%s) order by date_hour desc limit 0,10;" , (maxdate,maxhour,url_id,siteurl,user_agent,page_type,traffic_type))
                cursor.execute("select * from ftp_logs where (hour(date_hour),url_id,url,user_agent,page,type) = \
    (%s,%s,%s,%s,%s,%s) order by date_hour desc limit 0,10;" , (maxhour,url_id,siteurl,user_agent,page_type,traffic_type))
                results = cursor.fetchall()
                ############# arrumar dia da semana tb
                if len(results) < 4:
                    logging.info("Not enough data to analyze on weekday:%s, hour:%s, id:%s, site:%s, user-agent:%s, page:%s, type:%s" %(maxdate, maxhour,url_id,siteurl,user_agent,page_type,traffic_type))
                    continue

                var = []
                dates = []
                format_type = dict_colunas['format'][coluna]
                #joins each day data in a list to apply statistics
                for result in results:
                    var[:0] = [format_type(result[coluna])]
                    dates[:0] = [str(result['date_hour'])]

                print(user_agent, page_type, traffic_type, coluna, var, dates)

                # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
                cursor.execute("select log_analysis from alerts_analysis_history where url_id = '%s';" %url_id)
                last_alert_date = cursor.fetchall()
                if last_alert_date != ():
                    last_alert_date = last_alert_date[0]['log_analysis']         #gets the last date from the alerts sent in past
                    if last_alert_date != None:
                        last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
                        try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                            email_alert_id = last_alert_date[email_group_id].split(':')[0]
                            last_analyzed_date = last_alert_date[email_group_id].split(':')[1]
                            if last_analyzed_date == str(date1):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                                cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                                sent_date = cursor.fetchall()[0]['sent_date']
                                logging.info("There is already an email alert sent to %s about log_analysis data collected for %s in %s. \
                This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                                #continue
                        except:
                            pass
                
                # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
                # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
                cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
                last_emails_content = cursor.fetchall()
                last_emails_content = ()


                #n += 1
                #alerts_summary[url_id].append(type_alert)
                #alerts_summary[url_id].append('teste')
                #file_emailtext.append(text)
                #prior_changes.append(percdelta)

                coef = dict_colunas['outlier']['user-agent'][user_agent]*dict_colunas['outlier']['colunas'][coluna]
                if page_type in dict_colunas['outlier']['page'].keys():
                    coef *= dict_colunas['outlier']['page'][page_type]
                if traffic_type in dict_colunas['outlier']['type'].keys():
                    coef *= dict_colunas['outlier']['type'][traffic_type]
                try:
                    trim_var, upperlimit, lowerlimit, x = get_stats_values(var, coef, format_type)
                except Exception as e:
                    logging.info(e)
                    continue

                #gets last day value to compare deviation from expected value
                try:
                    var1 = format_type(results[0][coluna])
                    date1 = results[0]['date_hour']
                except:
                    logging.info("No data available for %s %s %s %s %s. Proceding to next url..." %(user_agent, page_type, traffic_type, coluna, siteurl))
                    continue

                # ------------------------------- OUTLIERS ANALYSIS --------------------------------
                #absdelta and percdelta are the anomaly detectors
                varabsdelta = var1 - trim_var
                try:
                    varpercdelta = (var1/trim_var)-1
                except:
                    varpercdelta = float("inf")

                #checks the variable being analyzed to determine the conditions to send email
                if var1 < lowerlimit or var1 > upperlimit:
                    type_alert = "%s %s %s %s" %(user_agent, page_type, traffic_type, coluna)
                    #classifying the outlier found             
                    if abs(varpercdelta) > 0.5:
                        type_alert += ' critical'
                    if varabsdelta < 0:
                        type_alert += ' up'
                    else:
                        type_alert += ' down'
                    logging.info("Outlier found: %s" %type_alert)

                    # -------------- EMAIL CONSTRUCTING BLOCK (OUTLIER) --------------
                    var_email = avoid_same_content(last_emails_content, type_alert)
                    if var_email == True:
                        if varabsdelta < 0:
                            sign = '-'                    
                            if coluna in ['count']:
                                if traffic_type[0] == '2':
                                    color = 'red'
                                else: 
                                    color = 'green'
                            else:
                                color = 'blue'
                        else:
                            if coluna in ['count']:
                                if traffic_type[0] == '2':
                                    color = 'green'
                                else: 
                                    color = 'red'
                            else:
                                color = 'blue'
                        text_to_function = dict_colunas['semantic']['user-agent'][language][user_agent]
                        try:
                            text_to_function += " " + dict_colunas['semantic']['page'][language][page_type]
                        except:    
                            text_to_function += " " + page_type
                        #text_to_function += " " + dict_colunas['semantic']['type'][language][traffic_type]
                        text_to_function += " " + dict_colunas['semantic']['colunas'][language][coluna]
                        
                        text = outlier_phrase(text_to_function, type_alert, traffic_type, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, 'dimension_on')
                        text += '<br><img src="cid:Graph%s.png"><br>' %n

                        alerts_summary[url_id].append(type_alert)
                        urltext.append(text)
                        if coluna in ['bounces', 'bounceRate']:
                            urlprior_changes.append(-varpercdelta)
                        else:
                            urlprior_changes.append(varpercdelta)                    
                        outlier_graph(maxdate, text_to_function, traffic_type, x, var, dates, trim_var, upperlimit, lowerlimit, analysis, n)
                        n += 1
                #sys.exit()


    # --------------------------------- EMAIL ALERTS HISTORY DATABASE MANIPULATION -----------------------------
    #if it makes sense to send url information to email, the email alert record is stored. The commit is only made inside the email script, which avoids errors
    if file_emailtext != []:
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

        # --------- EMAIL TOPICS SORTING BLOCK -----------
        #sorts changes from most negative to most positive
        sorted_email = sort_email_from_list(urlprior_changes, urltext, 'color:red','color:blue','color:green')

        file_emailtext += '<br><span style="font-size:16px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
        #file_emailtext += "".join(sorted_email) + '<br>'
        file_emailtext = sorted_email[0]


#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
if file_emailtext != []:
    title = title_to_email_section('LOG','change')
    file_emailtext = title + file_emailtext
    test_email(file_emailtext)
else:
    file_emailtext = ''
    logging.info("No data sent to email")
