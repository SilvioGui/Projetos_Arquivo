#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

dict_audits = {'semantic':
                    {
                   'score':{'en':'Score',
                                 'pt':'Score',
                                 },
#accessibility audits
                   'accesskeys':{'en':'&#39;[accesskey]&#39; values are not unique',
                                 'pt':'valores de &#39;[accesskey]&#39; não são únicos',
                                 },
                   'aria-allowed-attr':{'en':'&#39;[aria-*]&#39; attributes do not match their roles',
                                        'pt':'Os atributos &#39;[aria-*]&#39; não correspondem ao seu \'role\'',
                                        },
                   'aria-required-attr':{'en':'&#39;[role]&#39;s do not have all required &#39;[aria-*]&#39; attributes',
                                         'pt':'Os &#39;[role]&#39;s não têm todos os atributos &#39;[aria-*]&#39; requeridos',
                                         },
                   'aria-required-children':{'en':'Elements with &#39;[role]&#39; that require specific children &#39;[role]&#39;s, are missing',
                                             'pt':'Elementos com &#39;[role]&#39; que requerem &#39;[role]&#39; filhos específicos estão faltando',
                                             },
                   'aria-required-parent':{'en':'&#39;[role]&#39;s are not contained by their required parent element',
                                           'pt':'&#39;[role]&#39;s não são contidos pelo elemento pai necessário',
                                          },
                   'aria-roles':{'en':'&#39;[role]&#39; values are not valid',
                                 'pt':'Valores de &#39;[role]&#39; não são válidos',
                                },
                   'aria-valid-attr-value':{'en':'&#39;[aria-*]&#39; attributes have valid values',
                                            'pt':'Os atributos &#39;[aria-*]&#39; tem valores válidos',
                                            },
                   'aria-valid-attr':{'en':'&#39;[aria-*]&#39; attributes are valid and not misspelled',
                                 'pt':'Os atributos &#39;[aria-*]&#39; são válidos e não contém erros de digitação',
                                 },
                   'audio-caption':{'en':'&#39;&lt;audio&gt;&#39; elements are missing a &#39;&lt;track&gt;&#39; element with &#39;[kind="captions"]&#39;',
                                 'pt':'Os elementos &#39;&lt;audio&gt;&#39; têm faltando um elemento &#39;&lt;track&gt;&#39; com &#39;[kind="captions"]&#39;',
                                 },
                   'button-name':{'en':'Buttons have an accessible name',
                                 'pt':'Os botões têm nomes acessíveis',
                                 },
                   'bypass':{'en':'The page contains a heading, skip link, or landmark region',
                             'pt':'A página contém cabeçalho, skip links, ou região com ARIA landmark',
                                  },
                   'color-contrast':{'en':'Background and foreground colors do not have a sufficient contrast ratio',
                                 'pt':'As cores de frente e fundo não tem contraste suficiente',
                                  },
                   'definition-list':{'en':'&#39;&lt;dl&gt;&#39;\'s do not contain only properly-ordered &#39;&lt;dt&gt;&#39; and &#39;&lt;dd&gt;&#39; groups, &#39;&lt;script&gt;&#39; or &#39;&lt;template&gt;&#39; elements',
                                 'pt':'As &#39;&lt;dl&gt;&#39; não contêm grupos de &#39;&lt;dt&gt;&#39; e &#39;&lt;dd&gt;&#39; ou elementos &#39;&lt;template&gt;&#39; e &#39;&lt;script&gt;&#39; ordenados apropriadamente',
                                 },
                   'dlitem':{'en':'Definition list items are not wrapped in &#39;&lt;dl&gt;&#39; elements',
                                 'pt':'Os itens de definition list não estão dentro de elementos &#39;&lt;dl&gt;&#39;',
                                 },
                   'document-title':{'en':'Document has a &#39;&lt;title&gt;&#39; element',
                                 'pt':'O documento tem um elemento &#39;&lt;title&gt;&#39;',
                                 },
                   'duplicate-id':{'en':'&#39;[id]&#39; attributes on the page are not unique',
                                   'pt':'Os atributos &#39;[id]&#39;da página não são únicos',
                                 },
                   'frame-title':{'en':'&#39;&lt;frame&gt;&#39; or &#39;&lt;iframe&gt;&#39; elements do not have a title',
                                 'pt':'Os elementos &#39;&lt;frame&gt;&#39; ou &#39;&lt;iframe&gt;&#39; não tem um título',
                                 },
                   'html-has-lang':{'en':'&#39;&lt;html&gt;&#39; element does not have a &#39;[lang]&#39; attribute',
                                 'pt':'O elemento &#39;&lt;html&gt;&#39; não tem um atributo &#39;[lang]&#39;',
                                 },
                   'html-lang-valid':{'en':'&#39;&lt;html&gt;&#39; element does not have a valid value for its &#39;[lang]&#39; attribute',
                                 'pt':'O elemento &#39;&lt;html&gt;&#39; não tem um valor válido para seu atributo &#39;[lang]&#39;',
                                 },
                   'image-alt':{'en':'Image elements do not have &#39;[alt]&#39; attributes',
                                 'pt':'Elementos de imagem não tem atributos &#39;[alt]&#39;',
                                 },
                   'input-image-alt':{'en':'&#39;&lt;input type="image"&gt;&#39; elements do not have &#39;[alt]&#39; text',
                                     'pt':'Os elementos &#39;&lt;input type="image"&gt;&#39; não tem texto &#39;[alt]&#39;',
                                     },
                   'label':{'en':'Form elements do not have associated labels',
                                 'pt':'Os elementos de formulário não têm labels associadas',
                                 },
                   'layout-table':{'en':'Presentational &#39;&lt;table&gt;&#39; elements do not avoid using &#39;&lt;th&gt;&#39;, &#39;&lt;caption&gt;&#39; or the &#39;[summary]&#39; attribute',
                                 'pt':'Elementos &#39;&lt;table&gt;&#39; não evitam o uso de &#39;&lt;th&gt;&#39;, &#39;&lt;caption&gt;&#39; ou o atributo &#39;[summary]&#39;',
                                 },
                   'link-name':{'en':'Links do not have a discernible name',
                                 'pt':'Os links não têm nomes discerníveis',
                                 },
                   'list':{'en':'Lists contain only &#39;&lt;li&gt;&#39; elements and script supporting elements (&#39;&lt;script&gt;&#39; and &#39;&lt;template&gt;&#39;)',
                                 'pt':'As listas contêm somente elementos &#39;&lt;li&gt;&#39; e elementos que suportam scripts(&#39;&lt;script&gt;&#39; e &#39;&lt;template&gt;&#39;)',
                                 },
                   'auditoria':{'en':'List items (&#39;&lt;li&gt;&#39;) are contained within &#39;&lt;ul&gt;&#39; or &#39;&lt;ol&gt;&#39; parent elements',
                                 'pt':'Os itens das listas (&#39;&lt;li&gt;&#39;) estão contidos dentro de &#39;&lt;ul&gt;&#39; ou elementos pais &#39;&lt;ol&gt;&#39;',
                                 },
                   'meta-refresh':{'en':'The document uses &#39;&lt;meta http-equiv="refresh"&gt;&#39;',
                                 'pt':'O documento usa &#39;&lt;meta http-equiv="refresh"&gt;&#39;',
                                 },
                   'meta-viewport':{'en':'&#39;[user-scalable="no"]&#39; is used in the &#39;&lt;meta name="viewport"&gt;&#39; element or the &#39;[maximum-scale]&#39; attribute is less than 5',
                                 'pt':'&#39;[user-scalable="no"]&#39; é usado no elemento &#39;&lt;meta name="viewport"&gt;&#39; ou o atributo &#39;[maximum-scale]&#39; é menor do que 5',
                                 },
                   'object-alt':{'en':'&#39;&lt;object&gt;&#39; elements do not have &#39;[alt]&#39; text',
                                 'pt':'Os elementos &#39;&lt;object&gt;&#39; não tem um texto &#39;[alt]&#39;',
                                 },
                   'tabindex':{'en':'No element has a &#39;[tabindex]&#39; value greater than 0',
                                 'pt':'Nenhum elemento tem um &#39;[tabindex]&#39; com valor maior do que 0',
                                 },
                   'td-headers-attr':{'en':'Cells in a &#39;&lt;table&gt;&#39; element that use the &#39;[headers]&#39; attribute refers to other cells of that same table',
                                 'pt':'As células em um elemento &#39;&lt;table&gt;&#39; que fazem uso de atributo &#39;[headers]&#39; se referem à outras células da mesma tabela',
                                 },
                   'th-has-data-cells':{'en':'&#39;&lt;th&gt;&#39; elements and elements with &#39;[role="columnheader"/"rowheader"]&#39; do not have data cells they describe',
                                 'pt':'Os elementos &#39;&lt;th&gt;&#39; e elementos com &#39;[role="columnheader"/"rowheader"]&#39; não têm as células que descrevem',
                                 },
                   'valid-lang':{'en':'&#39;[lang]&#39; attributes do not have a valid value',
                                 'pt':'Os atributos &#39;[lang]&#39; não têm um valor válido',
                                 },
                   'video-caption':{'en':'&#39;&lt;video&gt;&#39; elements do not contain a &#39;&lt;track&gt;&#39; element with &#39;[kind="captions"]&#39;',
                                 'pt':'Os elementos &#39;&lt;video&gt;&#39; não contêm um elemento &#39;&lt;track&gt;&#39; com &#39;[kind="captions"]&#39;',
                                 },
                   'video-description':{'en':'&#39;&lt;video&gt;&#39; elements do not contain a &#39;&lt;track&gt;&#39; element with &#39;[kind="description"]&#39;',
                                 'pt':'Os elementos de vídeo &#39;&lt;video&gt;&#39; não contêm um elemento &#39;&lt;track&gt;&#39; com &#39;[kind="description"]&#39;',
                                 },
                   'logical-tab-order':{'en':'The page has a logical tab order',
                                 'pt':'A página tem uma ordem lógica de tabulação',
                                 },
                   'focusable-controls':{'en':'Interactive controls are keyboard focusable',
                                 'pt':'Controles interativos podem ser focados pelo teclado',
                                 },
                   'managed-focus':{'en':'The user\'s focus is directed to new content added to the page',
                                 'pt':'O foco do usuário é direcionado para novo conteúdo adicionado à página',
                                 },
                   'focus-traps':{'en':'User focus is not accidentally trapped in a region',
                                 'pt':'O foco do usuário não fica preso em alguma região acidentalmente',
                                 },
                   'custom-controls-labels':{'en':'Custom controls have associated labels',
                                 'pt':'Os Custom controls tem labels associadas',
                                 },
                   'custom-controls-roles':{'en':'Custom controls have ARIA roles',
                                 'pt':'Os custom controls têm ARIA roles',
                                 },
                   'visual-order-follows-dom':{'en':'Visual order on the page follows DOM order',
                                 'pt':'A ordem visual da página segue a ordem do DOM',
                                 },
                   'offscreen-content-hidden':{'en':'Offscreen content is hidden from assistive technology',
                                 'pt':'Conteúdo Offscreen está escondido de tecnologia assistiva',
                                 },
                   'heading-levels':{'en':'Headings don\'t skip levels',
                                 'pt':'Os cabeçalhos não pulam níveis',
                                 },
                   'use-landmarks':{'en':'HTML5 landmark elements are used to improve navigation',
                                 'pt':'Os elemento de landmark do HTML5 são usados para melhorar a navegação',
                                 },
                   'listitem':{'en':'List Item',
                                 'pt':'List Item',
                                 },
                   'interactive-element-affordance':{'en':'Interactive Element Affordance',
                                 'pt':'Interactive Element Affordance',
                                 },
    #pwa audits
                   'service-worker':{'en':'Does not register a service worker',
                                 'pt':'Não registra um service worker',
                                 },
                   'works-offline':{'en':'Does not respond with a 200 when offline',
                                 'pt':'Não responde com status 200 quando está offline',
                                 },
                   'without-javascript':{'en':'Contains some content when JavaScript is not available',
                                 'pt':'Possui algum conteúdo quando o JavaScript não está habilitado',
                                 },
                   'is-on-https':{'en':'Uses HTTPS',
                                 'pt':'Usa HTTPS',
                                 },
                   'redirects-http':{'en':'Redirects HTTP traffic to HTTPS',
                                 'pt':'Redireciona tráfego HTTP para HTTPS',
                                 },
                   'load-fast-enough-for-pwa':{'en':'Page load is not fast enough on 3G',
                                 'pt':'O carregamento da página não é rápido o suficiente no 3G',
                                 },
                   'webapp-install-banner':{'en':'User will not be prompted to Install the Web App',
                                 'pt':'O usuário não será perguntado para instalar o App',
                                 },
                   'splash-screen':{'en':'Is not configured for a custom splash screen',
                                 'pt':'Is not configured for a custom splash screen',
                                 },
                   'themed-omnibox':{'en':'Address bar does not match brand colors',
                                 'pt':'A barra de endereços não condiz com as cores da marca',
                                 },
                   'viewport':{'en':'Has a &#39;&lt;meta name="viewport"&gt;&#39; tag with &#39;width&#39; or &#39;initial-scale&#39;',
                                 'pt':'Possui uma tag &#39;&lt;meta name="viewport"&gt;&#39; com &#39;width&#39; ou &#39;initial-scale&#39;',
                                 },
                   'content-width':{'en':'Content is sized correctly for the viewport',
                                 'pt':'O conteúdo é dimensionado corretamente para o viewport',
                                 },
                   'pwa-cross-browser':{'en':'Site works cross-browser',
                                 'pt':'Site funciona cross-browser',
                                 },
                   'pwa-page-transitions':{'en':'Page transitions don\'t feel like they block on the network',
                                 'pt':'As transições de páginas não parecem travar devido à rede',
                                 },
                   'pwa-each-page-has-url':{'en':'Each page has a URL',
                                 'pt':'Cada página tem uma URL',
                                 },
    #performance audits
                   'efficient-animated-content':{'en':'Efficient Animated Content',
                                 'pt':'Conteúdo Animado Eficiente',
                                 },
                   'final-screenshot':{'en':'Final Screenshot',
                                 'pt':'Final Screenshot',
                                 },
                   'metrics':{'en':'Metrics',
                                 'pt':'Métricas',
                                 },
                   'first-contentful-paint':{'en':'First Contentful paint',
                                 'pt':'First Contentful paint',
                                 },
                   'first-meaningful-paint':{'en':'First meaningful paint',
                                 'pt':'First meaningful paint',
                                 },
                   'first-cpu-idle':{'en':'First CPU Idle',
                                 'pt':'First CPU Idle',
                                 },
                   'interactive':{'en':'Interactive',
                                 'pt':'Interactive',
                                 },
                   'consistently-interactive':{'en':'Consistently Interactive',
                                 'pt':'Consistently Interactive',
                                 },
                   'speed-index':{'en':'Perceptual Speed Index',
                                 'pt':'Índice de Percepção de Velocidade',
                                 },
                   'estimated-input-latency':{'en':'Estimated Input Latency',
                                 'pt':'Latência estimada de entrada',
                                 },
                   'render-blocking-resources':{'en':'Render-Blocking Resources',
                                 'pt':'Site não usa recursos que retardam a primeira pintura',
                                 },
                   'link-blocking-first-paint':{'en':'Reduce render-blocking stylesheets',
                                 'pt':'Reduza as stylesheets que bloqueiam renderização',
                                 },
                   'script-blocking-first-paint':{'en':'Reduce render-blocking scripts',
                                 'pt':'Reduza as stylesheets que bloqueiam renderização',
                                 },
                   'uses-responsive-images':{'en':'Properly size images',
                                 'pt':'Dimensione imagens apropriadamente',
                                 },
                   'offscreen-images':{'en':'Offscreen images',
                                 'pt':'Imagens Offscreen',
                                 },
                   'unminified-css':{'en':'Minify CSS',
                                 'pt':'Minificar CSS',
                                 },
                   'unminified-javascript':{'en':'Minify JavaScript',
                                 'pt':'Minificar JavaScript',
                                 },
                   'unused-css-rules':{'en':'Unused CSS rules',
                                 'pt':'Regras CSS não usadas',
                                 },
                   'uses-optimized-images':{'en':'Optimize images',
                                 'pt':'Otimize imagens',
                                 },
                   'uses-rel-preconnect':{'en':'Preload key requests',
                                 'pt':'Faça Preload de elementos chave',
                                 },
                   'uses-webp-images':{'en':'Serve images in next-gen formats',
                                 'pt':'Servir imagens em formatos da próxima geração',
                                 },
                   'uses-text-compression':{'en':'Enable text compression',
                                 'pt':'Habilite a compressão de texto',
                                 },
                   'time-to-first-byte':{'en':'Keep server response times low (TTFB)',
                                 'pt':'Mantenha o tempo de resposta do servidor baixo (TTFB)',
                                 },
                   'redirects':{'en':'Avoids page redirects',
                                 'pt':'Evite redirecionamentos de páginas',
                                 },
                   'uses-rel-preload':{'en':'Preload key requests',
                                 'pt':'Use Preload em recursos essenciais',
                                 },
                   'total-byte-weight':{'en':'Avoids enormous network payloads',
                                 'pt':'Evite transmissão de enormes quantidades de dados',
                                 },
                   'uses-long-cache-ttl':{'en':'Uses inefficient cache policy on static assets',
                                 'pt':'Uso ineficiente de cache em recursos estáticos',
                                 },
                   'dom-size':{'en':'Avoids an excessive DOM size',
                                 'pt':'Evite um tamanho de DOM excessivo',
                                 },
                   'critical-request-chains':{'en':'Critical Request Chains',
                                 'pt':'Cadeia de Requesições Críticas',
                                 },
                   'network-requests':{'en':'Network Requests',
                                 'pt':'Requisições à Rede',
                                 },
                   'user-timings':{'en':'User Timing marks and measures',
                                 'pt':'Marcações e medições de User Timing',
                                 },
                   'bootup-time':{'en':'JavaScript boot-up time is too high',
                                 'pt':'O tempo de boot do JavaScript é muito alto',
                                 },
                   'screenshot-thumbnails':{'en':'Screenshot Thumbnails',
                                 'pt':'Screenshot Thumbnails',
                                 },
                   'mainthread-work-breakdown':{'en':'Main thread work breakdown',
                                 'pt':'Redução do trabalho da thread principal',
                                 },
                   'font-display':{'en':'Avoid invisible text while webfonts are loading',
                                 'pt':'Evite textos invisíveis enquanto as fontes web estão carregando',
                                 },
    #best practices audits
                   'doctype':{'en':'Doctype',
                                 'pt':'Doctype',
                                 },
                   'js-libraries':{'en':'JS libraries',
                                 'pt':'JS libraries',
                                 },
                   'appcache-manifest':{'en':'Avoids Application Cache',
                                 'pt':'Evite Cache de Aplicação',
                                 },
                   'no-websql':{'en':'Avoids WebSQL DB',
                                 'pt':'Evite WebSQL DB',
                                 },
                   'uses-http2':{'en':'Does not use HTTP/2 for all of its resources',
                                 'pt':'Não usa HTTP/2 para todos os seus recursos',
                                 },
                   'uses-passive-event-listeners':{'en':'Uses passive listeners to improve scrolling performance',
                                 'pt':'Uso de passive listeners para melhorar a performance de scroll',
                                 },
                   'no-mutation-events':{'en':'Uses Mutation Events in its own scripts',
                                 'pt':'Usa Mutation Events em seus scripts',
                                 },
                   'no-document-write':{'en':'Avoids &#39;document.write()&#39;',
                                 'pt':'Evite &#39;document.write()&#39;',
                                 },
                   'external-anchors-use-rel-noopener':{'en':'Does not open external anchors using &#39;rel="noopener"&#39;',
                                 'pt':'Não abre novas abas usando &#39;rel="noopener"&#39;',
                                 },
                   'geolocation-on-start':{'en':'Avoids requesting the geolocation permission on page load',
                                 'pt':'Evite perguntar por permissão de geolocalização no carregamento da página',
                                 },
                   'no-vulnerable-libraries':{'en':'Avoids front-end JavaScript libraries with known security vulnerabilities',
                                 'pt':'Evite bibliotecas de front-end JavaScript com vulnerabilidades de segurança conhecidas',
                                 },
                   'notification-on-start':{'en':'Avoids requesting the notification permission on page load',
                                 'pt':'Evite perguntar por permissão de notificações no carregamento da página',
                                 },
                   'deprecations':{'en':'Avoids deprecated APIs',
                                 'pt':'Evite APIs depreciadas',
                                 },
                   'manifest-short-name-length':{'en':'Manifest\'s &#39;short_name&#39; will be truncated when displayed on homescreen',
                                 'pt':'O &#39;short_name&#39; será truncado quando mostrado na tela inicial',
                                 },
                   'password-inputs-can-be-pasted-into':{'en':'Allows users to paste into password fields',
                                 'pt':'Allows users to paste into password fields',
                                 },
                   'errors-in-console':{'en':'Browser errors were logged to the console',
                                 'pt':'Os erros do Browser são impressos no console',
                                 },
                   'image-aspect-ratio':{'en':'Displays images with incorrect aspect ratio',
                                 'pt':'Exibe imagens com proporção incorreta',
                                 },
    #seo audits
                   'viewport':{'en':'Has a &#39;&lt;meta name="viewport"&gt;&#39; tag with &#39;width&#39; or &#39;initial-scale&#39;',
                                 'pt':'Possui uma tag &#39;&lt;meta name="viewport"&gt;&#39; com &#39;width&#39; ou &#39;initial-scale&#39;',
                                 },
                   'meta-description':{'en':'Document has a meta description',
                                 'pt':'O documento tem uma meta description',
                                 },
                   'http-status-code':{'en':'Page has successful HTTP status code',
                                 'pt':'A página têm um código HTTP de sucesso',
                                 },
                   'link-text':{'en':'Links have descriptive text',
                                 'pt':'Os links têm texto descritivo',
                                 },
                   'is-crawlable':{'en':'Page isn’t blocked from indexing',
                                 'pt':'A página não está bloqueada de indexação',
                                 },
                   'hreflang':{'en':'Document has a valid &#39;hreflang&#39;',
                                 'pt':'O documento tem um &#39;hreflang&#39; válido',
                                 },
                   'canonical':{'en':'Document has a valid &#39;rel=canonical&#39;',
                                 'pt':'O document tem um &#39;rel=canonical&#39; válido',
                                 },
                   'font-size':{'en':'Document uses legible font sizes',
                                 'pt':'O documento usa fontes de tamanhos legíveis',
                                 },
                   'plugins':{'en':'Document avoids plugins',
                                 'pt':'O documento evita plugins',
                                 },
                   'robots-txt':{'en':'Robots.txt',
                                 'pt':'Robots.txt',
                                 },
                   'mobile-friendly':{'en':'Page is mobile friendly',
                                 'pt':'A página é mobile friendly',
                                 },
                   'structured-data':{'en':'Structured data is valid',
                                 'pt':'Os dados estruturados são válidos',
                                 },
            }
}

