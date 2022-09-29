#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- GOOGLE SEARCH CONSOLE DATA ALERTS --------------------------------
table_name, script_type = 'gsc_errors', 'alerts'
url_ids = get_url_ids('gsc','Google Search Console Errors',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#gets all the columns to compare data
colunas_web = ['notFound', 'notFollowed', 'authPermissions', 'serverError', 'soft404', 'other']
colunas_smartphone = ['notFound', 'notFollowed', 'authPermissions', 'serverError', 'soft404', 'other', 'roboted', 'manyToOneRedirect', 'flashContent']

#dictionary containing necessary values for every column.
#1st section uses semantic for email construction, 2nd section for number of IQRs used for outlier detection,
#3rd section to trend analysis correlation factor, 4th section for variable types
dict_colunas = {'semantic':
                {'en':{
                    'notFound':'Not Found (404)',
                    'notFollowed':'Not Followed Urls',
                    'authPermissions':'Access Denied Urls',
                    'serverError':'Server Errors',
                    'soft404':'Soft 404',
                    'roboted':'Roboted Urls',
                    'manyToOneRedirect':'Faulty Redirects',
                    'flashContent':'Flash Content Not Renderized',
                    'other':'Other Errors'
                     },
                'pt':{
                    'notFound':'Não encontrado (404)',
                    'notFollowed':'URLs Não Seguidas',
                    'authPermissions':'URLs com Acesso Negado',
                    'serverError':'Erros de Servidor',
                    'soft404':'Soft 404',
                    'roboted':'URLs Bloqueadas',
                    'manyToOneRedirect':'Redirecionamento Ineficiente',
                    'flashContent':'Conteúdo Flash Não Renderizado',
                    'other':'Outros Erros'
                     },
                 },
    'details':{'en':{
                    'notFound':'Most 404 errors don\'t affect your site\'s ranking in Google, so you can safely ignore them. Typically, they are caused by typos,\
                                site misconfigurations, or by Google\'s increased efforts to recognize and crawl links in embedded content such as JavaScript. \
                                Here are some pointers to help you investigate and fix 404 errors:<br>\
                                1. Decide if it\'s worth fixing. Many (most?) 404 errors are not worth fixing. Here\'s why: Sort your 404s by priority and fix \
                                the ones that need to be fixed. You can ignore the other ones, because 404s don\'t harm your site\'s indexing or ranking.<br>\
                                2. See where the invalid links live. Click a URL to see Linked from these pages information. Your fix will depend on whether\
                                the link is coming from your own or from another site',
                    'notFollowed':'Not followed errors lists URLs that Google could not completely follow, along with some information as to why. Here are some reasons\
                                   why Googlebot may not have been able to follow URLs on your site: <br>\
                                   Some features such as JavaScript, cookies, session IDs, frames, DHTML, or Flash can make it difficult for search engines to crawl your site.\
                                   Use Fetch as Google to see exactly how your site appears to Google.',
                    'authPermissions':'In general, Google discovers content by following links from one page to another. To crawl a page, Googlebot must be able \
                                       to access it. If you\'re seeing unexpected Access Denied errors, it may be for the following reasons:<br>\
                                       1. Googlebot couldn\'t access a URL on your site because your site requires users to log in to view all or some of your content.<br>\
                                       2. Your server requires users to authenticate using a proxy, or your hosting provider may be blocking Google from accessing your site.',
                    'serverError':'This kind of error means that Googlebot couldn\'t access your URL, the request timed out, or \
                                   your site was busy. As a result, Googlebot was forced to abandon the request.',
                    'soft404':'Usually, when a visitor requests a page on your site that doesn\'t exist, a web server returns a 404 (not found) error. This HTTP \
                               response code clearly tells both browsers and search engines that the page doesn\'t exist. As a result, the content of the page \
                               (if any) won\'t be crawled or indexed by search engines.<br>\
                                A soft 404 occurs when your server returns a real page for a URL that doesn\'t actually exist on your site. This usually happens\
                                when your server handles faulty or non-existent URLs as "OK," and redirects the user to a valid page like the home page or a \
                                "custom" 404 page.<br>\
                                This is a problem because search engines might spend much of their time crawling and indexing non-existent, often duplicative \
                                URLs on your site. This can negatively impact your site\'s crawl coverage because your real, unique URLs might not be discovered \
                                as quickly or visited as frequently due to the time Googlebot spends on non-existent pages.',
                    'roboted':'This error(?) indicates that the robots.txt file needs to be modified to allow crawling of URLs. When the URLs are blocked, the\
                               pages can\'t be crawled and because of this, they may not appear in search results.',
                    'manyToOneRedirect':'Some websites use separate URLs to serve desktop and smartphone users and configure desktop pages to direct smartphone \
                                         users to the mobile site (e.g. m.example.com). A faulty redirect occurs when a desktop page incorrectly redirects smartphone \
                                         users to a smartphone page not relevant to their query. A typical example of this occurs when all desktop pages redirect \
                                         smartphone users to the homepage of the smartphone-optimized site. This kind of redirect disrupts users\' workflow and can\
                                         cause them to stop using the site and look elsewhere.',
                    'flashContent':'This error is related to having content rendered mostly in Flash. Many devices cannot render these pages \
                                    because Flash is not supported by iOS or Android versions 4.1 and higher.',
                    'other':'The errors marked as others didn\'t show a behavior that could classify them properly.',
                    'summary':'Check the summary below for details of the types of errors reported',
                     },
                'pt':{
                    'notFound':'A maioria dos erros 404 não afeta a classificação do site no Google. Por isso, não há problema em ignorá-los. Em geral, eles são \
                                causados por erros de digitação, configurações incorretas do site ou pelos avanços do Google no reconhecimento e rastreamento de \
                                links em conteúdos incorporados, como JavaScript. Veja algumas indicações para ajudar você a investigar e corrigir erros 404:<br>\
                                1. Decida se vale a pena corrigir o erro: Muitas vezes (talvez até na maioria dos casos), corrigir erros 404 é um desperdício de \
                                tempo. O motivo: Classifique seus erros 404 por prioridade e corrija aqueles que precisam ser corrigidos. Ignore os outros, pois \
                                erros 404 não prejudicam a classificação ou a indexação do site.<br>\
                                2. Veja onde estão os links inválidos. Clique em um URL para ver as informações de Links dessas páginas. A correção dependerá do \
                                local do link, se ele vem do seu ou de outro site',
                    'notFollowed':'Erros "Não seguido" listam os URLs que o Google não pôde acessar completamente, além de algumas informações sobre o motivo. O \
                                   Googlebot pode não ter conseguido acessar os URLs no seu website pelos seguintes motivos: <br>\
                                   Alguns recursos, como JavaScript, cookies, códigos de sessão, frames, DHTML ou Flash podem dificultar o rastreamento dos mecanismos \
                                   de pesquisa em relação a seu site. Use a Fetch as Google para ver exatamente como seu website aparece para o Google<br>\
                                   ',
                    'authPermissions':'Em geral, o Google detecta conteúdos seguindo links de uma página para outra. Para rastrear uma página, o Googlebot precisa \
                                       conseguir acessá-la. Se você vir erros do tipo "Acesso negado" não esperados, talvez seja por um destes motivos:<br>\
                                       1. O Googlebot não pôde acessar um URL em seu website, pois o site exige que os usuários façam login para visualizar todos \
                                       os conteúdos importantes.\
                                       2. O servidor exige que os usuários sejam autenticados usando um proxy. Ou seu provedor de hospedagem pode estar bloqueando \
                                       o acesso do Google ao site.',
                    'serverError':'Esse erro em URLs significa que o Googlebot não conseguiu acessar o URL, a solicitação excedeu o tempo limite ou o site estava \
                                   ocupado. Como resultado, o Googlebot teve que abandonar a solicitação.',
                    'soft404':'Normalmente, quando um visitante solicita uma página que não existe no seu site, um servidor da web retorna um erro 404 (não encontrado).\
                               Esse código de resposta HTTP diz claramente aos navegadores e aos mecanismos de pesquisa que a página não existe. Dessa forma, o \
                               conteúdo da página (se houver) não será rastreado ou indexado por mecanismos de pesquisa.<br>\
                               Um erro soft 404 ocorre quando o servidor retorna uma página real para um URL que não existe de verdade no seu website. Em geral, \
                               isso ocorre quando o servidor lida com URLs defeituosos ou inexistentes como se estivessem "OK" e redireciona o usuário para uma \
                               página válida, como a página inicial ou uma página 404 "personalizada".<br>\
                               Isso é um problema porque os mecanismos de pesquisa podem gastar muito tempo rastreando e indexando URLs inexistentes e com frequência\
                               duplicados em seu site. Isso pode afetar negativamente a cobertura de rastreamento do seu site, pois os URLs exclusivos e verdadeiros \
                               podem não ser descobertos tão rapidamente ou visitados com tanta frequência devido ao tempo em que o Googlebot passa em páginas inexistentes.',
                    'roboted':'Esse erro(?) muitas vezes isso indica que o arquivo robots.txt precisa ser modificado para permitir o rastreamento de URLs. \
                               Quando esses URLs são bloqueados, as páginas não podem ser rastreadas e, por isso, podem não aparecer nos resultados de pesquisa.',
                    'manyToOneRedirect':'Alguns sites usam URLs separados para veicular a usuários de computador e de smartphone e configuram as páginas para \
                                         computador de modo que elas direcionem os usuários de smartphone ao site para dispositivos móveis (por exemplo, m.example.com).\
                                         Um problema de redirecionamento ocorre quando uma página para computador redireciona os usuários de smartphone para uma página \
                                         não relacionada à consulta deles. Um exemplo típico disso é quando todas as páginas do site para computador redirecionam os \
                                         usuários de smartphone para a página inicial do site otimizado para smartphone. Esse tipo de redirecionamento interrompe o \
                                         fluxo de trabalho do usuário e pode fazer com que ele desista e acesse outro site',
                    'flashContent':'Erro relacionado à seção que têm conteúdo renderizado principalmente em Flash. Muitos dispositivos não podem \
                                    renderizar essas páginas porque o Flash não é compatível com iOS nem com Android nas versões 4.1 e superiores',
                    'other':'Os erros marcados como outros não apresentaram um comportamento que possibilitasse sua classificação',
                    'summary':'Verifique o resumo abaixo para ver detalhes dos tipos de erros relatados',
                     },
                 },
    #second subdivision
    'outlier':{
                'notFound':1.5,
                'notFollowed':1.5,
                'authPermissions':1.5,
                'serverError':1.5,
                'soft404':1.5,
                'roboted':1.5,
                'manyToOneRedirect':1.5,
                'flashContent':1.5,
                'other':2
                    },
    #third subdivision
    'correlation':{
                'notFound':0.9,
                'notFollowed':0.9,
                'authPermissions':0.9,
                'serverError':0.9,
                'soft404':0.9,
                'roboted':0.9,
                'manyToOneRedirect':0.9,
                'flashContent':0.9,
                'other':0.9,
                },
    #fourth subdivision
    'format':{
                'notFound':int,
                'notFollowed':int,
                'authPermissions':int,
                'serverError':int,
                'soft404':int,
                'roboted':int,
                'manyToOneRedirect':int,
                'flashContent':int,
                'other':int,
                },
    }

dict_traffic = {'semantic':{
    'smartphoneOnly':'Smartphone',
    'web':'Web',
    }
}

traffic_types = ['web','smartphoneOnly']

config_dict = yaml.load(email_to_send['gsc'])
file_emailtext = ''
details_text = ''

for url_id in url_ids:
    if config_dict[url_id]['errors'] == 0:
        logging.info('Errors not checked for url_id %s' %url_id)
        continue

    url_break = False
    url_dict = {}
    urltrends = []
    urltext = []
    urlprior_changes = []
    urlprior_trends = []
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []
    own_condition = 1

    #gets last 11 entries for the specified url, 10 for statistic analysis and 1 to be checked
    for traffic_type in traffic_types:
        if url_break == True:
            break
        cursor.execute("select * from gsc_errors where (url_id,platform)=(%s,%s) order by date desc limit 0,10;" , (url_id,traffic_type))
        results = cursor.fetchall()
        if len(results) == 0:
            logging.error('{}: no rows match: url_id: {} platform:{}'.format(__file__, url_id, traffic_type))
            continue
        siteurl = results[0]['url']
        domain = get_domain_name(siteurl)
        analysis = 'days'
        maxdate = 0
        logging.info("Analyzing %s %s" %(siteurl, traffic_type))

        if traffic_type == "smartphoneOnly":
            colunas = colunas_smartphone
        else:
            colunas = colunas_web

        #get values for each metric analyzed
        for coluna in colunas:
            #gets last day value
            try:
                var1 = int(results[0][coluna])
                date1 = results[0]['date']
            except:
                logging.info("No dates available for %s. Proceding to next url..." %siteurl)
                break

            # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
            # It checks the last date analyzed which had an email sent because in case the extraction scripts crash, it is necessary not to send the same alert again
            cursor.execute("select gsc_errors from alerts_analysis_history where url_id = '%s';" %url_id)
            last_alert_date = cursor.fetchall()
            if last_alert_date != ():
                last_alert_date = last_alert_date[0]['gsc_errors']         #gets the last date from the alerts sent in past
                if last_alert_date != None:
                    last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
                    try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                        email_alert_id = last_alert_date[email_group_id].split('|')[0]
                        last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                        if last_analyzed_date == str(date1):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                            cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                            sent_date = cursor.fetchall()[0]['sent_date']
                            logging.info("There is already an email alert sent to %s about Google Search Console Errors data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                            url_break = True
                            break
                    except:
                        pass

            # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
            # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
            cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
            last_emails_content = cursor.fetchall()

            # -------------------- PREPARE VALUES FOR ANALYSIS --------------------------
            var = []
            dates = []
            format_type = dict_colunas['format'][coluna]
            #joins each day data in a list to apply statistics
            for result in results:
                var[:0] = [format_type(result[coluna])]
                dates[:0] = [str(result['date'])]

            if len(var) >= 5:
                try:
                    #uses trimmean to get expected value
                    trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit = get_stats_values(var, dict_colunas['outlier'][coluna], format_type)
                    x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(var, 'all')
                        
                except Exception as e:
                    logging.info(e)
                    continue
            else:
                logging.info("No data available for %s %s. Proceding to next platform..." %(siteurl, coluna))
                break
                        
            # ------------------------------- TRENDS ANALYSIS --------------------------------
            #Checks if a variable is on a rising or falling trend. Accept criteria is:
            #R² > correlation coefficient
            #P value < 0.05 (coefficient value to reject null hypothesis of correlation)
            if r_value > dict_colunas['correlation'][coluna] and p_value < 0.05:
                type_alert = [coluna, traffic_type, '', False]
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
                        color = 'green'
                    else:
                        trend_type += ' rising'
                        color = 'red'
                    if coluna in ['roboted']:
                        color = 'blue'
                    trend = trend_phrase(dict_traffic['semantic'][traffic_type], dict_colunas['semantic'][language][coluna], type_alert, color, trend_type, format_type, 'dimension_on')
                    trend += '<br><img src="cid:Graph%s.png"><br>' %n

                    alerts_summary[url_id].append(type_alert)
                    urltrends.append(trend)
                    urlprior_trends.append(r_value)
                    trend_graph(maxdate, dict_colunas['semantic'][language][coluna], dict_traffic['semantic'][traffic_type], x, var, dates, vect_reg, r_value, color, analysis, n)                    
                    n += 1

                    if dict_colunas['details'][language][coluna] not in details_text:
                        details_text += '<b>%s</b>: %s<br>' %(dict_colunas['semantic'][language][coluna],dict_colunas['details'][language][coluna])

            # ------------------------------ OUTLIERS ANALYSIS ----------------------------------------
            # only runs outlier analysis if it is at least 2% of the traffic
            cursor.execute("select * from gsc_kpis where (url_id,type,device)=(%s,\"Overall\",\"All Devices\") order by date desc limit 0,10;" , [url_id])
            reference_results = cursor.fetchall()
            reference_var = []
            for reference_result in reference_results:
                reference_var[:0] = [format_type(reference_result['clicks'])]
            try:
                if len(var) >= 5:
                    ref_trim_var, ref_upperlimit, ref_lowerlimit, ref_crit_upperlimit, ref_crit_lowerlimit = get_stats_values(reference_var, dict_colunas['outlier'][coluna], format_type)
            except:
                continue

            if ref_trim_var == 0:
                logging.info("%s %s metric won\'t be mentioned in alert because the traffic type mentioned is usually negligible" %(coluna, traffic_type))
                continue
            #check if the metric appears in a significant variable (at least 2% of the clicks) otherwise it is ignored
            if trim_var/ref_trim_var < 0.01 and var1/ref_trim_var < 0.02:
                logging.info("%s %s metric won\'t be mentioned in alert because the traffic type mentioned is usually negligible" %(coluna, traffic_type))
                continue

            #absdelta and percdelta are the anomaly detectors
            varabsdelta = var1 - trim_var
            try:
                varpercdelta = (var1/trim_var)-1
            except:
                varpercdelta = 1
                
            #checks the variable being analyzed to determine the conditions to send email
            if var1 < lowerlimit or var1 > upperlimit:
                type_alert = [coluna, traffic_type, '', False]
                #classifying the outlier found             
                if var1 < crit_lowerlimit or var1 > crit_upperlimit and lowerlimit != upperlimit:
                    type_alert[3] = True
                if slope < 0:
                    type_alert[2] = 'up'
                else:
                    type_alert[2] = 'down'
                logging.info("Outlier found: %s" %type_alert)

                # -------------- EMAIL CONSTRUCTING BLOCK (OUTLIER) --------------
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    if varabsdelta < 0:
                        sign = '-'
                        color = 'green'
                    else:
                        sign = '+'
                        color = 'red'
                    if coluna in ['roboted']:
                        color = 'blue'

                    outliers_over_time = outlier_graph(maxdate, dict_colunas['semantic'][language][coluna], dict_traffic['semantic'][traffic_type], x, var, dates, trim_var, upperlimit, lowerlimit, analysis, n)
                    text = outlier_phrase(dict_colunas['semantic'][language][coluna], type_alert, dict_traffic['semantic'][traffic_type], var1, date1, color, abs(varpercdelta), trim_var, sign, format_type, 'dimension_on', 'yes', outliers_over_time)
                    text += '<br><img src="cid:Graph%s.png"><br>' %n

                    alerts_summary[url_id].append(type_alert)
                    if coluna == 'position':
                        urlprior_changes.append(-varpercdelta)
                    else:
                        urlprior_changes.append(varpercdelta)
                    n += 1

                    if dict_colunas['details'][language][coluna] not in details_text:
                        details_text += '<b>%s</b>: %s<br>' %(dict_colunas['semantic'][language][coluna],dict_colunas['details'][language][coluna])

                    #includes sample urls from the issue (only if rising)
                    if varabsdelta > 0:
                        cmdoutput = subprocess.getoutput("python3.6 GSC_API_errors_sample_urls.py %s %s %s" %(siteurl, coluna, traffic_type))                        
                        error_urls = cmdoutput.split("\n")
                        if len(error_urls) == 0:
                            continue
                        summary_table = '<br><table style="width:100%; font-size:11px; border-collapse: collapse; border: 1px solid black;">\
<tr><th style="border: 1px solid black;">Status</th><th style="border: 1px solid black;">Last Detected</th><th style="border: 1px solid black;">\
Url</th><th style="border: 1px solid black;">Linked From</th><th style="border: 1px solid black;">Sitemap XML</th></tr>'
                        simple_summary_table = summary_table
                        for error_url in error_urls:
                            error_url = error_url.split('\t')
                            summary_table += '<tr style="border: 1px solid black;">'
                            if len(error_url) == 3:
                                status, last_detected, url = error_url[0], error_url[1], error_url[2]
                                linked_from, sitemaps = [], []
                            elif len(error_url) == 4:
                                status, last_detected, url, linked_from = error_url[0], error_url[1], error_url[2], error_url[3]
                                linked_from, sitemaps = ast.literal_eval(linked_from), []
                            elif len(error_url) == 5:
                                status, last_detected, url, linked_from, sitemaps = error_url[0], error_url[1], error_url[2], error_url[3], error_url[4]
                                linked_from, sitemaps = ast.literal_eval(linked_from), ast.literal_eval(sitemaps)
                            else:
                                linked_from, sitemaps = [], []
                                continue

                            summary_table += '<td style="border: 1px solid black;">%s</td><td style="border: 1px solid black;">%s</td><td style="border: 1px solid black;">%s</td><td style="border: 1px solid black;">' %(status, last_detected, url)
                            simple_summary_table += '<td style="border: 1px solid black;">%s</td><td style="border: 1px solid black;">%s</td><td style="border: 1px solid black;">%s</td><td style="border: 1px solid black;"</table>' %(status, last_detected, url)
                            for link in linked_from:
                                summary_table += '<br>%s' %(link)
                            summary_table += '</td><td style="border: 1px solid black;">'
                            for link in sitemaps:
                                summary_table += '<br>%s' %(link)
                            summary_table += '</td></tr>'
                        summary_table += '</table>'
                        if simple_summary_table == summary_table: summary_table = ''
                        text += summary_table
                    urltext.append(text)


    # --------------------------------- EMAIL ALERTS HISTORY DATABASE MANIPULATION -----------------------------
    #if it makes sense to send url information to email, the email alert record is stored. The commit is only made inside the email script, which avoids errors
    if urltrends != [] or urltext != []:
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

        # --------- EMAIL TOPICS SORTING BLOCK -----------
        #sorts changes from most negative to most positive
        sorted_trends = sort_email_from_list(urlprior_trends, urltrends,'color:red','color:blue','color:green')
        sorted_email = sort_email_from_list(urlprior_changes, urltext, 'color:red','color:blue','color:green')

        file_emailtext += '<br><span style="font-size:16px"><b><a href="%s">%s</a></b></span><br>' %(siteurl, siteurl)
        file_emailtext += "".join(sorted_email)
        file_emailtext += "".join(sorted_trends) + '<br>'

if details_text != '':
    file_emailtext += '<b><span style="font-size:16px;color:blue;">' + dict_colunas['details'][language]['summary'] + '</span></b><br>' + details_text

# ------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Search Console Errors','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
