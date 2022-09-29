#!/usr/bin/env python
# -*- coding: utf-8 -*-
#imports all the libraries from calling script
from __main__ import *
from TEST_INFO import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

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
table_name, script_type = 'headers', 'alerts'
url_ids = get_url_ids('seo_crawl','SEO Tags')
url_ids = list(set(url_ids) & set(allowed_url_ids))

#dictionary used to make the email more semantic
dict_headers = {'semantic':{'en':{
                                'age':'The Age header contains the time in seconds the object has been in a proxy cache',
                                'cache-control':'The Cache-Control general-header field is used to specify directives for caching mechanisms in both \
                                                requests and responses. Caching directives are unidirectional, meaning that a given directive in a request \
                                                is not implying that the same directive is to be given in the response.',
                                'expires':'The Expires header contains the date/time after which the response is considered stale.',
                                'last-modified':'The Last-Modified response HTTP header contains the date and time at which the origin server believes the \
                                                resource was last modified. It is used as a validator to determine if a resource received or stored is the \
                                                same. Less accurate than an ETag header, it is a fallback mechanism. Conditional requests containing \
                                                If-Modified-Since or If-Unmodified-Since headers make use of this field.',
                                'etag':'The ETag HTTP response header is an identifier for a specific version of a resource. It allows caches to be more efficient,\
                                        and saves bandwidth, as a web server does not need to send a full response if the content has not changed. On the other side,\
                                        if the content has changed, etags are useful to help prevent simultaneous updates of a resource from overwriting each other \
                                        ("mid-air collisions").',
                                'accept-encoding':'The Accept-Encoding request HTTP header advertises which content encoding, usually a compression algorithm, the \
                                                   client is able to understand. Using content negotiation, the server selects one of the proposals, uses it and \
                                                   informs the client of its choice with the Content-Encoding response header.',
                                'set-cookie':'The Set-Cookie HTTP response header is used to send cookies from the server to the user agent',
                                'access-control-allow-origin':'The Access-Control-Allow-Origin response header indicates whether the response can be \
                                                                shared with resources with the given origin.',
                                'content-type':'The Content-Type entity header is used to indicate the media type of the resource. In responses, a Content-Type \
                                                header tells the client what the content type of the returned content actually is. Browsers will do MIME sniffing \
                                                in some cases and will not necessarily follow the value of this header; to prevent this behavior, the header \
                                                X-Content-Type-Options can be set to nosniff.',
                                'x-content-type-options':'The X-Content-Type-Options response HTTP header is a marker used by the server to indicate that the MIME \
                                                          types advertised in the Content-Type headers should not be changed and be followed. This allows to opt-out \
                                                          of MIME type sniffing, or, in other words, it is a way to say that the webmasters knew what they were doing.',
                                'strict-transport-security':'The HTTP Strict-Transport-Security response header (often abbreviated as HSTS)  lets a web site tell \
                                                            browsers that it should only be accessed using HTTPS, instead of using HTTP',
                                'vary':'The Vary HTTP response header determines how to match future request headers to decide whether a cached response can be \
                                        used rather than requesting a fresh one from the origin server. It is used by the server to indicate which headers it \
                                        used when selecting a representation of a resource in a content negotiation algorithm. The Vary header should be set on \
                                        a 304 Not Modified response exactly like it would have been set on an equivalent 200 OK response.',
                                'content-length':'The Content-Length entity header is indicating the size of the entity-body, in bytes, sent to the recipient.',
                                'pragma':'The Pragma HTTP/1.0 general header is an implementation-specific header that may have various effects along the \
                                          request-response chain. It is used for backwards compatibility with HTTP/1.0 caches where the Cache-Control HTTP/1.1 \
                                          header is not yet present.',
                                'server':'The Server header contains information about the software used by the origin server to handle the request. Overly long \
                                          and detailed Server values should be avoided as they potentially reveal internal implementation details that might make \
                                          it (slightly) easier for attackers to find and exploit known security holes.',
                                'connection':'The Connection general header controls whether or not the network connection stays open after the current transaction \
                                              finishes. If the value sent is keep-alive, the connection is persistent and not closed, allowing for subsequent \
                                              requests to the same server to be done.',
                                

                                },
                            
                            'pt':{
                                'age':'O header Age contém o tempo em segundos em que um objeto está em um proxy de cache',
                                'cache-control':'O header Cache-Control é usado para especificar diretrizes para mecanismos de cacheamento tanto em requisições \
                                                como em respostas. As diretrizes de cacheamento são unidirecionais, o que significa que uma dada diretriz em requisição \
                                                não vai ser necessariamente dada na respostas retornada.',
                                'expires':'O header Expires contém a data/hora a partir da qual a resposta será considerada obsoleta.',
                                'last-modified':'O header de resposta Last-Modified contém a data e hora em que o servidor de origem acredita que o recurso \
                                                tenha sido modificado pela última vez. É usualmente usado como validador para determinar se uma resposta recebida ou \
                                                armazenada é a mesma. Menos preciso que o header ETag, é um mecanismo de fallback. Requisições condicionalis contendo \
                                                headers If-Modified-Since ou If-Unmodified-Since fazem uso desse campo.',
                                'etag':'O header de resposta ETag é um identificador de uma versão específica de um recurso. Ele permite que o cacheamento seja mais eficiente,\
                                        e economize banda, já que o servidor web não precisa enviar uma resposta completa se o conteúdo não mudou. Por outro lado,\
                                        se o conteúdo mudou, as etags são úteis para prevenir que atualizações simultâneas de um recurso sobreescrevem umas as outras \
                                        ("mid-air collisions").',
                                'accept-encoding':'O header Accept-Encoding adverte qual encoding de conteúdo, normalmente um algoritmo de compressão, o \
                                                   cliente é capaz de entender. Usando negociação de conteúdo, o servidor seleciona uma das propostas, usa ela e \
                                                   informa ao cliente de sua escolha com o header de resposta Content-Encoding.',
                                'set-cookie':'O header de resposta Set-Cookie HTTP é usado para enviar cookies do servidor para o user-agent',
                                'access-control-allow-origin':'O header de resposta Access-Control-Allow-Origin indica se a resposta pode ser compartilhada \
                                                                com recursos da origem dada.',
                                'content-type':'O entity header Content-Type é usado para indicar o tipo de mídia do recurso. Em respostas, um header Content-Type \
                                                diz ao cliente de qual o tipo o conteúdo retornado realmente é. Os navegadores farão MIME sniffing em alguns casos \
                                                e não vão necessariamente seguir o valor desse header; para prevenir esse comportamento, o header \
                                                X-Content-Type-Options pode ser configurado para nosniff.',
                                'x-content-type-options':'O header de resposta X-Content-Type-Options é um marcador usado pelo servidor para indicar que os tipos de MIME \
                                                          apontados nos headers Content-Type não devem ser alterados e devem ser seguidos. Isso elimina a possibilidade \
                                                          de MIME sniffing, ou, em outras palavras, é um jeito de dizer que os gerenciadores do site sabem o que estão fazendo.',                                
                                'strict-transport-security':'O header de resposta Strict-Transport-Security (usualmente abreviado como HSTS)  permite que um site \
                                                            comunique aos navegadores que ele só deve ser acessado por meio deHTTPS, ao invés de HTTP',
                                'vary':'O header de resposta Vary determina qual deve ser a correspondência de headers de requisições futuras para decidir se uma resposta de cache \
                                        pode ser usada ao invés de se realizar uma nova requisição de conteúdo do servidor de origem. É usado pelo servidor para indicar quais headers \
                                        ele usou para selecionar a representação de algum recurso em um algoritmo de negociação de conteúdo. O Vary deve ser configurado para \
                                        uma resposta 304 Not Modified exatamente como seria em uma resposta equivalente 200 OK.',
                                'content-length':'O header Content-Length indica o tamanho do corpo da entidade, em bytes, enviado ao recipiente.',
                                'pragma':'O header Pragma é um header de implementação específica que pode ter vários efeitos ao longo da cadeia de respostas. \
                                          Ele é usado para compatibilidades retroativas com caches de HTTP/1.0 onde o header Cache-Control HTTP/1.1 \
                                          ainda não está presente.',
                                'server':'O header server contém informações sobre o software usado pelo servidor de origem para lidar com a requisição. Valores \
                                          muito longos e detalhados para o server devem ser evitados, pois eles podem potencialmente revelar detalhes de implementações internas \
                                          que podem tornar (ligeiramente) mais fácil para atacantes encontrarem e explorarem falhas de segurança conhecidas.',
                                'connection':'O header Connection controla se uma conexão deve permanecer aberta após o fim de uma transação corrente. \
                                              Se o valor enviado for keep-alive, a conexão persiste e não é fechada, permitindo que requisições subsequentes \
                                              para o mesmo servidor sejam feitas.',

                                },
                            },
                
                 'links':{'age':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/age',
                          'cache-control':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/cache-control',
                          'expires':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/expires',
                          'last-modified':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/last-modified',
                          'etag':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/etag',
                          'accept-encoding':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/accept-encoding',
                          'set-cookie':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/set-cookie',
                          'access-control-allow-origin':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/access-control-allow-origin',
                          'content-type':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/content-type',
                          'x-content-type-options':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/x-content-type-options',
                          'strict-transport-security':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/strict-transport-security',
                          'vary':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/vary',
                          'content-length':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Length',
                          'pragma':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/pragma',
                          'server':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server',
                          'connection':'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Connection',

                         }
                }

