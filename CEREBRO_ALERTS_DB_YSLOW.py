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

    mean_length = int(numpy.mean([len(i) for i in criteria_names])*0.4)      #gets every column name length to define a mean column length as integer value
    wrapped_text = ["\n".join(textwrap.wrap(i,mean_length)) for i in criteria_names]    #breaks text in the column length defined above to make the axis good to read

    plt.figure(figsize=(len(criteria_names)*0.9, 2)) #fig size in x and y direction
    plt.margins(0.005, 0)
    plt.rcParams['axes.facecolor'] = 'w'

    random_color = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))

    #plots bar graph of criteria_name and its values. x is created as a list from 0 to len(criteria_names) to make it work as x axis
    x = numpy.arange(len(criteria_names))
    plt.bar(x, criteria_values, width = 0.4, color = random_color)  #uses random color for each graph
    plt.xticks(x, wrapped_text, rotation = 45, ha ='right', rotation_mode = 'anchor', fontsize = 7)    #enables ploting float vs string
    plt.title(graph_title , color = 'navy', fontsize = 10, fontweight='bold')

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

# -------------------------- YSLOW ANALYSIS --------------------------------
table_name, script_type = 'yslow', 'alerts'
url_ids = get_url_ids('yslow','Yslow')
url_ids = list(set(url_ids) & set(allowed_url_ids))

#gets all the columns to compare data
colunas = ['ynumreq', 'ycdn', 'yemptysrc', 'yexpires', 'ycompress', 'ycsstop', 'yjsbottom', 'yexpressions', 'yexternal', 'ydns', 'yminify', 'yredirects', 'ydupes', \
           'yetags', 'yxhr', 'yxhrmethod', 'ymindom', 'yno404', 'ymincookie', 'ycookiefree', 'ynofilter', 'yimgnoscale', 'yfavicon', 'details']

