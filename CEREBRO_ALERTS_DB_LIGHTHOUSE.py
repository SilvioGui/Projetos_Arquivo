#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

# -------------------------- LIGHTHOUSE AUDITS --------------------------------
table_name, script_type = 'lighthouse', 'alerts'
url_ids = get_url_ids('lighthouse','Lighthouse',dict)
url_ids = list(set(url_ids) & set(allowed_url_ids))

dict_audits = {'semantic':{'first-input-delay': {
                'link': 'https://web.dev/fid/', 'pt': 'First Input Delay', 'en': 'First Input Delay'},
                           'cumulative-layout-shift': {
                'link': 'https://web.dev/cls/', 'pt': 'Cumulative Layout Shift', 'en': 'Cumulative Layout Shift'},
                           'largest-contentful-paint': {
                'link': 'https://web.dev/lcp/', 'pt': 'Largest Contentful Paint', 'en': 'Largest Contentful Paint'},
                           'first-contentful-paint': {
                'link': 'https://web.dev/first-contentful-paint', 'pt': 'First Contentful paint', 'en': 'First Contentful paint'},
                            'first-meaningful-paint': {
                'link': 'https://web.dev/first-meaningful-paint', 'pt': 'First meaningful paint', 'en': 'First meaningful paint'},
                            'speed-index': {
                'link': 'https://web.dev/speed-index', 'pt': 'Índice de Percepção de Velocidade', 'en': 'Perceptual Speed Index'},
                            'interactive': {
                'link': 'https://web.dev/interactive', 'pt': 'Interactive', 'en': 'Interactive'},
                            'first-cpu-idle':{
                'link': 'https://web.dev/first-cpu-idle', 'pt': 'First CPU Idle', 'en': 'First CPU Idle'},
                            'max-potential-fid':{
                'link': 'https://developers.google.com/web/updates/2018/05/first-input-delay', 'pt':'Delay do Primeiro Input','en':'First Input Delay'},
                            'estimated-input-latency': {
                'link': 'https://web.dev/estimated-input-latency', 'pt': 'Latência estimada de entrada', 'en': 'Estimated Input Latency'},
                            'total-blocking-time': {
                'link': 'Not Available', 'pt': 'Tempo Total de Bloqueio', 'en': 'Total Blocking Time'},
                            'render-blocking-resources': {
                'link': 'https://web.dev/render-blocking-resources', 'pt': 'Site não usa recursos que retardam a primeira pintura', 'en': 'Render-Blocking Resources'},
                            'uses-responsive-images': {
                'link': 'https://web.dev/uses-responsive-images', 'pt': 'Dimensione imagens apropriadamente', 'en': 'Properly size images'},
                            'offscreen-images': {
                'link': 'https://web.dev/offscreen-images', 'pt': 'Imagens Offscreen', 'en': 'Offscreen images'},
                            'unminified-css': {
                'link': 'https://web.dev/unminified-css', 'pt': 'Minificar CSS', 'en': 'Minify CSS'},
                            'unminified-javascript': {
                'link': 'https://web.dev/unminified-javascript', 'pt': 'Minificar JavaScript', 'en': 'Minify JavaScript'},
                            'unused-css-rules': {
                'link': 'https://web.dev/unused-css-rules', 'pt': 'Regras CSS não usadas', 'en': 'Unused CSS rules'},
                            'uses-optimized-images': {
                'link': 'https://web.dev/uses-optimized-images', 'pt': 'Otimize imagens', 'en': 'Optimize images'},
                            'uses-webp-images': {
                'link': 'https://web.dev/uses-webp-images', 'pt': 'Servir imagens em formatos da próxima geração', 'en': 'Serve images in next-gen formats'},
                            'uses-text-compression': {
                'link': 'https://web.dev/uses-text-compression', 'pt': 'Habilite a compressão de texto', 'en': 'Enable text compression'},
                            'uses-rel-preconnect': {
                'link': 'https://web.dev/uses-rel-preconnect', 'pt': 'Faça Preload de elementos chave', 'en': 'Preload key requests'},
                            'time-to-first-byte': {
                'link': 'https://web.dev/time-to-first-byte', 'pt': 'Mantenha o tempo de resposta do servidor baixo (TTFB)', 'en': 'Keep server response times low (TTFB)'},
                            'redirects': {
                'link': 'https://web.dev/redirects', 'pt': 'Evite redirecionamentos de páginas', 'en': 'Avoids page redirects'},
                            'uses-rel-preload': {
                'link': 'https://web.dev/uses-rel-preload', 'pt': 'Use Preload em recursos essenciais', 'en': 'Preload key requests'},
                            'efficient-animated-content': {
                'link': 'https://web.dev/efficient-animated-content', 'pt': 'Conteúdo Animado Eficiente', 'en': 'Efficient Animated Content'},
                            'total-byte-weight': {
                'link': 'https://web.dev/total-byte-weight', 'pt': 'Evite transmissão de enormes quantidades de dados', 'en': 'Avoids enormous network payloads'},
                            'uses-long-cache-ttl': {
                'link': 'https://web.dev/uses-long-cache-ttl', 'pt': 'Uso ineficiente de cache em recursos estáticos', 'en': 'Uses inefficient cache policy on static assets'},
                            'dom-size': {
                'link': 'https://web.dev/dom-size', 'pt': 'Evite um tamanho de DOM excessivo', 'en': 'Avoids an excessive DOM size'},
                            'critical-request-chains': {
                'link': 'https://web.dev/critical-request-chains', 'pt': 'Cadeia de Requesições Críticas', 'en': 'Critical Request Chains'},
                            'user-timings': {
                'link': 'https://web.dev/user-timings', 'pt': 'Marcações e medições de User Timing', 'en': 'User Timing marks and measures'},
                            'bootup-time': {
                'link': 'https://web.dev/bootup-time', 'pt': 'O tempo de boot do JavaScript é muito alto', 'en': 'JavaScript boot-up time is too high'},
                            'mainthread-work-breakdown': {
                'link': 'https://web.dev/mainthread-work-breakdown', 'pt': 'Redução do trabalho da thread principal', 'en': 'Main thread work breakdown'},
                            'font-display': {
                'link': 'https://web.dev/font-display', 'pt': 'Evite textos invisíveis enquanto as fontes web estão carregando', 'en': 'Avoid invisible text while webfonts are loading'},
                            'performance-budget': {
                'link': 'https://developers.google.com/web/tools/lighthouse/audits/budgets','pt':'Perfomance Budget','en':'Perfomance Budget'},
                            'resource-summary': {
                'link': 'https://developers.google.com/web/tools/lighthouse/audits/budgets','pt':'Sumário de Recursos','en':'Resources Summary'},
                            'third-party-summary': {
                'link': 'https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/loading-third-party-javascript/','pt':'Recursos de Terceiros','en':'Third Party Resources'},
                            'network-requests': {
                'link': 'Not Available', 'pt': 'Requisições à Rede', 'en': 'Network Requests'},
                            'network-rtt': {
                'link': 'https://hpbn.co/primer-on-latency-and-bandwidth/', 'pt': 'Network Round Trip Times', 'en': 'Network Round Trip Times'},
                            'network-server-latency': {
                'link': 'https://hpbn.co/primer-on-web-performance/#analyzing-the-resource-waterfall','pt':'Latências de Backend de Server','en':'Server Backend Latencies'},
                            'main-thread-tasks': {
                'link': 'Not Available','pt':'Tarefas','en':'Tasks'},
                            'diagnostics': {
                'link': 'https://github.com/GoogleChrome/lighthouse/blob/d2ec9ffbb21de9ad1a0f86ed24575eda32c796f0/docs/scoring.md#how-are-the-scores-weighted','pt':'Diagnóstico','en':'Diagnostics'},
                            'metrics': {
                'link': 'Not Available', 'pt': 'Métricas', 'en': 'Metrics'},
                            'screenshot-thumbnails': {
                'link': 'Not Available', 'pt': 'Screenshot Thumbnails', 'en': 'Screenshot Thumbnails'},
                            'final-screenshot': {
                'link': 'Not Available', 'pt': 'Screenshot Final', 'en': 'Final Screenshot'},
                            'accesskeys': {
                'link': 'https://web.dev/accesskeys/', 'pt': 'valores de &#39;[accesskey]&#39; não são únicos', 'en': '&#39;[accesskey]&#39; values are not unique'},
                            'aria-allowed-attr': {
                'link': 'https://web.dev/aria-allowed-attr/', 'pt': "Os atributos &#39;[aria-*]&#39; não correspondem ao seu 'role'", 'en': '&#39;[aria-*]&#39; attributes do not match their roles'},
                            'aria-required-attr': {
                'link': 'https://web.dev/aria-required-attr/', 'pt': 'Os &#39;[role]&#39;s não têm todos os atributos &#39;[aria-*]&#39; requeridos', 'en': '&#39;[role]&#39;s do not have all required &#39;[aria-*]&#39; attributes'},
                            'aria-required-children': {
                'link': 'https://web.dev/aria-required-children/', 'pt': 'Elementos com &#39;[role]&#39; que requerem &#39;[role]&#39; filhos específicos estão faltando', 'en': 'Elements with &#39;[role]&#39; that require specific children &#39;[role]&#39;s, are missing'},
                            'aria-required-parent': {
                'link': 'https://web.dev/aria-required-parent/', 'pt': '&#39;[role]&#39;s não são contidos pelo elemento pai necessário', 'en': '&#39;[role]&#39;s are not contained by their required parent element'},
                            'aria-roles': {
                'link': 'https://web.dev/aria-roles/', 'pt': 'Valores de &#39;[role]&#39; não são válidos', 'en': '&#39;[role]&#39; values are not valid'},
                            'aria-valid-attr-value': {
                'link': 'https://web.dev/aria-valid-attr-value/', 'pt': 'Os atributos &#39;[aria-*]&#39; tem valores válidos', 'en': '&#39;[aria-*]&#39; attributes have valid values'},
                            'aria-valid-attr': {
                'link': 'https://web.dev/aria-valid-attr/', 'pt': 'Os atributos &#39;[aria-*]&#39; são válidos e não contém erros de digitação', 'en': '&#39;[aria-*]&#39; attributes are valid and not misspelled'},
                            'audio-caption': {
                'link': 'https://web.dev/audio-caption/', 'pt': 'Os elementos &#39;&lt;audio&gt;&#39; têm faltando um elemento &#39;&lt;track&gt;&#39; com &#39;[kind="captions"]&#39;', 'en': '&#39;&lt;audio&gt;&#39; elements are missing a &#39;&lt;track&gt;&#39; element with &#39;[kind="captions"]&#39;'},
                            'button-name': {
                'link': 'https://web.dev/button-name/', 'pt': 'Os botões têm nomes acessíveis', 'en': 'Buttons have an accessible name'},
                            'bypass': {
                'link': 'https://web.dev/bypass/', 'pt': 'A página contém cabeçalho, skip links, ou região com ARIA landmark', 'en': 'The page contains a heading, skip link, or landmark region'},
                            'color-contrast': {
                'link': 'https://web.dev/color-contrast/', 'pt': 'As cores de frente e fundo não tem contraste suficiente', 'en': 'Background and foreground colors do not have a sufficient contrast ratio'},
                            'definition-list': {
                'link': 'https://web.dev/definition-list/', 'pt': 'As &#39;&lt;dl&gt;&#39; não contêm grupos de &#39;&lt;dt&gt;&#39; e &#39;&lt;dd&gt;&#39; ou elementos &#39;&lt;template&gt;&#39; e &#39;&lt;script&gt;&#39; ordenados apropriadamente', 'en': "&#39;&lt;dl&gt;&#39;'s do not contain only properly-ordered &#39;&lt;dt&gt;&#39; and &#39;&lt;dd&gt;&#39; groups, &#39;&lt;script&gt;&#39; or &#39;&lt;template&gt;&#39; elements"},
                            'dlitem': {
                'link': 'https://web.dev/dlitem/', 'pt': 'Os itens de definition list não estão dentro de elementos &#39;&lt;dl&gt;&#39;', 'en': 'Definition list items are not wrapped in &#39;&lt;dl&gt;&#39; elements'},
                            'document-title':{
                'link': 'https://web.dev/document-title/', 'pt': 'O documento tem um elemento &#39;&lt;title&gt;&#39;', 'en': 'Document has a &#39;&lt;title&gt;&#39; element'},
                           'duplicate-id': {
                'link': 'https://web.dev/duplicate-id/', 'pt': 'Os atributos &#39;[id]&#39;da página não são únicos', 'en': '&#39;[id]&#39; attributes on the page are not unique'},
                            'frame-title': {'link': 'https://web.dev/frame-title/', 'pt': 'Os elementos &#39;&lt;frame&gt;&#39; ou &#39;&lt;iframe&gt;&#39; não tem um título', 'en': '&#39;&lt;frame&gt;&#39; or &#39;&lt;iframe&gt;&#39; elements do not have a title'},
                           'html-has-lang': {
                'link': 'https://web.dev/html-has-lang/', 'pt': 'O elemento &#39;&lt;html&gt;&#39; não tem um atributo &#39;[lang]&#39;', 'en': '&#39;&lt;html&gt;&#39; element does not have a &#39;[lang]&#39; attribute'},
                           'html-lang-valid': {
                'link': 'https://web.dev/html-lang-valid/', 'pt': 'O elemento &#39;&lt;html&gt;&#39; não tem um valor válido para seu atributo &#39;[lang]&#39;', 'en': '&#39;&lt;html&gt;&#39; element does not have a valid value for its &#39;[lang]&#39; attribute'},
                           'image-alt': {
                'link': 'https://web.dev/image-alt/', 'pt': 'Elementos de imagem não tem atributos &#39;[alt]&#39;', 'en': 'Image elements do not have &#39;[alt]&#39; attributes'}, 'input-image-alt': {'link': 'https://web.dev/input-image-alt/', 'pt': 'Os elementos &#39;&lt;input type="image"&gt;&#39; não tem texto &#39;[alt]&#39;', 'en': '&#39;&lt;input type="image"&gt;&#39; elements do not have &#39;[alt]&#39; text'}, 'label': {'link': 'https://web.dev/label/', 'pt': 'Os elementos de formulário não têm labels associadas', 'en': 'Form elements do not have associated labels'},
                           'layout-table': {
                'link': 'https://web.dev/layout-table/', 'pt': 'Elementos &#39;&lt;table&gt;&#39; não evitam o uso de &#39;&lt;th&gt;&#39;, &#39;&lt;caption&gt;&#39; ou o atributo &#39;[summary]&#39;', 'en': 'Presentational &#39;&lt;table&gt;&#39; elements do not avoid using &#39;&lt;th&gt;&#39;, &#39;&lt;caption&gt;&#39; or the &#39;[summary]&#39; attribute'},
                           'link-name': {
                'link': 'https://web.dev/link-name/', 'pt': 'Os links não têm nomes discerníveis', 'en': 'Links do not have a discernible name'},
                           'list': {
                'link': 'https://web.dev/list/', 'pt': 'As listas contêm somente elementos &#39;&lt;li&gt;&#39; e elementos que suportam scripts(&#39;&lt;script&gt;&#39; e &#39;&lt;template&gt;&#39;)', 'en': 'Lists contain only &#39;&lt;li&gt;&#39; elements and script supporting elements (&#39;&lt;script&gt;&#39; and &#39;&lt;template&gt;&#39;)'},
                           'listitem': {
                'link': 'https://web.dev/listitem/', 'pt': 'List Item', 'en': 'List Item'},
                           'meta-refresh': {
                'link': 'https://web.dev/meta-refresh/', 'pt': 'O documento usa &#39;&lt;meta http-equiv="refresh"&gt;&#39;', 'en': 'The document uses &#39;&lt;meta http-equiv="refresh"&gt;&#39;'}, 'meta-viewport': {'link': 'https://web.dev/meta-viewport/', 'pt': '&#39;[user-scalable="no"]&#39; é usado no elemento &#39;&lt;meta name="viewport"&gt;&#39; ou o atributo &#39;[maximum-scale]&#39; é menor do que 5', 'en': '&#39;[user-scalable="no"]&#39; is used in the &#39;&lt;meta name="viewport"&gt;&#39; element or the &#39;[maximum-scale]&#39; attribute is less than 5'},
                           'object-alt': {
                'link': 'https://web.dev/object-alt/', 'pt': 'Os elementos &#39;&lt;object&gt;&#39; não tem um texto &#39;[alt]&#39;', 'en': '&#39;&lt;object&gt;&#39; elements do not have &#39;[alt]&#39; text'},
                           'tabindex': {
                'link': 'https://web.dev/tabindex/', 'pt': 'Nenhum elemento tem um &#39;[tabindex]&#39; com valor maior do que 0', 'en': 'No element has a &#39;[tabindex]&#39; value greater than 0'},
                           'td-headers-attr': {
                'link': 'https://web.dev/td-headers-attr/', 'pt': 'As células em um elemento &#39;&lt;table&gt;&#39; que fazem uso de atributo &#39;[headers]&#39; se referem à outras células da mesma tabela', 'en': 'Cells in a &#39;&lt;table&gt;&#39; element that use the &#39;[headers]&#39; attribute refers to other cells of that same table'},
                           'th-has-data-cells': {
                'link': 'https://web.dev/th-has-data-cells/', 'pt': 'Os elementos &#39;&lt;th&gt;&#39; e elementos com &#39;[role="columnheader"/"rowheader"]&#39; não têm as células que descrevem', 'en': '&#39;&lt;th&gt;&#39; elements and elements with &#39;[role="columnheader"/"rowheader"]&#39; do not have data cells they describe'},
                           'valid-lang': {
                'link': 'https://web.dev/valid-lang/', 'pt': 'Os atributos &#39;[lang]&#39; não têm um valor válido', 'en': '&#39;[lang]&#39; attributes do not have a valid value'}, 'video-caption': {'link': 'https://web.dev/video-caption/', 'pt': 'Os elementos &#39;&lt;video&gt;&#39; não contêm um elemento &#39;&lt;track&gt;&#39; com &#39;[kind="captions"]&#39;', 'en': '&#39;&lt;video&gt;&#39; elements do not contain a &#39;&lt;track&gt;&#39; element with &#39;[kind="captions"]&#39;'},
                           'video-description': {
                'link': 'https://web.dev/video-description/', 'pt': 'Os elementos de vídeo &#39;&lt;video&gt;&#39; não contêm um elemento &#39;&lt;track&gt;&#39; com &#39;[kind="description"]&#39;', 'en': '&#39;&lt;video&gt;&#39; elements do not contain a &#39;&lt;track&gt;&#39; element with &#39;[kind="description"]&#39;'},
                           'logical-tab-order': {
                'link': 'https://web.dev/logical-tab-order/', 'pt': 'A página tem uma ordem lógica de tabulação', 'en': 'The page has a logical tab order'},
                           'focusable-controls': {
                'link': 'https://web.dev/focusable-controls/', 'pt': 'Controles interativos podem ser focados pelo teclado', 'en': 'Interactive controls are keyboard focusable'},
                           'interactive-element-affordance': {
                'link': 'https://web.dev/interactive-element-affordance/', 'pt': 'Interactive Element Affordance', 'en': 'Interactive Element Affordance'},
                           'managed-focus': {
                'link': 'https://web.dev/managed-focus/', 'pt': 'O foco do usuário é direcionado para novo conteúdo adicionado à página', 'en': "The user's focus is directed to new content added to the page"},
                           'focus-traps': {
                'link': 'https://web.dev/focus-traps/', 'pt': 'O foco do usuário não fica preso em alguma região acidentalmente', 'en': 'User focus is not accidentally trapped in a region'},
                           'custom-controls-labels': {
                'link': 'https://web.dev/custom-controls-labels/', 'pt': 'Os Custom controls tem labels associadas', 'en': 'Custom controls have associated labels'},
                           'custom-controls-roles': {
                'link': 'https://web.dev/custom-control-roles/', 'pt': 'Os custom controls têm ARIA roles', 'en': 'Custom controls have ARIA roles'},
                           'visual-order-follows-dom': {
                'link': 'https://web.dev/visual-order-follows-dom/', 'pt': 'A ordem visual da página segue a ordem do DOM', 'en': 'Visual order on the page follows DOM order'},
                           'offscreen-content-hidden': {
                'link': 'https://web.dev/offscreen-content-hidden/', 'pt': 'Conteúdo Offscreen está escondido de tecnologia assistiva', 'en': 'Offscreen content is hidden from assistive technology'},
                           'heading-levels': {
                'link': 'https://web.dev/heading-levels/', 'pt': 'Os cabeçalhos não pulam níveis', 'en': "Headings don't skip levels"},
                           'use-landmarks': {
                'link': 'https://web.dev/use-landmarks/', 'pt': 'Os elemento de landmark do HTML5 são usados para melhorar a navegação', 'en': 'HTML5 landmark elements are used to improve navigation'},
                           'appcache-manifest': {
                'link': 'https://web.dev/appcache-manifest', 'pt': 'Evite Cache de Aplicação', 'en': 'Avoids Application Cache'},
                           'is-on-https': {
                'link': 'https://web.dev/is-on-https', 'pt': 'Usa HTTPS', 'en': 'Uses HTTPS'},
                           'uses-http2': {
                'link': 'https://web.dev/uses-http2', 'pt': 'Não usa HTTP/2 para todos os seus recursos', 'en': 'Does not use HTTP/2 for all of its resources'},
                           'uses-passive-event-listeners': {
                'link': 'https://web.dev/uses-passive-event-listeners', 'pt': 'Uso de passive listeners para melhorar a performance de scroll', 'en': 'Uses passive listeners to improve scrolling performance'},
                           'no-document-write': {
                'link': 'https://web.dev/no-document-write', 'pt': 'Evite &#39;document.write()&#39;', 'en': 'Avoids &#39;document.write()&#39;'},
                           'external-anchors-use-rel-noopener': {
                'link': 'https://web.dev/external-anchors-use-rel-noopener', 'pt': 'Não abre novas abas usando &#39;rel="noopener"&#39;', 'en': 'Does not open external anchors using &#39;rel="noopener"&#39;'},
                           'geolocation-on-start': {
                'link': 'https://web.dev/geolocation-on-start', 'pt': 'Evite perguntar por permissão de geolocalização no carregamento da página', 'en': 'Avoids requesting the geolocation permission on page load'},
                           'doctype': {
                'link': 'https://web.dev/doctype', 'pt': 'Doctype', 'en': 'Doctype'},
                           'no-vulnerable-libraries': {
                'link': 'https://web.dev/no-vulnerable-libraries', 'pt': 'Evite bibliotecas de front-end JavaScript com vulnerabilidades de segurança conhecidas', 'en': 'Avoids front-end JavaScript libraries with known security vulnerabilities'},
                           'js-libraries': {
                'link': 'https://web.dev/js-libraries', 'pt': 'JS libraries', 'en': 'JS libraries'},
                           'notification-on-start': {
                'link': 'https://web.dev/notification-on-start', 'pt': 'Evite perguntar por permissão de notificações no carregamento da página', 'en': 'Avoids requesting the notification permission on page load'},
                           'deprecations': {
                'link': 'https://web.dev/deprecations', 'pt': 'Evite APIs depreciadas', 'en': 'Avoids deprecated APIs'},
                           'password-inputs-can-be-pasted-into': {
                'link': 'https://web.dev/password-inputs-can-be-pasted-into', 'pt': 'Allows users to paste into password fields', 'en': 'Allows users to paste into password fields'},
                           'errors-in-console': {
                'link': 'https://web.dev/errors-in-console', 'pt': 'Os erros do Browser são impressos no console', 'en': 'Browser errors were logged to the console'},
                           'image-aspect-ratio': {
                'link': 'https://web.dev/image-aspect-ratio', 'pt': 'Exibe imagens com proporção incorreta', 'en': 'Displays images with incorrect aspect ratio'},
                           'viewport': {
                'link': 'https://web.dev/viewport', 'pt': 'Possui uma tag &#39;&lt;meta name="viewport"&gt;&#39; com &#39;width&#39; ou &#39;initial-scale&#39;', 'en': 'Has a &#39;&lt;meta name="viewport"&gt;&#39; tag with &#39;width&#39; or &#39;initial-scale&#39;'},
                           'meta-description': {
                'link': 'https://web.dev/meta-description', 'pt': 'O documento tem uma meta description', 'en': 'Document has a meta description'},
                           'http-status-code': {
                'link': 'https://web.dev/http-status-code', 'pt': 'A página têm um código HTTP de sucesso', 'en': 'Page has successful HTTP status code'},
                           'link-text': {
                'link': 'https://web.dev/link-text', 'pt': 'Os links têm texto descritivo', 'en': 'Links have descriptive text'},
                           'is-crawlable': {
                'link': 'https://web.dev/is-crawable', 'pt': 'A página não está bloqueada de indexação', 'en': 'Page isn’t blocked from indexing'},
                           'robots-txt': {
                'link': 'https://web.dev/robots-txt', 'pt': 'Robots.txt', 'en': 'Robots.txt'},
                           'hreflang': {
                'link': 'https://web.dev/hreflang', 'pt': 'O documento tem um &#39;hreflang&#39; válido', 'en': 'Document has a valid &#39;hreflang&#39;'},
                           'canonical': {
                'link': 'https://web.dev/canonical', 'pt': 'O document tem um &#39;rel=canonical&#39; válido', 'en': 'Document has a valid &#39;rel=canonical&#39;'},
                           'font-size': {
                'link': 'https://web.dev/font-size', 'pt': 'O documento usa fontes de tamanhos legíveis', 'en': 'Document uses legible font sizes'},
                           'plugins': {
                'link': 'https://web.dev/plugins', 'pt': 'O documento evita plugins', 'en': 'Document avoids plugins'},
                           'tap-targets': {
                'link': 'https://web.dev/tap-targets','pt':'Alvos de toques não são dimensionados apropriadamente','en':'Tap targets are not sized appropriately'},
                           'structured-data': {
                'link': 'https://web.dev/structured-data', 'pt': 'Os dados estruturados são válidos', 'en': 'Structured data is valid'},
                           'load-fast-enough-for-pwa': {
                'link': 'https://web.dev/load-fast-enough-for-pwa', 'pt': 'O carregamento da página não é rápido o suficiente no 3G', 'en': 'Page load is not fast enough on 3G'},
                           'works-offline': {
                'link': 'https://web.dev/works-offline', 'pt': 'Não responde com status 200 quando está offline', 'en': 'Does not respond with a 200 when offline'},
                           'offline-start-url': {
                'link': 'https://web.dev/offline-start-url','pt':'Offline Start URL','en':'Offline Start URL'},
                           'service-worker': {
                'link': 'https://web.dev/service-worker', 'pt': 'Não registra um service worker', 'en': 'Does not register a service worker'},
                           'installable-manifest': {
                'link': 'https://web.dev/installable-manifest','pt':'Manifest Instalável','en':'Installable Manifest'},
                           'redirects-http': {
                'link': 'https://web.dev/redirects-http', 'pt': 'Redireciona tráfego HTTP para HTTPS', 'en': 'Redirects HTTP traffic to HTTPS'},
                           'splash-screen': {
                'link': 'https://web.dev/splash-screen', 'pt': 'Is not configured for a custom splash screen', 'en': 'Is not configured for a custom splash screen'},
                           'themed-omnibox': {
                'link': 'https://web.dev/themed-omnibox', 'pt': 'A barra de endereços não condiz com as cores da marca', 'en': 'Address bar does not match brand colors'},
                           'content-width': {
                'link': 'https://web.dev/content-width', 'pt': 'O conteúdo é dimensionado corretamente para o viewport', 'en': 'Content is sized correctly for the viewport'},
                           'without-javascript': {
                'link': 'https://web.dev/without-javascript', 'pt': 'Possui algum conteúdo quando o JavaScript não está habilitado', 'en': 'Contains some content when JavaScript is not available'},
                           'apple-touch-icon': {
                'link': 'https://web.dev/apple-touch-icon/','pt':'Apple Touch Icon','en':'Apple Touch Icon'},
                           'pwa-cross-browser': {
                'link': 'https://web.dev/pwa-cross-browser', 'pt': 'Site funciona cross-browser', 'en': 'Site works cross-browser'},
                           'pwa-page-transitions': {
                'link': 'https://web.dev/pwa-page-transitions', 'pt': 'As transições de páginas não parecem travar devido à rede', 'en': "Page transitions don't feel like they block on the network"},
                            'pwa-each-page-has-url': {
                'link': 'https://web.dev/pwa-each-page-has-url', 'pt': 'Cada página tem uma URL', 'en': 'Each page has a URL'},
                },

'subtitles':{'en':{
                  'Progressive Web App':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Changes in PWA Audit score</b></div>',
                  'Performance':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Changes in Performance Audit score</b></div>',
                  'Accessibility':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Changes in Accessibility Audit score</b></div>',
                  'Best Practices':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Changes in Best Practices Audit score</b></div>',
                  'SEO':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Changes in SEO Audit score</b></div>',
                  },
             'pt':{
                  'Progressive Web App':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Mudanças de Nota da Auditoria de PWA</b></div>',
                  'Performance':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Mudanças de Nota da Auditoria de Performance</b></div>',
                  'Accessibility':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Mudanças de Nota da Auditoria de Acessibilidade</b></div>',
                  'Best Practices':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Mudanças de Nota da Auditoria de Melhores Práticas</b></div>',
                  'SEO':'<br><div style="font-size:15px;text-align:center;color:darkblue"><b>Mudanças de Nota da Auditoria de SEO</b></div>',
                  },
            },
}

