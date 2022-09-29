#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())
date_minus_1 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:00:00")

# -------------------------- PERFORMANCE ANALYSIS --------------------------------
table_name, script_type = 'performance', 'alerts'
url_ids = get_url_ids('performance','Performance',str)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#gets all the columns to compare data
#colunas = ['first-contentful-paint', 'first-meaningful-paint', 'first-cpu-idle', 'interactive', 'speed-index', \
#           'time-to-first-byte', 'critical-request-chains', 'network-requests']
colunas = ['speed-index', 'time-to-first-byte', 'critical-request-chains', 'network-requests']

dict_audits = {'semantic': {
    'first-contentful-paint': {'pt': 'First Contentful paint', 'en': 'First Contentful paint'},
    'first-meaningful-paint': {'pt': 'First meaningful paint', 'en': 'First meaningful paint'},
    'speed-index': {'pt': 'Índice de Percepção de Velocidade', 'en': 'Perceptual Speed Index'},
    'interactive': {'pt': 'Interactive', 'en': 'Interactive'},
    'first-cpu-idle': {'pt': 'First CPU Idle', 'en': 'First CPU Idle'},
    'max-potential-fid': {'pt': 'Delay do Primeiro Input', 'en': 'First Input Delay'},
    'estimated-input-latency': {'pt': 'Latência estimada de entrada', 'en': 'Estimated Input Latency'},
    'total-blocking-time': {'pt': 'Tempo Total de Bloqueio', 'en': 'Total Blocking Time'},
    'render-blocking-resources': {'pt': 'Site não usa recursos que retardam a primeira pintura', 'en': 'Render-Blocking Resources'},
    'uses-responsive-images': {'pt': 'Dimensione imagens apropriadamente', 'en': 'Properly size images'},
    'offscreen-images': {'pt': 'Imagens Offscreen', 'en': 'Offscreen images'},
    'unminified-css': {'pt': 'Minificar CSS', 'en': 'Minify CSS'},
    'unminified-javascript': {'pt': 'Minificar JavaScript', 'en': 'Minify JavaScript'},
    'unused-css-rules': {'pt': 'Regras CSS não usadas', 'en': 'Unused CSS rules'},
    'uses-optimized-images': {'pt': 'Otimize imagens', 'en': 'Optimize images'},
    'uses-webp-images': {'pt': 'Servir imagens em formatos da próxima geração', 'en': 'Serve images in next-gen formats'},
    'uses-text-compression': {'pt': 'Habilite a compressão de texto', 'en': 'Enable text compression'},
    'uses-rel-preconnect': {'pt': 'Faça Preload de elementos chave', 'en': 'Preload key requests'},
    'time-to-first-byte': {'pt': 'Mantenha o tempo de resposta do servidor baixo (TTFB)', 'en': 'Keep server response times low (TTFB)'},
    'redirects': {'pt': 'Evite redirecionamentos de páginas', 'en': 'Avoids page redirects'},
    'uses-rel-preload': {'pt': 'Use Preload em recursos essenciais', 'en': 'Preload key requests'},
    'efficient-animated-content': {'pt': 'Conteúdo Animado Eficiente', 'en': 'Efficient Animated Content'},
    'total-byte-weight': {'pt': 'Evite transmissão de enormes quantidades de dados', 'en': 'Avoids enormous network payloads'},
    'uses-long-cache-ttl': {'pt': 'Uso ineficiente de cache em recursos estáticos', 'en': 'Uses inefficient cache policy on static assets'},
    'dom-size': {'pt': 'Evite um tamanho de DOM excessivo', 'en': 'Avoids an excessive DOM size'},
    'critical-request-chains': {'pt': 'Cadeia de Requesições Críticas', 'en': 'Critical Request Chains'},
    'user-timings': {'pt': 'Marcações e medições de User Timing', 'en': 'User Timing marks and measures'},
    'bootup-time': {'pt': 'O tempo de boot do JavaScript é muito alto', 'en': 'JavaScript boot-up time is too high'},
    'mainthread-work-breakdown': {'pt': 'Redução do trabalho da thread principal', 'en': 'Main thread work breakdown'},
    'font-display': {'pt': 'Evite textos invisíveis enquanto as fontes web estão carregando', 'en': 'Avoid invisible text while webfonts are loading'},
    'performance-budget': {'pt': 'Perfomance Budget', 'en': 'Perfomance Budget'},
    'resource-summary': {'pt': 'Sumário de Recursos', 'en': 'Resources Summary'},
    'third-party-summary': {'pt': 'Recursos de Terceiros', 'en': 'Third Party Resources'},
    'network-requests': {'pt': 'Requisições à Rede', 'en': 'Network Requests'},
    'network-rtt': {'pt': 'Network Round Trip Times', 'en': 'Network Round Trip Times'},
    'network-server-latency': {'pt': 'Latências de Backend de Server', 'en': 'Server Backend Latencies'},
    'main-thread-tasks': {'pt': 'Tarefas', 'en': 'Tasks'}, 'diagnostics': {'pt': 'Diagnóstico', 'en': 'Diagnostics'},
    'metrics': {'pt': 'Métricas', 'en': 'Metrics'},
    'screenshot-thumbnails': {'pt': 'Screenshot Thumbnails', 'en': 'Screenshot Thumbnails'},
    'first-input-delay': {'pt': 'First Input Delay', 'en': 'First Input Delay'},
    'cumulative-layout-shift': {'pt': 'Cumulative Layout Shift Score', 'en': 'Cumulative Layout Shift Score'},
    'largest-contentful-paint': {'pt': 'Largest Contentful Paint', 'en': 'Largest Contentful Paint'},
    'final-screenshot': {'pt': 'Screenshot Final', 'en': 'Final Screenshot'}
    },

'outlier':{
          'efficient-animated-content':2,
          'first-contentful-paint':2,
          'first-meaningful-paint':2,
          'first-cpu-idle':2,
          'interactive':2,
          'consistently-interactive':2,
          'speed-index':2,
          'estimated-input-latency':2,
          'time-to-first-byte':2,
          'first-input-delay':2,
          'cumulative-layout-shift':2,
          'largest-contentful-paint':2,
          'critical-request-chains':3,
          'network-requests':3
          },
}