dict_colunas = {'semantic':{'ynumreq':{'en':{'rule':'Make Fewer HTTP Requests',
                                                               'description':'80% of the end-user response time is spent on the front-end. Most of this time is tied \
                                                                up in downloading all the components in the page: images, stylesheets, scripts, Flash, etc. Reducing \
                                                                the number of components in turn reduces the number of HTTP requests required to render the page. \
                                                                This is the key to faster pages.'
                                                               },
                                                         'pt':{'rule':'Fazer Menos Requisi????es HTTP',
                                                               'description':'80% do tempo de resposta ao usu??rio final ?? gasto no front-end. A maior parte desse tempo \
                                                                ?? para fazer o download de todos os componentes na p??gina: imagens, CSS, scripts, Flash, etc. Reduzindo \
                                                                o n??mero de componentes tamb??m reduz o n??mero de requisi????es HTTP necess??rias para renderizar a p??gina. \
                                                                Essa ?? a chave para p??ginas mais r??pidas.'
                                                               },
                                                         },
                                        'ycdn':{'en':{'rule':'Use a CDN',
                                                               'description':'The user\'s proximity to your web server has an impact on response times. Deploying your \
                                                               content across multiple, geographically dispersed servers will make your pages load faster from the \
                                                               user\'s perspective.'
                                                               },
                                                         'pt':{'rule':'Usar um CDN',
                                                               'description':'A proximidade do usu??rio com seu servidor tem um impacto no tempo de resposta. Disponibilizando \
                                                               conte??do atrav??s de m??ltiplos servidores, geograficamente dispersos faz com que suas paginas carreguem mais r??pido \
                                                               na perspectiva do usu??rio.'
                                                               },
                                                         },
                                        'yemptysrc':{'en':{'rule':'Avoid Empty src or href',
                                                               'description':'Tags with empty source may cause pointless aditional requests in some browsers'
                                                               },
                                                         'pt':{'rule':'Evitar src ou href Vazios',
                                                               'description':'Tags com src vazio podem ocasionar requisi????es adicionais sem sentido em alguns browsers'
                                                               },
                                                         },
                                        'yexpires':{'en':{'rule':'Add Expires Headers',
                                                               'description':'Web page designs are getting richer and richer, which means more scripts, stylesheets, \
                                                                images, and Flash in the page. A first-time visitor to your page may have to make several HTTP \
                                                                requests, but by using the Expires header you make those components cacheable. This avoids \
                                                                unnecessary HTTP requests on subsequent page views. Expires headers are most often used with images, \
                                                                but they should be used on all components including scripts, stylesheets, and Flash components. \
                                                                Browsers (and proxies) use a cache to reduce the number and size of HTTP requests, making web pages \
                                                                load faster. A web server uses the Expires header in the HTTP response to tell the client how long a \
                                                                component can be cached.'
                                                               },
                                                         'pt':{'rule':'Adicionar Header \'Expires\'',
                                                               'description':'O design de p??ginas da Web tem ficado cada vez mais rico, o que significa mais scripts, CSS, \
                                                                imagens, e Flash na p??gina. Um visitante de primeiro acesso a sua p??gina pode precisar fazer v??rias requisi????es \
                                                                HTTP, mas usando o header Expires voc?? pode tornar esses componentes cache??veis. Isso evita requisi????es\
                                                                HTTP desnecess??rias em pageviews subsequentes. O header Expires ?? utilizado com mais frequ??ncia com imagens, \
                                                                mas ele deve ser usado em todos os componentes como scripts, folhas de estilo, e componentes Flash. \
                                                                Os Browsers (e proxies) fazem cache para reduzir o n??mero e tamanho das requisi????es HTTP, fazendo as p??ginas \
                                                                carregarem mais r??pido. Um servidor web usa o header Expires na resposta HTTP para dizer ao cliente por quanto \
                                                                tempo um componente pode ser cacheado.'
                                                               },
                                                         },
                                        'ycompress':{'en':{'rule':'Compress Components With GZip',
                                                               'description':'Gzipping generally reduces the response size by about 70%. Approximately 90% of \
                                                                today\'s Internet traffic travels through browsers that claim to support gzip.'
                                                               },
                                                         'pt':{'rule':'Comprimir Componentes com GZip',
                                                               'description':'Compactando arquivos em Gzip geralmente reduz o tamanho da resposta em 70%. Aproximadamente 90% \
                                                                do tr??fego da Internet de hoje viaja atrav??s de navegadores que suportam o uso de gzip.'
                                                               },
                                                         },
                                        'ycsstop':{'en':{'rule':'Put CSS at Top',
                                                               'description':'When the browser loads the page progressively the header, the navigation bar, the logo \
                                                                at the top, etc. all serve as visual feedback for the user who is waiting for the page. This improves \
                                                                the overall user experience. Putting stylesheets in the HEAD allows this kind of rendering behavior'
                                                               },
                                                         'pt':{'rule':'Colocar CSS no Topo',
                                                               'description':'Quando o browser carrefa progressivamente o header, o menu de navega????o, o logo \
                                                                no come??o na p??gina, etc. tudo serve como um retorno visual para o usu??rio que espera pela p??gina. Isso\
                                                                melhora a experi??ncia em geral. Colocar os CSS permite esse comportamento na renderiza????o'
                                                               },
                                                         },
                                        'yjsbottom':{'en':{'rule':'Put JavaScript at Bottom',
                                                               'description':'The problem caused by scripts is that they block parallel downloads. The HTTP/1.1 specification \
                                                                suggests that browsers download no more than two components in parallel per hostname. If you serve your images \
                                                                from multiple hostnames, you can get more than two downloads to occur in parallel. While a script is downloading,\
                                                                however, the browser won\'t start any other downloads, even on different hostnames.'
                                                               },
                                                         'pt':{'rule':'Colocar JavaScript no Fim',
                                                               'description':'O problema causado pelos scripts ?? que eles bloqueiam downloads paralelos. A especifica????o do HTTP/1.1\
                                                                sugere que o browser n??o fa??am download de mais de 2 componentes em paralelo por hostname. Servir imagens por multiplos\
                                                                hostnames, por exemplo, permite que voc?? tenha mais de 2 downloads em paralelo. Entretanto, quando um javascript ?? baixado,\
                                                                os browser n??o fazem nenhum outro download, mesmo em hostnames diferentes.'
                                                               },
                                                         },
                                        'yexpressions':{'en':{'rule':'Avoid CSS Expressions',
                                                               'description':'The problem with expressions is that they are evaluated more frequently than most people expect. Not only \
                                                                are they evaluated when the page is rendered and resized, but also when the page is scrolled and even when the user moves \
                                                                the mouse over the page. One way to reduce the number of times your CSS expression is evaluated is to use one-time \
                                                                expressions, where the first time the expression is evaluated it sets the style property to an explicit value, which \
                                                                replaces the CSS expression. If the style property must be set dynamically throughout the life of the page, using event \
                                                                handlers instead of CSS expressions is an alternative approach.'
                                                               },
                                                         'pt':{'rule':'Evitar Express??es CSS',
                                                               'description':'O problema com express??es ?? que elas s??o calculadas mais frequentemente do que a maioria das pessoas espera. \
                                                                Elas n??o s??o apenas calculadas quando a p??gina ?? renderizada e redimensionada, mas tamb??m quando se faz scroll na p??gina \
                                                                ou se mexe o mouse sobre ela. Um jeito de reduzir o n??mero de vezes que a express??o CSS ?? calculada ?? usar express??es \
                                                                uma ??nica vez, onde ap??s o c??lculo sejam definidos valores expl??citos de propriedades de estilo que substituem a express??o \
                                                                CSS. Se a propriedade de estilo precisar ser definida de forma din??mica ao longo da utiliza????o da p??gina, utilizar event \
                                                                handlers no lugar de express??es CSS ?? uma boa alternativa.'
                                                               },
                                                         },
                                        'yexternal':{'en':{'rule':'Make JavaScript and CSS External',
                                                               'description':'Using external files generally produces faster pages because the JavaScript and CSS files \
                                                                are cached by the browser. JavaScript and CSS that are inlined in HTML documents get downloaded every time the HTML document \
                                                                is requested. This reduces the number of HTTP requests that are needed, but increases the size of the HTML document. On the \
                                                                other hand, if the JavaScript and CSS are in external files cached by the browser, the size of the HTML document is reduced \
                                                                without increasing the number of HTTP requests.'
                                                               },
                                                         'pt':{'rule':'Tornar JavaScript e CSS Externos',
                                                               'description':'Usar arquivos externos geralmente produz p??ginas mais r??pidas porque os arquivos JavaScript e CSS \
                                                                s??o cacheados pelo browser. Os inline JavaScript e CSS dos documentos HTML s??o baixados toda vez que o HTML ?? requisitado. \
                                                                Isso reduz o n??mero de requisi????es HTTP que s??o necess??rias, mas aumenta o tamanho do documento HTML. Por outro lado, \
                                                                se os JavaScript e CSS foram arquivos cacheados pelo browser, o tamanho do HTML ?? reduzido sem aumentar o n??mero de requisi????es HTTP.'
                                                               },
                                                         },
                                        'ydns':{'en':{'rule':'Reduce DNS Lookups',
                                                               'description':'The Domain Name System (DNS) maps hostnames to IP addresses, just as phonebooks map people\'s names to their \
                                                                phone numbers. When you type www.yahoo.com into your browser, a DNS resolver contacted by the browser returns that server\'s \
                                                                IP address. DNS has a cost. It typically takes 20-120 milliseconds for DNS to lookup the IP address for a given hostname. The \
                                                                browser can\'t download anything from this hostname until the DNS lookup is completed.'
                                                               },
                                                         'pt':{'rule':'Reduzir Consultas DNS',
                                                               'description':'O Domain Name System (DNS) mapeia os hostnames para endere??os de IP, assim como uma lista telef??nica mapeia pessoas \
                                                                a seus n??meros. Quando voc?? digita www.simplexanalytics.com.br no seu navegador, um resolvedor de nomes DNS contactado pelo browser \
                                                                retorna o endere??o do IP do servidor. O DNS tem um custo. Tipicamente leva entre 20 e 120 milisegundos para a consulta do IP dado um host.\
                                                                O browser n??o pode fazer nenhum download para aquele hostname at?? que a consulta DNS esteja completa.'
                                                               },
                                                         },
                                        'yminify':{'en':{'rule':'Minify JavaScript and CSS',
                                                               'description':'Minification is the practice of removing unnecessary characters from code to reduce its \
                                                                size thereby improving load times. When code is minified all comments are removed, as well as unneeded \
                                                                white space characters (space, newline, and tab).'
                                                               },
                                                         'pt':{'rule':'Minificar JavaScript e CSS',
                                                               'description':'Minifica????o ?? a pr??tica de remover caracteres desnecess??rios do codigo para reduzir seu \
                                                                tamanho e consequentemente melhorar o tempo de carregamento. Quando o c??digo ?? minificado todos os coment??rios \
                                                                s??o removidos, assim como caracteres desnecess??rios como espa??o, quebra de linha, e tabula????o.'
                                                               },
                                                         },
                                        'yredirects':{'en':{'rule':'Avoid URL Redirects',
                                                               'description':'The main thing to remember is that redirects slow down the user experience. Inserting a \
                                                                redirect between the user and the HTML document delays everything in the page since nothing in the \
                                                                page can be rendered and no components can start being downloaded until the HTML document has arrived.'
                                                               },
                                                         'pt':{'rule':'Evitar Redirecionamentos de URL',
                                                               'description':'A principal quest??o a ser lembrada ?? que redirecionamentos diminuem a experi??ncia do usu??rio.\
                                                                Inserindo um redirecionamento entre o usu??rio e o documento HTML atrasa que est?? presente na p??gina visto que \
                                                                nada pode ser renderizado e nenhum componente pode come??ar a ser baixado at?? que o documento HTML chegue.'
                                                               },
                                                         },
                                         'ydupes':{'en':{'rule':'Remove Duplicate JavaScript and CSS',
                                                               'description':'It hurts performance to include the same JavaScript file twice in one page. This isn\'t as \
                                                                unusual as you might think. One way to avoid accidentally including the same script twice is to implement \
                                                                a script management module in your templating system'
                                                               },
                                                         'pt':{'rule':'Remover JavaScript e CSS Duplicados',
                                                               'description':'?? prejudicial para a performance incluir o mesmo JavaScript mais de uma vez numa mesma p??gina. \
                                                                Esse erro ?? mais comum do que parece. Uma forma de evitar que o mesmo script seja reinserido de forma acidental \
                                                                ?? utilizar um m??dulo de gerenciamento de scripts no seu sistema'
                                                               },
                                                         },
                                         'yetags':{'en':{'rule':'Configure ETags',
                                                               'description':'Entity tags (ETags) are a mechanism that web servers and browsers use to determine whether the \
                                                                component in the browser\'s cache matches the one on the origin server. (An "entity" is another word a "component":\
                                                                images, scripts, stylesheets, etc.) ETags were added to provide a mechanism for validating entities that is more \
                                                                flexible than the last-modified date. An ETag is a string that uniquely identifies a specific version of a component. \
                                                                The only format constraints are that the string be quoted. The origin server specifies the component\'s ETag using the \
                                                                ETag response header.'
                                                               },
                                                         'pt':{'rule':'Configurar ETags',
                                                               'description':'As Entity tags (ETags) s??o um mecanismo que servidores e navegadores usam para determinar se um componente \
                                                                no cache do browser corresponde ao componente na origem. (Uma "entidade" ?? uma palavra semelhante a "componente":\
                                                                imagens, scripts, css, etc.) As ETags foram adicionadas para prover um mecanismo de valida????o que seja mais flex??vel do \
                                                                que a data last-modified. Uma ETag ?? uma string que identifica unicamente uma vers??o espec??fica de um componente. \
                                                                A ??nica restri????o de formato ?? que a string deve estar entre aspas. O servidor especifica a Etag dos componentes \
                                                                usando o header de resposta ETag.'
                                                               },
                                                         },
                                         'yxhr':{'en':{'rule':'Make AJAX cacheable',
                                                               'description':'One of the cited benefits of Ajax is that it provides instantaneous feedback to the user because it \
                                                                requests information asynchronously from the backend web server. However, using Ajax is no guarantee that the user \
                                                                won\'t be twiddling his thumbs waiting for those asynchronous JavaScript and XML responses to return. In many \
                                                                applications, whether or not the user is kept waiting depends on how Ajax is used. For example, in a web-based \
                                                                email client the user will be kept waiting for the results of an Ajax request to find all the email messages \
                                                                that match their search criteria. It\'s important to remember that "asynchronous" does not imply "instantaneous".'
                                                               },
                                                         'pt':{'rule':'Tornar AJAX cache??vel',
                                                               'description':'Um dos benef??cios mais citados do Ajax ?? que ele prov?? feedback instant??neo para o usu??rio porque ele \
                                                                requisita informa????es de forma ass??ncrona do servidor do backend. Entretanto, usar Ajax n??o garante que o usu??rio \
                                                                n??o fique ansionso em esperar a reposta ass??ncrona para esses JavaScript e XML. Em muitas aplica????es, o usu??rio \
                                                                deve ficar esperando ou n??o dependendo de como o Ajax ?? usado. Por exemplo, em um cliente de email o usu??rio \
                                                                dever?? esperar os resultados de uma requisi????o Ajax para encontrar todas as mensagens que correspondem a seu crit??rio \
                                                                de busca. ?? importante lembrar que "ass??ncrono" n??o implica em ser "instant??neo".'
                                                               },
                                                         },
                                          'yxhrmethod':{'en':{'rule':'Use GET for AJAX Requests',
                                                               'description':'When using XMLHttpRequest, POST is implemented in the browsers as a \
                                                                two-step process: sending the headers first, then sending data. So it\'s best to use GET, which only takes one TCP \
                                                                packet to send (unless you have a lot of cookies). The maximum URL length in Internet Explorer is 2K, so if you send more than 2K \
                                                                data you might not be able to use GET.'
                                                               },
                                                         'pt':{'rule':'Usar GET para Requisi????es AJAX',
                                                               'description':'Quando se faz uma XMLHttpRequest, o m??todo POST ?? implementado nos browsers como um processo de duas \
                                                                etapas: enviando primeiramente os headers, e enviando a data apos isso. Sendo assim ?? melhor usar o GET, que s?? precisa \
                                                                de um pacote TCP para envio (a n??o ser que voc?? tenha muitos cookies). A extens??o m??xima de URL no Internet Explorer ?? 2K,\
                                                                ent??o talvez se voc?? precisar enviar mais do que 2K, voc?? pode n??o ser capaz de usar o GET.'
                                                               },
                                                         },
                                          'ymindom':{'en':{'rule':'Reduce the Number of DOM Elements',
                                                               'description':'A complex page means more bytes to download and it also means slower DOM access in JavaScript. It makes a \
                                                                difference if you loop through 500 or 5000 DOM elements on the page when you want to add an event handler for example.\
                                                                A high number of DOM elements can be a symptom that there\'s something that should be improved with the markup of the\
                                                                page without necessarily removing content. Are you using nested tables for layout purposes? Are you throwing in more \
                                                                &lt;div&gt;s only to fix layout issues? Maybe there\'s a better and more semantically correct way to do your markup.'
                                                               },
                                                         'pt':{'rule':'Reduzir o N??mero de Elementos no DOM',
                                                               'description':'Uma p??gina complexa significa mais bytes para download e tamb??m significa acesso mais lento ao DOM em JavaScript.\
                                                                Faz diferen??a se voc?? fizer um loop por 500 ou 5000 elementos do DOM na p??gina quando voc?? quer adicionar um event handler por exemplo.\
                                                                Um grande n??mero de elementos DOM pode ser um sintoma de que algo deve ser melhorado com a marca????o da p??ginas sem necessariamente\
                                                                remover conte??do. Voc?? est?? usando tabelas embutidas para prop??sitos de layout? Voc?? est?? usando &lt;div&gt;s apenas para corrigir quest??es\
                                                                de layout? Talvez haja um jeito melhor e mais sem??ntico de corrigir as suas marca????es.'
                                                               },
                                                         },
                                          'yno404':{'en':{'rule':'Avoid HTTP 404 Error',
                                                               'description':'HTTP requests are expensive so making an HTTP request and getting a useless response (i.e. 404 Not Found) is totally \
                                                                unnecessary and will slow down the user experience without any benefit.'
                                                               },
                                                         'pt':{'rule':'Evitar o Status HTTP 404',
                                                               'description':'As requisi????es HTTP s??o custosas ent??o fazer uma requisi????o HTTP e receber uma resposta sem utilidade(ex: 404 N??o Encontrado) \
                                                                ?? totalmente desnecess??rio e vai deixar a experi??ncia do usu??rio mais lenta sem trazer nenhum benef??cio.'
                                                               },
                                                         },
                                          'ymincookie':{'en':{'rule':'Reduce Cookie Size',
                                                               'description':'HTTP cookies are used for a variety of reasons such as authentication and personalization. Information about cookies \
                                                                is exchanged in the HTTP headers between web servers and browsers. It\'s important to keep the size of cookies as low as possible \
                                                                to minimize the impact on the user\'s response time.'
                                                               },
                                                         'pt':{'rule':'Reduzir Tamanho de Cookies',
                                                               'description':'Os cookies HTTP s??o usados para uma variedade de raz??es, como autentica????o e personaliza????o. Informa????es sobre cookies \
                                                                s??o trocadas nos headers HTTP entre os servidores e navegadores. ?? importante manter o tamanho dos cookies o menor poss??vel \
                                                                para minimizar o impacto no tempo de resposta do usu??rio.'
                                                               },
                                                         },
                                          'ycookiefree':{'en':{'rule':'Use Cookie-Free Domains',
                                                               'description':'When the browser makes a request for a static image and sends cookies together with the request, the server \
                                                                doesn\'t have any use for those cookies. So they only create network traffic for no good reason. You should make sure static \
                                                                components are requested with cookie-free requests. Create a subdomain and host all your static components there.'
                                                               },
                                                         'pt':{'rule':'Usar Dom??nios Livres de Cookies',
                                                                'description':'Quando o browser faz uma requisi????o para um imagem est??tica e envia cookies juntos ?? requisi????o, o servidor \
                                                                n??o faz nenhum uso desses cookies. Ent??o eles apenas criam tr??fego na internet sem nenhuma raz??o. Voc?? deve garantir que \
                                                                componentes est??ticos sejam requisitados sem cookies. Crie um subdom??nio e hospede todos os seus componentes est??ticos nele.'
                                                              },
                                                         },
                                          'ynofilter':{'en':{'rule':'Avoid Alpha Image Loader Filter',
                                                               'description':'The Internet Explorer proprietary AlphaImageLoader filter aims to fix a problem with semi-transparent true color PNGs in \
                                                                IE versions < 7. The problem with this filter is that it blocks rendering and freezes the browser while the image is being \
                                                                downloaded. It also increases memory consumption and is applied per element, not per image, so the problem is multiplied.'
                                                               },
                                                         'pt':{'rule':'Evitar o Filtro Alpha Image Loader',
                                                               'description':'A propriedade filtro AlphaImageLoader no Internet Explorer visa corrigir um problema com cores semi-transparentes em PNG \
                                                                em vers??es do IE < 7. O problema com esse filtro ?? que ele bloqueia a renderiza????o e congela o navegador enquanto a imagem est?? sendo baixada.\
                                                                Ele tamb??m aumenta o consumo de mem??ria e ?? aplicado por elemento, n??o por imagem, ent??o o problema ?? multiplicado.'
                                                               },
                                                         },
                                          'yimgnoscale':{'en':{'rule':'Do Not Scale Images in HTML',
                                                               'description':'Don\'t use a bigger image than you need just because you can set the width and height in HTML. If you need\
                                                                &lt;img width="100" height="100" src="example.jpg" alt="Example Img" /&gt; \
                                                                then your image (example.jpg) should be 100x100px rather than a scaled down 500x500px image.'
                                                               },
                                                         'pt':{'rule':'N??o Alterar Escala de Imagens no HTML',
                                                               'description':'N??o use uma imagem maior do que voc?? precisa s?? porque voc?? pode configurar sua largura e altura no HTML.\
                                                                Se voc?? precisa de &lt;img width="100" height="100" src="example.jpg" alt="Example Img" /&gt; \
                                                                ent??o sua imagem (example.jpg) deve ter 100x100px ao inv??s de ser reduzida de uma imagem 500x500px.'
                                                               },
                                                         },
                                          'yfavicon':{'en':{'rule':'Make Favicon Small and Cacheable',
                                                               'description':'The favicon.ico is an image that stays in the root of your server. It\'s a necessary evil because even if \
                                                                you don\'t care about it the browser will still request it, so it\'s better not to respond with a 404 Not Found. Also \
                                                                since it\'s on the same server, cookies are sent every time it\'s requested. This image also interferes with the \
                                                                download sequence, for example in IE when you request extra components in the onload, the favicon will be downloaded \
                                                                before these extra components.'
                                                               },
                                                         'pt':{'rule':'Tornar o Favicon Pequeno e Cache??vel',
                                                               'description':'O favicon.ico ?? uma imagem que fica na raiz do seu servidor. ?? um mal necess??rio porque mesmo se voc?? n??o se importar \
                                                                com ele, o navegador ainda vai requisit??-lo, ent??o ?? melhor n??o responder com um 404. Al??m disso, como ele est?? no mesmo servidor, \
                                                                cookies s??o enviados toda vez que ele ?? requisitado. Essa imagem tamb??m interfere na sequ??ncia de download, por exemplo no Internet \
                                                                Explorer, quando voc?? requisita componentes extra atrav??s de onload, o favicon ser?? baixado antes desses componentes extra.'
                                                               },
                                                         },
                            },
                }

