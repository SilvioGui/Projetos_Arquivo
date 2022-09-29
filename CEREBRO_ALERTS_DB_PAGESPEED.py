#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

#function to create png images with graphics
def criterias_graph(reasons_graph):
    criteria_names = []
    criteria_values = []
    for key in reasons_graph:
        criteria_names.append(dict_colunas['semantic'][key][language]['rule'])
        criteria_values.append(float(reasons_graph[key]))
    graph_title = get_graph_values(domain, variable, var_type, dates, analysis, weekday, 'performance')

    mean_length = int(numpy.mean([len(i) for i in criteria_names])*0.5)      #gets every column name length to define a mean column length as integer value
    wrapped_text = ["\n".join(textwrap.wrap(i,mean_length)) for i in criteria_names]    #breaks text in the column length defined above to make the axis good to read

    plt.figure(figsize=(len(criteria_names)*0.9, 2)) #fig size in x and y direction
    plt.margins(0.01, 0.05)

    random_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

    #plots bar graph of criteria_name and its values. x is created as a list from 0 to len(criteria_names) to make it work as x axis
    x = numpy.arange(len(criteria_names))
    plt.bar(x, criteria_values, width = 0.4, color = random_color)  #uses random color for each graph
    plt.xticks(x, wrapped_text, rotation = 45, ha ='right', rotation_mode = 'anchor', fontsize = 7)    #enables ploting float vs string
    plt.title(graph_title , color = 'navy', fontsize = 10, fontweight='bold')

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

# -------------------------- PAGESPEED SCORE ALERTS --------------------------------
table_name, script_type = 'pagespeed', 'alerts'
url_ids = get_url_ids('pagespeed','Pagespeed Insights',str)
url_ids = list(set(url_ids) & set(allowed_url_ids))

#gets all the columns to compare data
colunas = ['AvoidLandingPageRedirects', 'EnableGzipCompression', 'LeverageBrowserCaching', 'MainResourceServerResponseTime', 'MinifyCss', 'MinifyHTML',
           'MinifyJavaScript', 'MinimizeRenderBlockingResources', 'OptimizeImages', 'PrioritizeVisibleContent']
colunas2 = ['FirstContentfulPaint', 'DOMContentLoadedEventFired']

