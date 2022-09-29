#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()

#function to create png images with graphics
def single_line_graph(x, y, dates, n):
    graph_title, expected_value, upper_limit, lower_limit = get_graph_values(domain, variable, '', dates, analysis, weekday0, 'outlier')
        
    font0 = FontProperties()
    font0.set_family('arial')
    font0.set_size(12)
    font0.set_style('italic')        
    font0.set_weight('bold')        
    
    font1 = FontProperties()
    font1.set_family('arial')
    font1.set_size(15)
    font1.set_weight('bold')        

    plt.figure(figsize=(len(x)-0.5, 3))
    plt.rcParams['axes.facecolor'] = 'w'

    plt.xticks(range(len(x)), dates, rotation = 20)    #enables ploting float vs string
    #graph information
    plt.title(graph_title , color = 'navy' , fontproperties = font1)

    #plots a random color (not white) smooth line (200 points are used interpolating the array's size)
    random_color = (random.uniform(0, 0.8), random.uniform(0, 0.8), random.uniform(0, 0.8))
    plt.plot(x, y, color = random_color)

    #formats the axis to display big numbers with coma separating every 3 values. This also excludes scientific notation use 
    ax = plt.subplot()
    if format_type == float:
        ax.set_yticklabels(['{:0,.2f}'.format(format_type(x)) for x in ax.get_yticks().tolist()])
    elif format_type == int:
        ax.set_yticklabels(['{:0,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one


# -------------------------- GOOGLE SEARCH CONSOLE DATA ALERTS --------------------------------
table_name, script_type = 'gsc_index', 'alerts'
url_ids = get_url_ids('gsc','Google Search Console Index',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection,
#3rd section to trend analysis correlation factor, 4th section for variable types
dict_colunas = { 
    #first subdivision
    'semantic':{'en':{
                    'ERROR':'Error',
                    'WARNING':'Warning',
                    'INFORMATIONAL':'Informational',
                    'OK':'Ok',
                    'SUBMITTED_NOINDEX':'Submitted URL marked ‘noindex’',
                    'TOO_MANY_REDIRECT':'Redirect error',
                    'SERVER_ISSUES':'Server error (5xx)',
                    'SUBMITTED_BLOCKED':'Submitted URL blocked by robots.txt',
                    'SUBMITTED_GENERIC_CRAWL_ERROR':'Submitted URL has crawl issue',
                    'SUBMITTED_NOT_FOUND':'Submitted URL not found (404)',
                    'INDEXED_BLOCKED':'Indexed, though blocked by robots.txt',
                    'CRAWLED':'Crawled - currently not indexed',
                    'ALT_REDIRECT':'Page with redirect',
                    'NO_INDEX_TAG':'Excluded by ‘noindex’ tag',
                    'BLOCKED':'Blocked by robots.txt',
                    'ALTERNATE_WITH_CANONICAL':'Alternate page with proper canonical tag',
                    'DUP_USER_CANONICAL':'Duplicate, Google chose different canonical than user',
                    'GENERIC_CRAWL_ERROR':'Crawl anomaly',
                    'NOT_FOUND':'Not found (404)',
                    'DISCOVERED':'Discovered - currently not indexed',
                    'SUBMITTED_DUP':'Duplicate, submitted URL not selected as canonical',
                    'DUP_NO_CANONICAL':'Duplicate without user-selected canonical',
                    'INDEXED_NOT_SUBMITTED':'Indexed, not submitted in sitemap',
                    'INDEXED':'Submitted and indexed',
                    'NOT_AUTHORIZED':'Not Authorized (401)',
                    'SOFT_404':'Soft 404',
                    'FORBIDDEN':'Blocked due to forbidden access (403)',
                    'CLIENT_ERROR':'Blocked due to another cliente error 4xx',
                    },
                'pt':{
                    'ERROR':'Error',
                    'WARNING':'Warning',
                    'INFORMATIONAL':'Informational',
                    'OK':'Ok',
                    'SUBMITTED_NOINDEX':'URL enviado marcado como "noindex"',
                    'TOO_MANY_REDIRECT':'Erro de redirecionamento',
                    'SERVER_ISSUES':'Erro no servidor (5xx)',
                    'SUBMITTED_BLOCKED':'URL enviado bloqueado pelo arquivo robots.txt',
                    'SUBMITTED_GENERIC_CRAWL_ERROR':'URL enviado tem problema de rastreamento',
                    'SUBMITTED_NOT_FOUND':'URL enviado não encontrado (404)',
                    'INDEXED_BLOCKED':'Indexada, mas bloqueada pelo robots.txt',
                    'CRAWLED':'Rastreada, mas não indexada no momento',
                    'ALT_REDIRECT':'Página com redirecionamento',
                    'NO_INDEX_TAG':'Excluída pela tag "noindex"',
                    'BLOCKED':'Bloqueada pelo robots.txt',
                    'ALTERNATE_WITH_CANONICAL':'Página alternativa com tag canônica adequada',
                    'DUP_USER_CANONICAL':'Cópia, o Google e o usuário selecionaram uma página canônica diferente',
                    'GENERIC_CRAWL_ERROR':'Anomalia no rastreamento',
                    'NOT_FOUND':'Não encontrado (404)',
                    'DISCOVERED':'Detectada, mas não indexada no momento',
                    'SUBMITTED_DUP':'Cópia, o URL enviado não foi selecionado como canônico',
                    'DUP_NO_CANONICAL':'Cópia sem página canônica selecionada pelo usuário',
                    'INDEXED_NOT_SUBMITTED':'Indexada, não enviada no sitemap',
                    'INDEXED':'Enviada e indexada',
                    'NOT_AUTHORIZED':'Bloqueada devido a solicitação não autorizada (401)',
                    'SOFT_404':'Erro soft 404',
                    'FORBIDDEN':'Bloqueada devido a acesso proibido (403)',
                    'CLIENT_ERROR':'Bloqueada devido a outro problema 4xx',
                    },
                },
    #second subdivision
    'outlier':1.5,
    #third subdivision
    'correlation':0.9,
    #fourth subdivision
    'format':int,
}

config_dict = yaml.load(email_to_send['gsc'])
file_emailtext = ''

for url_id in url_ids:
    if config_dict[url_id]['index'] == 0:
        logging.info('Index not checked for url_id %s' %url_id)
        continue
    #gets last 2 entries for the specified url
    url_dict = {}
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select url,date,sum(total), type from gsc_index where url_id = %s group by type,date order by date desc limit 4;" %url_id)
    results = cursor.fetchall()
    if len(results) == 0:
        logging.info('{}: no rows match to url_id: {}'.format(__file__, url_id))
        continue

    current_indexed_numbers = {}
    for result in results:
        current_indexed_numbers[result['type']] = int(result['sum(total)'])
    try:
        indexed = current_indexed_numbers['OK']
    except:
        logging.error('The indexed pages "type" is not defined for not null entries on url id: %s' %url_id)
        continue
    
    siteurl = results[0]['url']
    domain = get_domain_name(siteurl)
    color = 'blue'
    variable = ''
    analysis = 'weekdays'
    own_condition = 1
    url_break = False
    url_trends = []
    url_outliers = []
    url_prior_outliers = []
    url_prior_trends = []

    logging.info("Analyzing %s Google index..." %siteurl)

    # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
    # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
    cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
    last_emails_content = cursor.fetchall()
    
    cursor.execute("select weekday(max(date)) from gsc_index where url_id = %s;" %(url_id))
    maxdate = cursor.fetchall()[0]['weekday(max(date))']

    cursor.execute("select max(date) from gsc_index where url_id = %s;" %(url_id))
    end_date = cursor.fetchall()[0]['max(date)']
    check_dates = []
    start_date = end_date - timedelta(days=63)
    weekday0 = int(end_date.weekday())

    while end_date >= start_date:
        check_dates.append(end_date)
        end_date = end_date - timedelta(days=7)
    date1 = check_dates[0]
    check_dates = check_dates[::-1]

    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select gsc_index from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['gsc_index']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about Google Search Console Indexed Pages data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                    else:
                        logging.info("There is already an email alert sent to %s about Google Search Console Indexed Pages data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                        continue

            except:
                pass

    for index_type in current_indexed_numbers:
        cursor.execute("select distinct(status) from gsc_index where url_id = %s and type = '%s';" %(url_id, index_type))
        results = cursor.fetchall()
        index_conditions = []
        for result in results:
            index_conditions.append(result['status'])
        
        for index_condition in index_conditions:
            cursor.execute("select date,total,type,status from gsc_index where (url_id, weekday(date), type, status) = (%s, %s, '%s','%s') order by date desc limit 10;" %(url_id, weekday0, index_type, index_condition))
            sub_results = cursor.fetchall()
            variable = dict_colunas['semantic'][language][index_condition]
            
            var = []
            format_type = int
            #joins each day data in a list to apply statistics
            for sub_result in sub_results:
                if sub_result['date'] in check_dates:
                    var.append(format_type(sub_result['total']))
                else:
                    var.append(0)

            var1 = var[0]
            var2 = var[1]
            var = var[::-1]
            if len(var) >= 5:
                #uses trimmean to get expected value
                trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_colunas['outlier'], format_type)
                x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
            else:
                logging.info("No data available for %s %s. Proceding to next type..." %(siteurl, index_condition))
                continue
            
            if var1/indexed <= 0.015 and var2/indexed < 0.015:
                logging.info("The amount of %s are irrelevant, proceding to next condition..." %index_condition)
                continue

            # ------------------------------- TRENDS ANALYSIS --------------------------------
            #Checks if a variable is on a rising or falling trend. Accept criteria is:
            #R² > correlation coefficient
            #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
            if r_value > dict_colunas['correlation'] and p_value < 0.05:
                type_alert = [index_condition, index_type, '', False]
                #classifying the trend found             
                if r_value > 0.99:
                    type_alert[3] = True
                if slope < 0:
                    type_alert[2] = 'falling'
                else:
                    type_alert[2] = 'rising'
                logging.info("Trend found: %s" %type_alert)
                
                # -------------- EMAIL CONSTRUCTING BLOCK (TRENDS) --------------
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    if slope < 0:
                        trend_type += ' falling'
                        if index_type in ['ERROR','WARNING']:
                            color = 'green'
                        else:
                            color = 'blue'
                    else:
                        trend_type += ' rising'
                        if index_type in ['ERROR','WARNING']:
                             color = 'red'
                        else:
                             color = 'blue'
                    trend_graph(maxdate, dict_colunas['semantic'][language][index_condition], '', x, var, check_dates, vect_reg, r_value, color, analysis, n)
                    trend = trend_phrase('', dict_colunas['semantic'][language][index_condition], type_alert, color, trend_type, format_type, 'dimension_on')
                    trend += '<br><img src="cid:Graph%s.png"><br>' %n
                    
                    alerts_summary[url_id].append(type_alert)
                    url_trends.append(trend)
                    url_prior_trends.append(r_value)
                    n += 1

            # ------------------------------ OUTLIERS ANALYSIS ----------------------------------------
            #absdelta and percdelta are the anomaly detectors    
            varabsdelta = var1 - trim_var
            try:
                varpercdelta = (var1/trim_var)-1
            except:
                varpercdelta = float("inf")

            if var1 < lowerlimit or var1 > upperlimit:
                type_alert = [index_condition, index_type, '', False]
                #classifying the outlier found             
                if var1 < crit_lowerlimit or var1 > crit_upperlimit and lowerlimit != upperlimit:
                    type_alert[3] = True
                if slope < 0:
                    type_alert[2] = 'up'
                    sign = '-'
                else:
                    type_alert[2] = 'down'
                    sign = '+'
                logging.info("Outlier found: %s" %type_alert)

                # -------------- EMAIL CONSTRUCTING BLOCK (OUTLIER) --------------
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    if index_type in ['ERROR','WARNING'] and varabsdelta < 0:
                        color = 'green'
                    elif index_type in ['ERROR','WARNING'] and varabsdelta > 0:
                        color = 'red'
                    else:
                        color = 'blue'

                    outliers_over_time = outlier_graph(maxdate, '"' + dict_colunas['semantic'][language][index_condition] + '"', '', x, var, check_dates, trim_var, upperlimit, lowerlimit, analysis, n)
                    text = outlier_phrase(dict_colunas['semantic'][language][index_condition], type_alert, '', var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, 'dimension_off', 'yes', outliers_over_time)
                    text += '<br><img src="cid:Graph%s.png"><br>' %n
                    
                    url_outliers.append(text)
                    if index_type == 'ERROR':
                        url_prior_outliers.append(-varpercdelta)
                    else:
                        url_prior_outliers.append(varpercdelta)
                        
                    alerts_summary[url_id].append(type_alert)
                    #single_line_graph(x, var, check_dates, n)
                    n += 1
                    
    if url_trends != [] or url_outliers != []:
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

        # --------- EMAIL TOPICS SORTING BLOCK -----------
        #sorts changes from most negative to most positive
        sorted_trends = sort_email_from_list(url_prior_trends, url_trends,'color:red','color:blue','color:green')
        sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green')

        file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
        file_emailtext += "".join(sorted_email) + '<br>'
        file_emailtext += "".join(sorted_trends) + '<br>'
                    
# ------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Google Search Console Index','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