dict_texts = {'text1':{
                        'en':'<span style="font-size:12px"><i><b>%s</b> Score had a major change of <span style="color:%s;">%s</span> points',
                        'pt':'<span style="font-size:12px"><i>O score da regra <b>%s</b> teve a maior mudança, de <span style="color:%s;">%s</span> pontos',
                      },
                }

prior_changes = []
file_emailtext = ''

for url_id in url_ids:
    #gets last 2 entries for the specified url
    url_dict = {}
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select * from performance where url_id = '%s' and device = 'mobile' order by datetime desc limit 1;" %url_id)
    results = cursor.fetchall()
    siteurl = results[0]['url']
    domain = ''
    variable = ''
    traffic_type = ''
    var_type = ''
    analysis = 'hours'
    dates = []
    url_outliers = []
    url_prior_outliers = []

    logging.info("Analyzing %s..." %siteurl)
    
    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select performance from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['performance']         #gets the last date from the alerts sent in past
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
                        logging.info("There is already an email alert sent to %s about Perfomance data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        continue
                    else:
                        logging.info("There is already an email alert sent to %s about Perfomance data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, date1))
                        continue
            except:
                pass

    cursor.execute("select own_url from monitoring_links where id = %s and owner_id = %s;" , [url_id, owner_id])
    own_condition = cursor.fetchall()[0]['own_url']

    # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
    # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
    cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, date_minus_1))
    last_emails_content = cursor.fetchall()

    for coluna in colunas:
        cursor.execute("select * from performance where url_id = '%s' and device = 'mobile' order by datetime desc limit 12;" %url_id)
        results = cursor.fetchall()
        var = []
        dates = []
        format_type = int
        #joins each day data in a list to apply statistics
        for result in results:
            try:
                var[:0] = [format_type(result[coluna.replace('-','_')])]
                dates[:0] = [str(result['datetime'])]
            except:
                continue

        if len(var) >= 5:
            #uses trimmean to get expected value
            if coluna in dict_audits['outlier']:
                trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_audits['outlier'][coluna], format_type)
            else:
                trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, 1.5, format_type)
            x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
        else:
            logging.info("No data available for %s. Proceding to next channel..." %(siteurl))
            continue

        #gets last day value to compare deviation from expected value
        try:
            var1 = format_type(results[0][coluna.replace('-','_')])
            date1 = results[0]['datetime']
        except:
            logging.info("No data available for %s. Proceding to next browser..." %(siteurl))
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
            if coluna in ['critical-request-chains', 'network-requests']:
                if abs(varpercdelta) < 0.1:
                    continue
            type_alert = [coluna, traffic_type, 'mobile', False]
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

                outliers_over_time = outlier_graph(0, dict_audits['semantic'][coluna][language], semantic_var, x, var, dates, trim_var, upperlimit, lowerlimit, 'hours', n)
                if varpercdelta != float("inf"):
                    text = outlier_phrase(dict_audits['semantic'][coluna][language], type_alert, semantic_var, var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, dimension_condition, 'yes', outliers_over_time)
                    text += '<br><img src="cid:Graph%s.png"><br>' %n
                    n += 1
                else:
                    continue
                alerts_summary[url_id].append(type_alert)
                url_outliers.append(text)
                url_prior_outliers.append(varpercdelta)

                dict_urls[url_id] = str(date1)
                analyzed_urls[execute_file[2]] = dict_urls 

    if url_outliers != []:        
        sorted_email = sort_email_from_list(url_prior_outliers, url_outliers, 'color:red','color:blue','color:green')
        file_emailtext += '<br><span style="font-size:15px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
        file_emailtext += "".join(sorted_email) + '<br>'       
                

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
if file_emailtext != '':
    title = title_to_email_section('Performance','change')
    file_emailtext = title + file_emailtext
else:
    file_emailtext = ''
    logging.info("No data sent to email")