dict_colunas = {'semantic':{'AvoidLandingPageRedirects':{'en':{'rule':'Avoid Landing Page Redirects',
                                                               'description':'This rule shows that you have more than one redirect from the given url to the final landing page.\
                                                                Redirects trigger an additional HTTP request-response cycle and delay page rendering.\
                                                                In the best case, each redirect will add a single roundtrip (HTTP request-response), \
                                                                and in the worst it may result in multiple additional roundtrips to perform the DNS lookup,\
                                                                TCP handshake, and TLS negotiation in addition to the additional HTTP request-response cycle.\
                                                                As a result, you should minimize use of redirects to improve site performance.'
                                                               },
                                                         'pt':{'rule':'Evitar Redirecionamentos na Landing Page',
                                                               'description':'Esta regra detecta que você tem mais de um redirecionamento na URL de destino final.\
                                                               Os redirecionamentos desencadeiam um ciclo adicional de solicitação-resposta HTTP e atrasam a \
                                                               renderização da página. Na melhor das hipóteses, cada redirecionamento adicionará uma viagem de ida \
                                                               e volta (solicitação-resposta HTTP). Na pior dos hipóteses, várias viagens de ida e volta adicionais \
                                                               serão necessárias para concluir a busca DNS, o handshake do TCP e a negociação do TLS, além do ciclo \
                                                               adicional de solicitação-resposta HTTP. Como resultado, será preciso minimizar o uso de \
                                                               redirecionamentos para melhorar o desempenho do site.'
                                                               },
                                                         },
                            'EnableGzipCompression':{'en':{'rule':'Enable Gzip Compression',
                                                               'description':'This rule detects that compressible resources were served without gzip compression.\
                                                                All modern browsers support and automatically negotiate gzip compression for all HTTP requests. \
                                                                Enabling gzip compression can reduce the size of the transferred response by up to 90%, \
                                                                which can significantly reduce the amount of time to download the resource, reduce data usage \
                                                                for the client, and improve the time to first render of your pages.'
                                                               },
                                                         'pt':{'rule':'Habilitar a Compressão Gzip',
                                                               'description':'Todos os navegadores modernos são compatíveis com compactação gzip e a processam \
                                                               automaticamente em todas as solicitações HTTP. Ativar a compactação gzip pode reduzir o tamanho da \
                                                               resposta transferida em até 90%. Como resultado, pode haver uma redução significativa no tempo de \
                                                               download do recurso, no uso de dados do cliente e no tempo de renderização das páginas.'
                                                               },
                                                         },
                            'LeverageBrowserCaching':{'en':{'rule':'Make Use of Browser Caching',
                                                               'description':'This rule detects that the response from your server does not include caching headers \
                                                                or if the resources are specified to be cached for only a short time.\
                                                                Fetching resources over the network is both slow and expensive: the download may require multiple \
                                                                roundtrips between the client and server, which delays processing and may block rendering of page \
                                                                content, and also incurs data costs for the visitor. All server responses should specify a caching \
                                                                policy to help the client determine if and when it can reuse a previously fetched response.\
                                                                '},
                                                         'pt':{'rule':'Fazer Uso do Cache do Browser',
                                                               'description':'Esta regra detecta que a resposta do servidor não inclui cabeçalhos explícitos de \
                                                               armazenamento em cache ou quando há uma especificação para armazenar recursos em cache somente \
                                                               por um curto período. A busca de recursos na rede é lenta e dispensiosa: o download pode exigir \
                                                               múltiplas viagens de ida e volta entre o cliente e o servidor, o que atrasa o processamento e pode \
                                                               bloquear a renderização do conteúdo da página, além de causar custos de dados para o visitante. \
                                                               Todas as respostas do servidor precisam especificar uma política de cache para ajudar o cliente a \
                                                               determinar em que situações é possível reutilizar uma resposta buscada previamente'},
                                                         },
                            'MainResourceServerResponseTime':{'en':{'rule':'Reduce Server Response Time',
                                                               'description':'This rule detects that your server response time is above 200 ms.\
                                                                Server response time measures how long it takes to load the necessary HTML to begin rendering \
                                                                the page from your server, subtracting out the network latency between Google and your server. \
                                                                There may be variance from one run to the next, but the differences should not be too large. \
                                                                In fact, highly variable server response time may indicate an underlying performance issue.\
                                                                '},
                                                         'pt':{'rule':'Reduzir Tempo de Resposta do Servidor',
                                                               'description':'Esta regra detecta que o tempo de resposta do servidor é superior a 200 ms.\
                                                                O tempo de resposta do servidor mede quanto tempo ele leva para carregar o HTML necessário \
                                                                para começar a processar a página de seu servidor, subtraindo o tempo de latência de rede \
                                                                entre o Google e seu servidor. Pode haver variação entre as execuções, mas as diferenças não \
                                                                são muito grandes. Na verdade, tempos de resposta do servidor altamente variáveis podem indicar \
                                                                um problema de desempenho subjacente. \
                                                               '},
                                                         },
                                            'MinifyCss':{'en':{'rule':'Minify CSS',
                                                               'description':'This rule detects that the size of one of your CSS could be reduced through minification.\
                                                                Minification refers to the process of removing unnecessary or redundant data without affecting \
                                                                how the resource is processed by the browser - e.g. code comments and formatting, removing unused \
                                                                code, using shorter variable and function names, and so on. \
                                                                '},
                                                         'pt':{'rule':'Minificar CSS',
                                                               'description':'Esta regra detecta que é possível diminuir o tamanho dos seus recursos CSS por meio \
                                                                de minificação. A minificação é o processo de remover dados desnecessários ou redundantes sem afetar \
                                                                o processamento do recurso pelo navegador. Por exemplo, a formatação e os comentários de códigos, os \
                                                                códigos sem uso, a redução dos nomes de variáveis e funções etc.'},
                                                         },
                                        'MinifyHTML':{'en':{'rule':'Minify HTML',
                                                               'description':'This rule detects that the size of one of your HTML could be reduced through minification.\
                                                                Minification refers to the process of removing unnecessary or redundant data without affecting \
                                                                how the resource is processed by the browser - e.g. code comments and formatting, removing unused \
                                                                code, using shorter variable and function names, and so on.'},
                                                        'pt':{'rule':'Minificar HTML',
                                                               'description':'Esta regra detecta que é possível diminuir o tamanho do seu HTML por meio \
                                                                de minificação. A minificação é o processo de remover dados desnecessários ou redundantes sem afetar \
                                                                o processamento do recurso pelo navegador. Por exemplo, a formatação e os comentários de códigos, os \
                                                                códigos sem uso, a redução dos nomes de variáveis e funções etc.'},
                                                         },
                            'MinifyJavaScript':{'en':{'rule':'Minify Javascript',
                                                               'description':'This rule detects that the size of one of your Javascript could be reduced through minification.\
                                                                Minification refers to the process of removing unnecessary or redundant data without affecting \
                                                                how the resource is processed by the browser - e.g. code comments and formatting, removing unused \
                                                                code, using shorter variable and function names, and so on.'},
                                                        'pt':{'rule':'Minificar Javascript',
                                                               'description':'Esta regra detecta que é possível diminuir o tamanho dos seus recursos Javascript por meio \
                                                                de minificação. A minificação é o processo de remover dados desnecessários ou redundantes sem afetar \
                                                                o processamento do recurso pelo navegador. Por exemplo, a formatação e os comentários de códigos, os \
                                                                códigos sem uso, a redução dos nomes de variáveis e funções etc.'},
                                                         },
                            'MinimizeRenderBlockingResources':{'en':{'rule':'Eliminate Render Blocking JS and CSS in Above-the-Fold',
                                                               'description':'This rule detects that your HTML references a blocking external JavaScript file in \
                                                                the above-the-fold portion of your page. Before the browser can render a page it has to build the \
                                                                DOM tree by parsing the HTML markup. During this process, whenever the parser encounters a script \
                                                                it has to stop and execute it before it can continue parsing the HTML. In the case of an external \
                                                                script the parser is also forced to wait for the resource to download, which may incur one or more \
                                                                network roundtrips and delay the time to first render of the page'},
                                                         'pt':{'rule':'Eliminar JS e CSS que Bloqueiam Renderização do Above-the-Fold',
                                                               'description':'Esta regra detecta que seu HTML faz referência a um arquivo JavaScript externo de \
                                                                bloqueio na região acima da dobra da página. Antes de renderizar uma página, o navegador precisa \
                                                                criar a árvore DOM analisando a marcação HTML. Durante esse processo, sempre que o analisador \
                                                                encontrar um script, ele tem que parar e executá-lo antes de continuar analisando o HTML. No caso \
                                                                de um script externo, o analisador também é forçado a aguardar o download do recurso, que pode ter \
                                                                uma ou mais viagens de ida e volta da rede e atrasar a primeira renderização da página. '},
                                                         },
                                        'OptimizeImages':{'en':{'rule':'Optimize Images',
                                                               'description':'This rule detects that the images on the page can be optimized to reduce their filesize \
                                                                without significantly impacting their visual quality. Images often account for most of the downloaded \
                                                                bytes on a page. As a result, optimizing images can often yield some of the largest byte savings and \
                                                                performance improvements: the fewer bytes the browser has to download, the less competition there is \
                                                                for the client\'s bandwidth and the faster the browser can download and render content on the screen.'},
                                                         'pt':{'rule':'Otimizar Imagens',
                                                               'description':'Esta regra detecta que as imagens na página podem ser otimizadas para reduzir o tamanho \
                                                                do arquivo sem afetar significativamente a qualidade visual. Em geral, as imagens correspondem à \
                                                                maioria dos bytes transferidos por download em uma página. Como resultado, muitas vezes a otimização \
                                                                de imagens pode gerar algumas das maiores economias de bytes e melhorias de desempenho: quanto menos \
                                                                bytes o navegador tiver que transferir por download, menor será a disputa pela a largura de banda do \
                                                                cliente e mais rápido o navegador poderá fazer download e renderizar o conteúdo na tela.'},
                                                         },
                    
                            'PrioritizeVisibleContent':{'en':{'rule':'Reduce HTML to Render the Above-the-Fold',
                                                               'description':'This rule detects that additional network round trips are required to render the above \
                                                                the fold content of the page. If the amount of data required exceeds the initial congestion window \
                                                                (typically 14.6kB compressed), it will require additional round trips between your server and the \
                                                                user’s browser. For users on networks with high latencies such as mobile networks this can cause \
                                                                significant delays to page loading.'},
                                                         'pt':{'rule':'Reduzir o HTML de Renderização do Above-the-Fold',
                                                               'description':'Esta regra detecta os movimentos de ida e volta adicionais na rede que são necessários \
                                                                para processar o conteúdo da região acima da dobra na página. Se a quantidade de dados necessária \
                                                                ultrapassar a janela de congestionamento inicial (em geral, 14,6 KB compactados), serão necessários \
                                                                ciclos adicionais de envio entre o servidor e o navegador do usuário. Para usuários em redes com \
                                                                latências altas, como as redes móveis, isso pode causar atrasos significativos no carregamento da \
                                                                página.'},
                                                        },
                            'FirstContentfulPaint':{'en':{'rule':'First Contentful Paint',
                                                               'description':'<span style="font-size:12px"><i>FCP measures when a user sees a visual response from the \
                                                                page. Faster times are more likely to keep users engaged.</i></span>'},
                                                         'pt':{'rule':'First Contentful Paint',
                                                               'description':'<span style="font-size:12px"><i>O FCP mede quando um usuário vê uma resposta visual da \
                                                                página. Com respostas mais rápidas, há mais chances de manter os usuários envolvidos.</i></span>'},
                                                         },
                            'DOMContentLoadedEventFired':{'en':{'rule':'DOM Content Loaded Event Fired',
                                                               'description':'DOM Content Loaded measures when HTML document has been loaded and parsed. Faster\
                                                                times have been shown to correlate with lower bounce rates.'},
                                                         'pt':{'rule':'Evento DOM Content Loaded Disparado',
                                                               'description':'O DOM Content Loaded mede quando o documento foi carregado e parseado. Tempo mais\
                                                                curto tem correlação com menores taxas de rejeição.'},
                                                         },
                            },
}