dict_texts = {'text1':{
                        'en':'<span style="font-size:12px"><i><b>%s</b> Score had a major change of <span style="color:%s;">%s</span> points',
                        'pt':'<span style="font-size:12px"><i>O score da regra <b>%s</b> teve a maior mudan??a, de <span style="color:%s;">%s</span> pontos',
                      },
                }

prior_changes = []
file_emailtext = []

for url_id in url_ids:
    #gets last 2 entries for the specified url
    url_dict = {}
    if url_id not in alerts_summary:
        alerts_summary[url_id] = []

    cursor.execute("select * from yslow where url_id = '%s' order by date desc limit 0,2;" %url_id)
    results = cursor.fetchall()
    siteurl = results[0]['url']
    domain = ''
    variable = ''
    var_type = ''
    analysis = 'days'
    dates = []
    try:
        day0 = results[1]
        day1 = results[0]
        date0 = day0['date']
        date1 = day1['date']
    except:
        logging.info("No dates to compare for %s. Proceding to next url..." %siteurl)
        continue
    logging.info("Analyzing %s" %siteurl)

    # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
    cursor.execute("select yslow from alerts_analysis_history where url_id = '%s';" %url_id)
    last_alert_date = cursor.fetchall()
    if last_alert_date != ():
        last_alert_date = last_alert_date[0]['yslow']         #gets the last date from the alerts sent in past
        if last_alert_date != None:
            last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
            try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
                email_alert_id = last_alert_date[email_group_id].split('|')[0]
                last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
                if last_analyzed_date == str(date1):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                    cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                    sent_date = cursor.fetchall()[0]['sent_date']
                    logging.info("There is already an email alert sent to %s about YSlow data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, date1, sent_date))
                    continue
            except:
                pass

    format_type = int
    score0 = format_type(day0['score'])
    score1 = format_type(day1['score'])
    details = {}
    text = ''
    if day1['details'] is not None:
        details = yaml.load(day1['details'])

    # ------------------------------ RUNNING THE ANALYSIS ----------------------------------------
    #absdelta and percdelta are the anomaly detectors
    absdelta = score1 - score0
    try:
        percdelta = (score1/score0)-1
    except:
        percdelta = float("inf")

    #if the test score changes more than 5 points it is considered and anomaly
    if abs(absdelta) > 6:
        type_alert = ["yslow score", '', '', False]
        if absdelta < 0:
            sign = '-'
            type_alert[2] = 'down'
        else:
            sign = '+'
            type_alert[2] = 'up'
        if abs(absdelta) > 25:
            type_alert[3] = True
        logging.info("Change found: %s" %type_alert)

        reasons = {}
        reasons_graph = {}
        for coluna in colunas:
            rulescore0 = day0[coluna]
            rulescore1 = day1[coluna]
            try:
                value = int(rulescore1) - int(rulescore0)
                reasons[coluna] = value
                reasons_graph[coluna] = 100 - int(rulescore1)
            except:
                pass
        if absdelta < 0:
            mainreason = min(reasons, key=reasons.get)
            sign = '-'
            color = 'red'
        else:
            mainreason = max(reasons, key=reasons.get)
            sign = '+'
            color = 'green'

        if percdelta != float("inf"):
            text = get_comparison_phrases(siteurl, 'Yslow Score', score0, date0, score1, date1, sign, color, abs(percdelta), type_alert, format_type, 'singular')
            text += dict_texts['text1'][language] %(dict_colunas['semantic'][mainreason][language]['rule'],color,'{:0,.2f}'.format(reasons[mainreason]))
            text += '<br>' + dict_colunas['semantic'][mainreason][language]['description'] + '</i></span>'
        else:
            text += get_comparison_phrases_zero(siteurl, 'Yslow Score', date0, score1, date1, color, float)                     
        text += '<br><img src="cid:Graph%s.png">' %n

        criterias_graph(reasons_graph)
        n += 1

        if score1 != 100:
            line_count = 1
            for rule in details.keys():
                if details[rule]['message'] != '':
                    if "CDN" in details[rule]['message']:
                        details[rule]['message'] = details[rule]['message'].split('.')[0]
                    text += '<br>%s. <i>%s</i>' %(line_count, details[rule]['message'])
                    line_count += 1
                    #if len(details[rule]['message']) > 0:
                    #    text += '<ol>'
                    #    for component in details[rule]['components']:
                    #        decoded_component = urllib.parse.unquote(component)
                    #        text += '<li style="font-size:10px">%s</li>' %decoded_component
                    #    text += '</ol>'                            
            text += '<br>'

        alerts_summary[url_id].append(type_alert)
        file_emailtext.append(text)
        prior_changes.append(percdelta)

    if text != '':
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls 

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
if file_emailtext != []:
    file_emailtext = sort_email_from_list(prior_changes, file_emailtext)
    file_emailtext = "".join(file_emailtext)

    title = title_to_email_section('Yslow Score','change')
    file_emailtext = title + file_emailtext
else:
    file_emailtext = ''
    logging.info("No data sent to email")