dict_texts = {'text1':{
                          'en':'<br> The %s topic(s) with the greatest change are detailed below:<br>',
                          'pt':'<br> Os %s tópico(s) com maiores mudanças estão detalhados abaixo:<br>',
                         },
               'text2':{
                          'en':'<span style="color:red"><b>Main negative changes:</b></span>',   
                          'pt':'<span style="color:red"><b>Principais mudanças negativas:</b></span>',
                         },
               'text3':{
                          'en':'<span style="color:green"><b>Main positive changes:</b></span>',
                          'pt':'<span style="color:green"><b>Principais mudanças positivas:</b></span>',
                         },
               'text4':{
                          'en':'Average %s Score',
                          'pt':'%s Score Médio',
                         },
              }

perf_audits = ['cumulative-layout-shift',
               'largest-contentful-paint',
               'first-contentful-paint',
               'first-meaningful-paint',
               'speed-index',
               'interactive',
               'first-cpu-idle',
               #'max-potential-fid',
               'estimated-input-latency',
               #'total-blocking-time',
               'render-blocking-resources',
               'uses-responsive-images',
               'offscreen-images',
               'unminified-css',
               'unminified-javascript',
               'unused-css-rules',
               'uses-optimized-images',
               'uses-webp-images',
               'uses-text-compression',
               'uses-rel-preconnect',
               'time-to-first-byte',
               'redirects',
               'uses-rel-preload',
               'efficient-animated-content',
               'total-byte-weight',
               'uses-long-cache-ttl',
               'dom-size',
               'critical-request-chains',
               'user-timings',
               'bootup-time',
               'mainthread-work-breakdown',
               #'font-display',
               #'performance-budget',
               #'resource-summary',
               #'third-party-summary',
               'network-requests',
               #'network-rtt',
               #'network-server-latency',
               #'main-thread-tasks',
               #'diagnostics',
               #'metrics',
               'screenshot-thumbnails',
               'final-screenshot',
               ]