dict_texts = {'text1':{
                        'en':'<span style="font-size:12px"><i><b>%s</b> Score had a major change of <span style="color:%s;">%s</span> points',
                        'pt':'<span style="font-size:12px"><i>O score da regra <b>%s</b> teve a maior mudança, de <span style="color:%s;">%s</span> pontos',
                        },
                    }


traffic_types = ['desktop','mobile']
prior_changes = []
file_emailtext = []

for url_id in url_ids:
    url_dict = {}
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    for traffic_type in traffic_types:
        text = ''
        cursor.execute("select * from pagespeed where (url_id,device)=(%s,%s) order by date desc limit 0,2;" , (url_id, traffic_type))
        results = cursor.fetchall()
        siteurl = results[0]['url']
        domain = ''
        variable = ''
        var_type = ''
        analysis = 'days'
        dates = []
        logging.info("Analyzing %s %s" %(siteurl, traffic_type))

        #get values for each metric analyzed
        try:
            day0 = results[1]
            day1 = results[0]
            date0 = day0['date']
            date1 = day1['date']
        except:
            logging.info("No dates to compare for %s %s. Proceding to next url..." %(traffic_type, siteurl))
            continue

        # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
        cursor.execute("select pagespeed from alerts_analysis_history where url_id = '%s';" %url_id)
        last_alert_date = cursor.fetchall()
        if last_alert_date != ():
            last_alert_date = last_alert_date[0]['pagespeed']         #gets the last date from the alerts sent in past
            if last_alert_date != None:
                last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
                try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                    email_alert_id = last_alert_date[email_group_id].split('|')[0]
                    last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                    if last_analyzed_date == str(date1):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                        cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                        sent_date = cursor.fetchall()[0]['sent_date']
                        logging.info("There is already an email alert sent to %s about Pagespeed data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                        break
                except:
                    pass

        # ------------------------------ RUNNING THE ANALYSIS ----------------------------------------
        #Optimization score
        try:
            score0 = float(day0['score'])
            score1 = float(day1['score'])
            score_absdelta = score1 - score0
            try:
                score_percdelta = (score1/score0)-1
            except:
                if score1 == score0:
                    score_percdelta = 0
                else:
                    score_percdelta = float("inf")

            #checks the score to determine the conditions to send email
            if abs(score_absdelta) > 8:
                 type_alert = ["pagespeed score", traffic_type, '', False]
                 if score_absdelta < 0:
                     sign = '-'
                     type_alert[2] = 'down'
                 else:
                     sign = '+'
                     type_alert[2] = 'up'
                 if abs(score_absdelta) > 30:
                     type_alert[3] = True
                 logging.info("Change found: %s" %type_alert)

                 reasons = {}
                 reasons_graph = {}
                 for coluna in colunas:
                     rulescore0 = float(day0[coluna])
                     rulescore1 = float(day1[coluna])
                     try:
                         value = rulescore1 - rulescore0
                         reasons[coluna] = value
                         reasons_graph[coluna] = abs(rulescore1)
                     except:
                         pass
                 if score_absdelta < 0:
                    mainreason = max(reasons, key=reasons.get)
                    sign = '-'
                    color = 'red'
                 else:
                    mainreason = min(reasons, key=reasons.get)
                    sign = '+'
                    color = 'green'

                 if score_percdelta != float("inf"):
                     text += get_comparison_phrases(siteurl, traffic_type.title() + ' Pagespeed Score', score0, date0, score1, date1, sign, color, abs(score_percdelta), type_alert, float, 'singular')
                     text += dict_texts['text1'][language] %(dict_colunas['semantic'][mainreason][language]['rule'],color,'{:0,.2f}'.format(reasons[mainreason]))
                     text += '<br>' + dict_colunas['semantic'][mainreason][language]['description'] + '</i></span><br>'
                 else:
                     text += get_comparison_phrases_zero(siteurl, traffic_type.title() + ' Pagespeed Score', date0, score1, date1, color, float)                     
                 text += '<br><img src="cid:Graph%s.png"><br>' %n
                 alerts_summary[url_id].append(type_alert)

                 criterias_graph(reasons_graph)
                 n += 1
        except:
            logging.info("No data to compare Score for %s %s. Proceding to next url..." %(traffic_type, siteurl))
    
        #FCP
        try:
            fcp0 = int(day0['FirstContentfulPaint'])
            fcp1 = int(day1['FirstContentfulPaint'])
            fcp_absdelta = fcp1 - fcp0
            try:
                fcp_percdelta = (fcp1/fcp0)-1
            except:
                if fcp1 == fcp0:
                    fcp_percdelta = 0
                else:
                    fcp_percdelta = float("inf")
            #checks the FCP to determine the conditions to send email
            if abs(fcp_percdelta) > 0.05 and fcp1 != 0:
                 type_alert = ["pagespeed FCP", traffic_type, '', False]
                 if fcp_absdelta < 0:
                     sign = '-'
                     color = 'green'
                     type_alert[2] = 'down'
                 else:
                     sign = '+'
                     color = 'red'
                     type_alert[2] = 'up'
                 if abs(fcp_percdelta) > 0.3:
                     type_alert[3] = True
                 logging.info("Change found: %s" %type_alert)

                 if fcp_percdelta != float("inf"):
                     text += get_comparison_phrases(siteurl, traffic_type.title() + ' First Contentful Paint', fcp0, date0, fcp1, date1, sign, color, abs(fcp_percdelta), type_alert, int, 'singular')
                 else:
                     text += get_comparison_phrases_zero(siteurl, traffic_type.title() + ' First Contentful Paint', date0, fcp1, date1, color, int)                     
                 alerts_summary[url_id].append(type_alert)
        except:
            logging.info("No dates to compare FCP for %s %s. Proceding to next url..." %(traffic_type, siteurl))


        #DOM loaded
        try:
            dcl0 = int(day0['DOMContentLoadedEventFired'])
            dcl1 = int(day1['DOMContentLoadedEventFired'])
            dcl_absdelta = dcl1 - dcl0
            try:
                dcl_percdelta = (dcl1/dcl0)-1
            except:
                if dcl1 == dcl0:
                    dcl_percdelta = 0
                else:
                    dcl_percdelta = float("inf")
            #checks the DCL analyzed to determine the conditions to send email
            if abs(dcl_percdelta) > 0.05 and dcl1 != 0:
                 type_alert = ["pagespeed DCL" , traffic_type, '', False]
                 if dcl_absdelta < 0:
                     sign = '-'
                     color = 'green'
                     type_alert[2] = 'down'
                 else:
                     sign = '+'
                     color = 'red'
                     type_alert[2] = 'up'
                 if abs(dcl_percdelta) > 0.3:
                     type_alert[3] = True
                 logging.info("Change found: %s" %type_alert)

                 if dcl_percdelta != float("inf"):
                     text += get_comparison_phrases(siteurl, traffic_type.title() + ' DOM Content Loaded', dcl0, date0, dcl1, date1, sign, color, abs(dcl_percdelta), type_alert, int, 'singular')
                     #text += dict_colunas['semantic']['DOMContentLoadedEventFired'][language]['description']
                 else:
                     text += get_comparison_phrases_zero(siteurl, traffic_type.title() + ' DOM Content Loaded', date0, dcl1, date1, color, int)                     

                 alerts_summary[url_id].append(type_alert)
        except:
            logging.info("No dates to compare DCL for %s %s. Proceding to next url..." %(traffic_type, siteurl))

        if text != '':
            file_emailtext.append(text)
            prior_changes.append(max(score_percdelta, fcp_percdelta, dcl_percdelta))
            dict_urls[url_id] = str(date1)
            analyzed_urls[execute_file[2]] = dict_urls 

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
if file_emailtext != []:
    #sorts changes from most negative to most positive
    file_emailtext = sort_email_from_list(prior_changes, file_emailtext)
    file_emailtext = "".join(file_emailtext)

    title = title_to_email_section('Pagespeed Insights','change')
    file_emailtext = title + file_emailtext
else:
    file_emailtext = ''
    logging.info("No data sent to email")
