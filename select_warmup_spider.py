#Warm up cache by daily craw
from itertools import count
from lxml import html
import scrapy
import time
import logging
import sys, os
import pymysql.cursors
import datetime
from warnings import filterwarnings
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/")
from lib import auth
import urllib
from urllib.parse import urlparse
from scrapy.utils.request import referer_str
import requests
from bs4 import BeautifulSoup
                                 
class select_warmup(scrapy.Spider):
    name = 'select_warmup'
    custom_settings = {
        'CONCURRENT_REQUESTS': 4,
        'ROBOTSTXT_OBEY': True,
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'CONCURRENT_REQUESTS_PER_IP': 4,
        'DOWNLOAD_FAIL_ON_DATALOSS': False,
        'REDIRECT_MAX_TIMES': 5,
        'REDIRECT_ENABLED': True,
    }

    
    def log_silvio(self,msg):
        arquivo = open('silvio.txt', 'a')
        arquivo.write(str(msg))
        arquivo.close()

    def start_requests(self):
        self.log_silvio('teste.........................\n')

        db = auth.getConnection()
        cursor = db.cursor()
        f = open("server_id.txt", "r")
        f = f.read(1)
        time = '{:%H:%M}'.format(datetime.datetime.now())
        #cursor.execute('select * from warm_urls where (active, server_id) = (1,' + f + ') and crawl_time like "%%{}%%";'.format(time))
        cursor.execute('select * from warm_urls where (active, server_id) = (1,' + f + ');')
        sites_warmup = cursor.fetchall()
        print(sites_warmup)

        for site_warmup in sites_warmup:

            
            cont=1
            sitemap_geral=""
            while(cont>0):
                sitemap_xml = site_warmup['sitemaps_to_crawl']
                sitemap_xml = sitemap_xml.replace('.xml','-%s.xml'.format(cont))
                sitemap_xml_result = requests.get(sitemap_xml)
                status = str(sitemap_xml_result.status_code)
                
                if status != '200':
                    self.log_silvio('não localizou o arquivo xml: %s'.format(sitemap_xml))
                    count=-1
                    break
                sitemap_xml = BeautifulSoup(sitemap_xml.text, 'html.parser')
                urls_list = sitemap_xml.findAll('url')
                sitemap_geral = sitemap_geral + urls_list
                count+=1
            print('------------------------->SITEMAP:\n %s',sitemap_geral)
    '''









        a=('https://www.dafiti.com.br/masculino/calcados-masculinos/tenis/tenis-casual/calcados-femininos/calcados-infantis/sapatos/tenis-feminino-salto-alto.sdex',
           'https://www.dafiti.com.br/feminino/casa/decoracao/objetos-decorativos/adesivos/quarto/decoracao-e-acessorios/infantil/cozinha-parede-cinza.sdex',
           'https://www.dafiti.com.br/masculino/roupas-masculinas/calcas-casuais/calca-tecido/calca-masculina-militar.sdex',
           'https://www.dafiti.com.br/masculino/bolsas-e-acessorios-masculinos/carteiras/trifold.sdex',
           'https://www.dafiti.com.br/feminino/casa/moveis/quarto/guarda-roupa/guarda-roupa-de-bebe/comoda-4-gavetas-lila.sdex')
        try:
            num=0
            for b in a:
                num=+1
                yield scrapy.Request(a[num], self.parse, dont_filter=True, headers={"User-Agent": 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) simplex warmup'})

        except ValueError:
            self.log_silvio('erro: %s',ValueError)
            '''

    def parse(self, response):
        msg = self.crawled(response.request, response)
        file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log',  urlparse(response.url).netloc + '_' + '{:%Y%m%d_%Hh}'.format(datetime.datetime.now()) + '.log'), 'a')
        file.write(('{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.today()) + ' ' + msg['msg'] + '\n') % msg['args'])
        file.close()

    def crawled(self, request, response):
        request_flags = ' %s' % str(request.flags) if request.flags else ''
        response_flags = ' %s' % str(response.flags) if response.flags else ''
        return {
            'level': logging.DEBUG,
            'msg': u"Crawled\t%(status)s\t%(request)s\t%(request_flags)s\t%(user_agent)s\t%(response_flags)s",
            'args': {
                'status': response.status,
                'request': request,
                'request_flags': request_flags,
                'user_agent': request.headers['User-Agent'],
                'response_flags': response_flags,
                # backward compatibility with Scrapy logformatter below 1.4 version
                'flags': response_flags
            }
        }