pwa_audits = ['load-fast-enough-for-pwa',
              'works-offline',
              'offline-start-url',
              'is-on-https',
              'service-worker',
              'installable-manifest',
              'redirects-http',
              'splash-screen',
              'themed-omnibox',
              'content-width',
              'viewport',
              'without-javascript',
              'apple-touch-icon',
              'pwa-cross-browser',
              'pwa-page-transitions',
              'pwa-each-page-has-url',
              ]
access_audits = ['accesskeys',
                 'aria-allowed-attr',
                 'aria-required-attr',
                 'aria-required-children',
                 'aria-required-parent',
                 'aria-roles',
                 'aria-valid-attr-value',
                 'aria-valid-attr',
                 'audio-caption',
                 'button-name',
                 'bypass',
                 'color-contrast',
                 'definition-list',
                 'dlitem',
                 'document-title',
                 'duplicate-id',
                 'frame-title',
                 'html-has-lang',
                 'html-lang-valid',
                 'image-alt',
                 'input-image-alt',
                 'label',
                 'layout-table',
                 'link-name',
                 'list',
                 'listitem',
                 'meta-refresh',
                 'meta-viewport',
                 'object-alt',
                 'tabindex',
                 'td-headers-attr',
                 'th-has-data-cells',
                 'valid-lang',
                 'video-caption',
                 'video-description',
                 'accesskeys',
                 'logical-tab-order',
                 'focusable-controls',
                 'interactive-element-affordance',
                 'managed-focus',
                 'focus-traps',
                 'custom-controls-labels',
                 'custom-controls-roles',
                 'visual-order-follows-dom',
                 'offscreen-content-hidden',
                 'heading-levels',
                 'use-landmarks']