dict_texts = {'text1':{
                        'en':'<p style="font-size:20px"><b>The following URLs headers had changes detected from last Simplex SEO Crawl to %s</b></p>',
                        'pt':'<p style="font-size:20px"><b>Os headers das URLs seguintes tiveram alterações se compararmos o último rastreamento da Simplex com o dia %s</b></p>',
                       },
              'text2':{
                        'en':'<br>Sites using HTTPS should have a HSTS directive to enhance their protection',
                        'pt':'<br>Sites que utilizam HTTPS devem ter uma diretriz de HSTS para aumentar sua proteção',
                       },
            }

main_headers = ['age', 'cache-control', 'expires', 'last-modified', 'etag', 'accept-encoding', 'set-cookie', 'access-control-allow-origin',
'content-type', 'x-content-type-options', 'strict-transport-security', 'vary', 'content-length', 'pragma', 'server', 'connection']
                
file_emailtext = ''

for url_id in url_ids:
    url_dict = {}
    url_text = ''
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute('select url,date,headers from seo_monitoring where (url_id, type) = (%s, "Desktop Javascript Rendered") order by date desc limit 0,2;', [url_id])
    #gets last date values
    results = cursor.fetchall()
    if len(results) == 0:
        logging.info("No data present for %s..." %siteurl)
        continue
    siteurl = results[0]['url']
    logging.info("Analyzing %s..." %siteurl)
    try:
        currentdate = results[0]['date']
        lastdate = results[1]['date']
    except:
        logging.info("No dates to compare for %s. Proceding to next url..." %siteurl)
        continue

    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select headers from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['headers']         #gets the last date from the alerts sent in past
        if last_alert_date != None:
            last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
            try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                email_alert_id = last_alert_date[email_group_id].split('|')[0]
                last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                if last_analyzed_date == str(currentdate):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                    cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                    sent_date = cursor.fetchall()[0]['sent_date']
                    logging.info("There is already an email alert sent to %s about SEO data collected for %s in %s. \
    This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, currentdate, sent_date))
                    #continue
            except:
                pass

    current_headers = yaml.load(results[0]['headers'])
    last_headers = yaml.load(results[1]['headers'])

    current_headers_list= [x.lower() for x in current_headers.keys()]
    last_headers_list = [x.lower() for x in last_headers.keys()]

    sys.exit()
    print(current_headers_list)
    print(last_headers_list)


    #cookies
    #for item in cookies_dict: #response.cookies:
    #   item.name
    #   item.value
    #   item.secure
    #   item.domain
    #   item.domain_initial_dot
    #   item.domain_specified
    #   item.expires
    #   item.path_specified
    #   item.path
    #   item.port_specified
    #   item.port
    #   item.rfc2109
    #   item.secure
    #   item.set_nonstandard_attr
    #   item.version
    
    for key_lower, key in zip(current_headers_list, current_headers.keys()):
        if key_lower not in main_headers:
            continue        
        if key_lower not in last_headers_list:
            url_text += "<br>The header <b>%s</b> is not present anylonger" %key_lower
            if key_lower in dict_headers['semantic'][language].keys():
                url_text += dict_headers['semantic'][language][key_lower] + '<br>'
        elif key_lower not in ['date']:
            current_value = current_headers[key]
            last_value = last_headers[key]
            if current_value != last_value:
                url_text += '<br>The header <b>%s</b> value has changed from <span style="color:red">%s</span> to <span style="color:green">%s</span>' %(key, last_value, current_value)
                

    if 'https' in siteurl and 'strict-transport-security' not in current_headers:
        url_text += dict_texts['text2'][language]

    if url_text != '':
        url_text += '<br>'
    if url_text != '':
        url_text = '<br><a href="%s"><b>%s</b></a>' %(siteurl, siteurl) + url_text 
    
    file_emailtext += url_text 

    #sys.exit()
    if file_emailtext != '':
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 
    
#email sending part
if file_emailtext != '':
    title = title_to_email_section('URL Headers','change')
    file_emailtext = title + file_emailtext
    test_email(file_emailtext)
else:
    logging.info("No data sent to email")