dict_texts = {'text1':{
                        'en':'<br>There is still not enough information to follow %s on <a href="%s">%s</a>',
                        'pt':'<br>Ainda não há dados suficientes de %s para acompanhar em <a href="%s">%s</a>',
                        }
                }

def plot_n_curves(x, y, x_label_dates, n, names):
    font0 = FontProperties()
    font0.set_family('arial')
    font0.set_size(10)
    font0.set_style('italic')        
    font0.set_weight('bold')        
    
    font1 = FontProperties()
    font1.set_family('arial')
    font1.set_size(10)
    font1.set_weight('bold')        

    plt.figure(figsize=(10, 2.5))
    plt.rcParams['axes.facecolor'] = 'w'

    plt.xticks(range(len(x_label_dates)), x_label_dates, rotation = 25, color = 'black')    #enables ploting float vs string
    #graph information
    plt.title(graph_title, color = 'black' , fontproperties = font1)
    
    x_sm = numpy.array(x)
    for y_set, curve_name in zip(y, names):
        curve_name = html.unescape(curve_name)
        f = interp1d(x_sm, y_set, kind='linear')
        y_smooth=f(x_sm)
        plt.plot(x_sm, y_smooth, label = curve_name)

    max_len = 0
    for name in names:
        if len(name) > max_len:
            max_len = len(name)

    if max_len < 10:
        numero_cols = '5'
    elif max_len < 20:
        numero_cols = '4'
    elif max_len < 30:
        numero_cols = '3'
    elif max_len < 40:
        numero_cols = '2'
    else:
        numero_cols = '1'
    if len(str(start_date)) > 15:
        legend_padding = -0.55
    else:
        legend_padding = -0.4
    legend_padding = legend_padding - (math.ceil(len(names)/int(numero_cols)))*0.1
    
    #formats the axis to display big numbers with coma separating every 3 values. This also excludes scientific notation use 
    ax = plt.subplot()
    #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(loc=3, bbox_to_anchor=(0, legend_padding), ncol = int(numero_cols))
    
    if format_type == float:
        ax.set_yticklabels(['{:0,.2f}'.format(float(x)) for x in ax.get_yticks().tolist()])
    elif format_type == int:
        ax.set_yticklabels(['{:0,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

def smooth_list(entry_list, alpha):
    start_value = numpy.mean(entry_list[0:5])
    entry_list[0] = start_value
    m = 1
    while m < len(entry_list):
        if entry_list[m] != None:
            entry_list[m] = entry_list[m-1]*alpha + entry_list[m]*(1-alpha)
        else:
            entry_list[m] = entry_list[m-1]
        m += 1
    return entry_list

def moving_average(entry_list, n) :
    ret = numpy.cumsum(entry_list, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    new_list = list(ret[n - 1:] / n)
    while len(new_list) != len(entry_list):
        new_list.insert(0,None) 
    return new_list

# -------------------------- PAGESPEED SCORE REPORTS --------------------------------
table_name, script_type = 'lighthouse', 'reports'
reports = email_to_send['lighthouse']
if reports == None:
    raise RuntimeError('Report not enabled')
file_emailtext = ''
time_step = 1/24 

report_dict = yaml.load(reports)
format_type = float

for report in report_dict.keys():
    if 'audit' not in report_dict[report]:
        continue
    graph_title = report
    report_interval = int(report_dict[report]['period'])
    url_ids = report_dict[report]['urls']
    metrics = report_dict[report]['metrics']
    dimension = report_dict[report]['audit']
    statistics = report_dict[report]['stats']

    url_ids = list(set(url_ids) & set(allowed_url_ids))

    end_date = datetime.now(pytz.timezone(timezone)).strftime('%Y-%m-%d %H:00:00')
    end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    start_date = end_date - timedelta(days=report_interval)
    date1 = start_date
    dates = []
    x_label_dates = []

    while date1 < end_date:
        date1 = date1 + timedelta(days=time_step)
        dates.append(str(date1))

    x_axis_step = int(round(len(dates)/7,0))

    j = len(dates) - 1
    for date in dates[::-1]:
        if j >= 0:
            if date !=  dates[j]:
                x_label_dates.append('')
            else:
                x_label_dates.append(date)
                j -= x_axis_step
        else:
            x_label_dates.append('')
    x_label_dates = x_label_dates[::-1]
            
    #any number of metrics for 1 website
    if len(url_ids) == 1:
        siteurls = []
        i = 0
        report_values = []
        while i < len(metrics):
            report_values.append([])
            i += 1

        url_id = url_ids[0]
        for metric in metrics:
            if url_id not in reports_summary:
                reports_summary[url_id] = []
                    
            cursor.execute('select * from lighthouse where (url_id, audit_type, audit) = (%s, %s, %s) and datetime > %s order by datetime asc;' , (url_id, dimension, metric, start_date))
            results = cursor.fetchall()
            siteurl = results[0]['url']

            if len(results) < 5:
                file_emailtext += dict_texts['text1'][language] %(dict_audits['semantic'][language][metric], siteurl, siteurl)
                logging.info('There is still not enough information to follow %s on %s' %(dict_audits['semantic'][language][metric], siteurl))
                report_values = report_values[:-1]
                continue

            available_dates = []
            for result in results:
                available_dates.append(str(result['datetime']))
            not_available_dates = [x for x in dates if x not in available_dates]

            date_i = 0
            for date in dates:
                if date in not_available_dates:
                    report_values[metrics.index(metric)].append(None)
                else:
                    result_metric = float(results[date_i]['value'])
                    report_values[metrics.index(metric)].append(result_metric)
                    date_i += 1

            if 'smooth' in statistics and 'avg' in statistics:
                logging.info("It's not possible to apply exponencial smoothing and moving average simultaneously")
            elif 'smooth' in statistics and 'avg' not in statistics:
                if float(statistics['smooth']) >=0 and float(statistics['smooth']) <= 1:
                    correct_values = report_values[metrics.index(metric)]
                    smooth_curve = smooth_list(correct_values, float(statistics['smooth']))
                    report_values[metric.index(metric)] = smooth_curve
            elif 'avg' in statistics and 'smooth' not in statistics:
                correct_values = report_values[metrics.index(metric)]
                avg_curve = moving_average(correct_values, int(statistics['avg']))
                report_values[metrics.index(metric)] = avg_curve
                    
            dict_urls[url_id] = str(date1)
            analyzed_urls[execute_file[2]] = dict_urls
            reports_summary[url_id].append(metric)

            index = metrics.index(metric)
            metric = dict_audits['semantic'][metric][language]
            metrics[index] = metric

        siteurls = [siteurl]
        if report_values != []:
            plot_n_curves(list(range(0,len(dates))), report_values, x_label_dates, n, metrics)
            file_emailtext += '<img src="cid:Graph%s.png"><br>' %n
            n += 1

    #any numbers of websites comparing 1 same metric
    elif len(metrics) == 1:
        siteurls = []
        i = 0
        report_values = []
        while i < len(url_ids):
            report_values.append([])
            i += 1

        metric = metrics[0]
        for url_id in url_ids:
            if url_id not in reports_summary:
                reports_summary[url_id] = []
                                
            cursor.execute('select * from lighthouse where (url_id, audit_type, audit) = (%s, %s, %s) and datetime > %s order by datetime asc;' , (url_id, dimension, metric, start_date))
            results = cursor.fetchall()
            siteurl = results[0]['url']
            siteurls.append(siteurl)

            if len(results) < 5:
                file_emailtext += dict_texts['text1'][language] %(dict_audits['semantic'][language][metric], siteurl, siteurl)
                logging.info('There is still not enough information to follow %s on %s' %(dict_audits['semantic'][language][metric], siteurl))
                report_values = report_values[:-1]
                siteurls = siteurls[:-1]
                continue

            available_dates = []
            for result in results:
                available_dates.append(str(result['datetime']))
            not_available_dates = [x for x in dates if x not in available_dates]

            date_i = 0
            for date in dates:
                if date in not_available_dates:
                    report_values[url_ids.index(url_id)].append(None)
                else:
                    result_metric = float(results[date_i]['value'])
                    report_values[url_ids.index(url_id)].append(result_metric)
                    date_i += 1

            if 'smooth' in statistics and 'avg' in statistics:
                logging.info("It's not possible to apply exponencial smoothing and moving average simultaneously")
            elif 'smooth' in statistics and 'avg' not in statistics:
                if float(statistics['smooth']) >=0 and float(statistics['smooth']) <= 1:
                    correct_values = report_values[url_ids.index(url_id)]
                    smooth_curve = smooth_list(correct_values, float(statistics['smooth']))
                    report_values[url_ids.index(url_id)] = smooth_curve
            elif 'avg' in statistics and 'smooth' not in statistics:
                correct_values = report_values[url_ids.index(url_id)]
                avg_curve = moving_average(correct_values, int(statistics['avg']))
                report_values[url_ids.index(url_id)] = avg_curve

            dict_urls[url_id] = str(date1)
            analyzed_urls[execute_file[2]] = dict_urls
            reports_summary[url_id].append(metric)

        if report_values != []:
            plot_n_curves(list(range(0,len(dates))), report_values, x_label_dates, n, siteurls)
            file_emailtext += '<img src="cid:Graph%s.png"><br>' %n
            n += 1


#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
if file_emailtext != '':
    title = title_to_email_section('Lighthouse','report')
    file_emailtext = title + file_emailtext
else:
    file_emailtext = ''
    logging.info("No data sent to %s on email group %s" %(toaddr, email_group_id))