best_audits = ['appcache-manifest',
               'is-on-https',
               'uses-http2',
               'uses-passive-event-listeners',
               'no-document-write',
               'external-anchors-use-rel-noopener',
               'geolocation-on-start',
               'doctype',
               'no-vulnerable-libraries',
               'js-libraries',
               'notification-on-start',
               'deprecations',
               'password-inputs-can-be-pasted-into',
               'errors-in-console',
               'image-aspect-ratio']
seo_audits = ['viewport',
              'document-title',
              'meta-description',
              'http-status-code',
              'link-text',
              'is-crawlable',
              'robots-txt',
              'hreflang',
              'canonical',
              'font-size',
              'plugins',
              'mobile-friendly',
              'structured-data']

loop_audits = [['Performance',perf_audits,'perf',15],['Progressive Web App',pwa_audits,'pwa',10],['Accessibility',access_audits,'access',10],
               ['Best Practices',best_audits,'best',10],['SEO',seo_audits,'seo',8]]

config_dict = yaml.load(email_to_send[table_name])
audit_file_emailtext = {}

date_limit = date - timedelta(days=1)
email_limit_hour = (datetime.now() - timedelta(days=12/24)).strftime("%Y-%m-%d %H:00:00")

for url_id in url_ids:
    check_aggregation = config_dict['aggregation']
    cursor.execute("select template from monitoring_links where id = %s;" %url_id)
    template = cursor.fetchall()[0]['template']
    if template == None:
        template = ''
    if check_aggregation == 'hour':
        #gets last 2 entries for the specified url
        url_dict = {}
        if url_id not in alerts_summary:
            alerts_summary[url_id] = []

        for loop_audit in loop_audits:
            if loop_audit[2] not in config_dict[url_id]:
                logging.info('url id %s is not checked for %s' %(url_id, loop_audit[0]))
                continue

            audit_type = loop_audit[0]
            sub_audits = loop_audit[1]        
            audit_tolerance = loop_audit[3]
            cursor.execute("select datetime,url,value from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s', 'mobile')\
                           and datetime > '%s' and value is not null order by datetime desc limit 0,3" %(audit_type, url_id, date_limit))
            earlier_results = cursor.fetchall()
            early_values = []
            for early_result in earlier_results:
                early_values.append(float(early_result['value']))

            cursor.execute("select datetime,url,value from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s', 'mobile')\
                           and datetime > '%s' and value is not null order by datetime desc limit 3,5" %(audit_type, url_id, date_limit))      
            older_results = cursor.fetchall()
            old_values = []
            for old_value in older_results:
                old_values.append(float(old_value['value']))

            if earlier_results == () or older_results == ():
                logging.info('Not enough data for url id %s' %url_id)
                continue

            if early_values == [] or old_values == []:
                logging.info("No dates to compare for url id %s on %s. Proceding to next url..." %(url_id, audit_type))
                continue
            siteurl = earlier_results[0]['url']

            # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
            cursor.execute("select lighthouse from alerts_analysis_history where url_id = '%s';" %url_id)
            last_alert_date = cursor.fetchall()
            if last_alert_date != ():
                last_alert_date = last_alert_date[0]['lighthouse']         #gets the last date from the alerts sent in past
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
                                logging.info("There is already an email alert sent to %s about Lighthouse data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour, sent_date))
                                break
                            else:
                                logging.info("There is already an email alert sent to %s about Lighthouse data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour))
                                break
                    except:
                        pass

            score1 = stats.trim_mean(early_values, 0.25)
            score0 = stats.trim_mean(old_values, 0.25)
            counted_values = len(early_values) 

            # ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
            # gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
            cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_limit_hour))
            last_emails_content = cursor.fetchall()

            #_absdelta and _percdelta are the anomaly detectors
            score_absdelta = score1 - score0
            try:
                score_percdelta = (score1/score0)-1
            except:
                score_percdelta = float("inf")
            text = ''

            logging.info('Analyzing %s for %s' %(loop_audit[0], siteurl))
            format_type = float
            
            #Loop through audit tyeps, if the changes are greater than specified points it is considered and anomaly
            if abs(score_absdelta) >= loop_audit[3]:
                 if template != "":
                     type_alert = ["Score", audit_type + template + "mobile", '', False]
                 else:
                     type_alert = ["Score", audit_type, 'mobile', False]
                 if score_absdelta < 0:
                    sign = '-'
                    type_alert[2] = 'down'
                    color = 'red'
                    sql_direction1 = 'asc'
                    sql_direction2 = 'desc'
                 else:
                    sign = '+'
                    type_alert[2] = 'up'
                    color = 'green'
                    sql_direction1 = 'desc'
                    sql_direction2 = 'asc'
                 if abs(score_absdelta) > loop_audit[3]*2.5:
                    type_alert[3] = True
                 logging.info("Change found: %s" %type_alert)

                 var_email = avoid_same_content(last_emails_content, type_alert)
                 if var_email == True:                    
                     alerts_summary[url_id].append(type_alert)
                     good_audit_reasons = []
                     good_audit_reasons_order = []
                     bad_audit_reasons = []
                     bad_audit_reasons_order = []

                     cursor.execute("select datetime from (select url,datetime,value from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s','mobile') and value \
is not null and datetime > '%s' order by datetime desc limit 0,3) as a order by value %s limit 1;" %(audit_type, url_id, date_limit, sql_direction1))
                     date1 = cursor.fetchall()[0]['datetime']
                                                           
                     cursor.execute("select datetime from (select url,datetime,value from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s','mobile') and value \
is not null and datetime > '%s' order by datetime desc limit 3,5) as a order by value %s limit 1;" %(audit_type, url_id, date_limit, sql_direction2))
                     date0 = cursor.fetchall()[0]['datetime']

                     cursor.execute("select value,datetime from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s', 'mobile') and value is not null and \
datetime >= '%s' order by datetime asc;" %(audit_type, url_id, date0))
                     graph_results = cursor.fetchall()
                     if len(graph_results) >= 5:
                         dates_graph = []
                         values_graph = []
                         for graph_result in graph_results:
                             dates_graph.append(graph_result['datetime'])
                             values_graph.append(float(graph_result['value']))
                         font0 = FontProperties()
                         font0.set_family('verdana')
                         font0.set_size(8)
                         font1 = FontProperties()
                         font1.set_family('verdana')
                         font1.set_size(10)
                         font1.set_weight('bold')
                         plt.figure(figsize=(7.5, 2))
                         plt.rcParams['axes.facecolor'] = 'w'
                         plt.xticks(range(len(dates_graph)), dates_graph, rotation = 25, color = 'black', fontproperties = font0)    #enables ploting float vs string
                         plt.title('Lighthouse %s Score' %audit_type, color = 'black' , fontproperties = font1)
                         plt.axis((-1,len(dates_graph),0,100))
                         i = 0

                         bar_position = len(dates_graph) - (counted_values + 0.5)                     
                         plt.axvline(x = bar_position, linestyle='--', color = color)
                         for number in values_graph:
                             if i < bar_position and color == 'green':
                                 plt.plot(i, number, 'h', color = 'red')
                             elif i < bar_position and color == 'red':
                                 plt.plot(i, number, 'h', color = 'green')
                             elif i >= bar_position:
                                 plt.plot(i, number, 'H', color = color)
                             i += 1
                         plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
                     else:
                         logging.info("Not enough data points to plot a grapg for %s" %siteurl)
                         
                     for sub_audit in sub_audits:
                         if sub_audit in ['first-contentful-paint', 'first-meaningful-paint', 'first-cpu-idle', 'interactive', 'speed-index']:
                             continue
                         cursor.execute("select * from lighthouse where (audit_type, audit, url_id, device, datetime) = ('%s','%s','%s','mobile','%s') limit 1;" %(audit_type, sub_audit, url_id, date1))
                         sub_audit_results1 = cursor.fetchall()

                         cursor.execute("select * from lighthouse where (audit_type, audit, url_id, device, datetime) = ('%s','%s','%s','mobile','%s') limit 1;" %(audit_type, sub_audit, url_id, date0))
                         sub_audit_results0 = cursor.fetchall()
                         if len(sub_audit_results0) < 1 or len(sub_audit_results1) < 1:
                             logging.info("Not enough data for sub audit %s" %sub_audit)
                             continue
                         sub_audit_score0 = float(sub_audit_results0[0]['value'])
                         sub_audit_score1 = float(sub_audit_results1[0]['value'])
                         try:
                             value = sub_audit_score1 - sub_audit_score0
                             if value > 0:
                                 good_audit_reasons.append(sub_audit)
                                 good_audit_reasons_order.append(value)
                             elif value < 0:
                                 bad_audit_reasons.append(sub_audit)
                                 bad_audit_reasons_order.append(value)
                         except:
                             pass

                     if score_percdelta != float("inf"):
                         text = get_comparison_phrases(siteurl, dict_texts['text4'][language] %audit_type, score0, date0, score1, date1, sign, color, abs(score_percdelta), type_alert, format_type, 'singular')
                     else:
                         text += get_comparison_phrases_zero(siteurl, dict_texts['text4'][language] %audit_type, date0, score1, date1, color, format_type)

                     if len(graph_results) >= 5:
                         text += '<br><img src="cid:Graph%s.png"><br>' %n
                         n += 1
                         
                     if len(bad_audit_reasons) > 0 and score_absdelta < 0:
                         line_count = 1
                         bad_audit_reasons = sort_email_from_list(bad_audit_reasons_order, bad_audit_reasons) 
                         bad_audit_reasons = bad_audit_reasons[0:3]
                         text += dict_texts['text1'][language] %len(bad_audit_reasons)
                         # negative changes
                         text += dict_texts['text2'][language]             
                         for bad_audit in bad_audit_reasons:
                             if dict_audits['semantic'][bad_audit][language] not in text:
                                 text += '<br>%s. <b><a href="%s">%s</a></b>' %(line_count, dict_audits['semantic'][bad_audit]['link'], dict_audits['semantic'][bad_audit][language])
                                 line_count += 1
                         text += '<br><br>'

                         # positive changes
                     elif len(good_audit_reasons) > 0 and score_absdelta > 0:
                         line_count = 1
                         good_audit_reasons = sort_email_from_list(good_audit_reasons_order, good_audit_reasons)
                         good_audit_reasons = good_audit_reasons[0:3]
                         text += dict_texts['text3'][language]             
                         for good_audit in good_audit_reasons:
                             if dict_audits['semantic'][good_audit][language] not in text:
                                 text += '<br>%s. <b><a href="%s">%s</a></b>' %(line_count, dict_audits['semantic'][good_audit]['link'], dict_audits['semantic'][good_audit][language])
                                 line_count += 1
                         text += '<br><br>'

                 alerts_summary[url_id].append(type_alert)
                 if text != '' and audit_type not in audit_file_emailtext:
                     audit_file_emailtext[audit_type] = dict_audits['subtitles'][language][audit_type]
                     
                 if text != '':
                     audit_file_emailtext[audit_type] += text
                     dict_urls[url_id] = str(date1)
                     analyzed_urls[execute_file[2]] = dict_urls


    elif check_aggregation == 'day' and time_check == 'hour':
        logging.info("Url %s: The consolidated day analysis will be made onlyat %s for email group %s" %(url_id, send_hour, email_group_id))

    elif check_aggregation == 'day' and time_check == 'day':
        #gets last 2 days (up to 48 entries) for the specified url
        url_dict = {}
        if url_id not in alerts_summary:
            alerts_summary[url_id] = []

        for loop_audit in loop_audits:
            if loop_audit[2] not in config_dict[url_id]:
                logging.info('url id %s is not checked for %s' %(url_id, loop_audit[0]))
                continue

            audit_type = loop_audit[0]
            sub_audits = loop_audit[1]        
            audit_tolerance = loop_audit[3]

            cursor.execute("select url,datetime from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s','mobile') order by id desc limit 1;" %(audit_type, url_id))
            results = cursor.fetchall()
            if results == ():
                logging.info('Not enough data for url id %s' %url_id)
                continue
            else:
                siteurl = results[0]['url']
                last_day_end = results[0]['datetime']
                last_day_begin = last_day_end - timedelta(days=23/24)
                first_day_end = last_day_begin - timedelta(days=1/24)
                first_day_begin = first_day_end - timedelta(days=23/24)

            cursor.execute("select avg(value) from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s','mobile') and datetime between '%s' and '%s' order by id desc limit 1;" %(audit_type, url_id, first_day_begin, first_day_end))
            first_results = cursor.fetchall()
            cursor.execute("select avg(value) from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s','mobile') and datetime between '%s' and '%s' order by id desc limit 1;" %(audit_type, url_id, last_day_begin, last_day_end))
            last_results = cursor.fetchall()

            if first_results[0]['avg(value)'] == None or last_results[0]['avg(value)'] == None:
                logging.info('Not enough data for url id %s %s on %s' %(url_id, siteurl, audit_type))
                continue

            day0 = first_results[0]
            day1 = last_results[0]
            date0 = str(first_day_begin.date())
            date1 = str(last_day_begin.date())
                
            # ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
            cursor.execute("select lighthouse from alerts_analysis_history where url_id = '%s';" %url_id)
            last_alert_date = cursor.fetchall()
            if last_alert_date != ():
                last_alert_date = last_alert_date[0]['lighthouse']         #gets the last date from the alerts sent in past
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
                                logging.info("There is already an email alert sent to %s about Lighthouse data collected for %s in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour, sent_date))
                                break
                            else:
                                logging.info("There is already an email alert sent to %s about Lighthouse data collected for %s in %s. \
A new alert on the same issue won't be sent." %(toaddr, siteurl, current_hour))
                                break
                    except:
                        pass

            score0 = float(day0['avg(value)'])
            score1 = float(day1['avg(value)'])
            
            #_absdelta and _percdelta are the anomaly detectors
            score_absdelta = score1 - score0
            try:
                score_percdelta = (score1/score0)-1
            except:
                score_percdelta = float("inf")
            text = ''

            logging.info('Analyzing %s for %s' %(loop_audit[0], siteurl))
            format_type = float
            #Loop through audit types, if the changes are greater than specified points it is considered and anomaly
            if abs(score_absdelta) >= loop_audit[3]/2.5:
                 if template != "":
                     type_alert = ["Score", audit_type + " " + template, '', False]
                 else:
                     type_alert = ["Score", audit_type, '', False]
                 if score_absdelta < 0:
                    sign = '-'
                    type_alert[2] = 'down'
                    color = 'red'
                 else:
                    sign = '+'
                    type_alert[2] = 'up'
                    color = 'green'
                 if abs(score_absdelta) > loop_audit[3]:
                    type_alert[3] = True
                 logging.info("Change found: %s" %type_alert)
                    
                 positive_audit_reasons = []
                 positive_audit_reasons_order = []
                 negative_audit_reasons = []
                 negative_audit_reasons_order = []

                 cursor.execute("select * from lighthouse where (audit_type, audit, url_id, device) = ('%s','score','%s','mobile') and datetime between '%s' and '%s' limit 24;" %(audit_type, url_id, last_day_begin, last_day_end))
                 audit_results_debug = cursor.fetchall()
                 if len(audit_results_debug) < 2:
                     logging.info("Not enough data to determine greatest change for audit %s" %loop_audit[0])
                     continue

                 i = len(audit_results_debug) - 1
                 for audit_result_debug in audit_results_debug:
                     try:
                         audit_time = audit_results_debug[i]['datetime']
                         audit_score1 = float(audit_results_debug[i]['value'])
                         audit_score0 = float(audit_results_debug[i-1]['value'])
                         value = audit_score1 - audit_score0
                         if value > 0:
                             positive_audit_reasons.append(audit_time)
                             positive_audit_reasons_order.append(value)
                         elif value < 0:
                             negative_audit_reasons.append(audit_time)
                             negative_audit_reasons_order.append(value)
                     except:
                         pass
                     i -= 1
                                                  
                 if sign == '+':
                     reason = max(positive_audit_reasons_order)
                     reason_time = positive_audit_reasons[positive_audit_reasons_order.index(reason)]
                 elif sign == '-':
                     reason = min(negative_audit_reasons_order)
                     reason_time = negative_audit_reasons[negative_audit_reasons_order.index(reason)]
                 
                 if score_percdelta != float("inf"):
                     text = get_comparison_phrases(siteurl, dict_texts['text4'][language] %audit_type %audit_type, score0, date0, score1, date1, sign, color, abs(score_percdelta), type_alert, format_type, 'singular')
                 else:
                     text += get_comparison_phrases_zero(siteurl, dict_texts['text4'][language] %audit_type %audit_type, date0, score1, date1, color, format_type)                     
                 text += talk_about_time(str(reason_time), sign, color) #comments on the email which hour is more likely to have shown this problem
                 
                 alerts_summary[url_id].append(type_alert)
                 good_audit_reasons = []
                 good_audit_reasons_order = []
                 bad_audit_reasons = []
                 bad_audit_reasons_order = []
                 for sub_audit in sub_audits:
                     if sub_audit in ['first-contentful-paint', 'first-meaningful-paint', 'first-cpu-idle', 'interactive', 'speed-index']:
                         continue
                     cursor.execute("select * from lighthouse where datetime <= '%s' and (audit_type, audit, url_id, device) = ('%s','%s','%s','mobile') order by datetime desc limit 0,2;" %(reason_time, audit_type, sub_audit, url_id))
                     sub_audit_results = cursor.fetchall()
                     if len(sub_audit_results) < 2:
                         logging.info("Not enough data for sub audit %s" %sub_audit)
                         continue
                     sub_audit_score0 = float(sub_audit_results[1]['value'])
                     sub_audit_score1 = float(sub_audit_results[0]['value'])
                     try:
                         value = sub_audit_score1 - sub_audit_score0
                         if value > 0:
                             good_audit_reasons.append(sub_audit)
                             good_audit_reasons_order.append(value)
                         elif value < 0:
                             bad_audit_reasons.append(sub_audit)
                             bad_audit_reasons_order.append(value)
                     except:
                         pass

                 if len(bad_audit_reasons) > 0 and score_absdelta < 0:
                     line_count = 1
                     bad_audit_reasons = sort_email_from_list(bad_audit_reasons_order, bad_audit_reasons) 
                     bad_audit_reasons = bad_audit_reasons[0:3]
                     text += dict_texts['text1'][language] %len(bad_audit_reasons)
                     # negative changes
                     text += dict_texts['text2'][language]             
                     for bad_audit in bad_audit_reasons:
                         if dict_audits['semantic'][bad_audit][language] not in text:
                             text += '<br>%s. <b><a href="%s">%s</a></b>' %(line_count, dict_audits['semantic'][bad_audit]['link'], dict_audits['semantic'][bad_audit][language])
                             line_count += 1
                     text += '<br><br>'

                     # positive changes
                 elif len(good_audit_reasons) > 0 and score_absdelta > 0:
                     line_count = 1
                     good_audit_reasons = sort_email_from_list(good_audit_reasons_order, good_audit_reasons)
                     good_audit_reasons = good_audit_reasons[0:3]
                     text += dict_texts['text3'][language]             
                     for good_audit in good_audit_reasons:
                         if dict_audits['semantic'][good_audit][language] not in text:
                             text += '<br>%s. <b><a href="%s">%s</a></b>' %(line_count, dict_audits['semantic'][good_audit]['link'], dict_audits['semantic'][good_audit][language])
                             line_count += 1
                     text += '<br><br>'

            if text != '' and audit_type not in audit_file_emailtext:
                audit_file_emailtext[audit_type] = dict_audits['subtitles'][language][audit_type]
                
            if text != '':
                audit_file_emailtext[audit_type] += text
                dict_urls[url_id] = str(date1)
                analyzed_urls[execute_file[2]] = dict_urls
    
for key in audit_file_emailtext.keys():
    if audit_file_emailtext[key] != '':
        file_emailtext += audit_file_emailtext[key]
        
#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
#email sending part
if file_emailtext != '':
    title = title_to_email_section('Lighthouse Audits','change')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
