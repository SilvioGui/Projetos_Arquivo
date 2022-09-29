from app.model import Collector,Answers_total
from peewee import JOIN
from datetime import datetime, timedelta,date
from app.config import config
import requests
import os, sys

key = config['survey_monkey_key']


#---VERIFICAÇÃO DATA---#

a=input('Digite a data de inicio ')
b=input('Digite a data do fim ')
date1 = date.today() - datetime.strptime(a, '%Y-%m-%d').date()
date2 = date.today() - datetime.strptime(b, '%Y-%m-%d').date()
c=int(str(date1)[0:3])
d=int(str(date2)[0:3])

print(Collector.select().where((Collector.date >= datetime.now() - timedelta(days=c)) & (Collector.date <= datetime.now() - timedelta(days=d))).order_by(Collector.date.desc()))
#--BUSCA NO BANCO OS COLLECTOR_ID PARA FAZER O REQUEST--#
for collector_model in Collector.select().where((Collector.date >= datetime.now() - timedelta(days=c)) & (Collector.date <= datetime.now() - timedelta(days=d))).order_by(Collector.date.desc()):
    contage_total = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, None: 0}
    print(collector_model.date - timedelta(days=1))
    #--REQUEST DAS INFORMAÇÕES PELO SURVEY MONKEY--#
    stats = requests.get('https://api.surveymonkey.com/v3/collectors/{}/stats'.format(collector_model.collector_id),
                         headers={'Authorization': 'bearer {}'.format(key)}).json()
    print(stats)
    data_answers=Answers_total.select().where(Answers_total.dados_diarios == (collector_model.date - timedelta(days=1)))
    #--VERIFICA SE A DATA JÁ ESTÁ INCLUSA NO BANCO--#
    try:
        data=data_answers.get()#-> VAI DAR ERRO QUANDO NÃO TIVER INFORMAÇÃO NO BANCO(LIMITAÇÃO DO PEEWEE)
    except:
        data=None     
    if data==None:
        print('passou do if')
        #--INSERT NO BANCO DE DADOS--#
        Answers_total.create(
        dados_diarios  = (collector_model.date - timedelta(days=1)),
        enviados  = stats['mail_status']['sent'],
        nao_entregues  = stats['mail_status']['bounced'],
        abertos = stats['mail_status']['opened'],
        nao_abertos  =stats['mail_status']['not_sent'],
        completamente_respondido  = stats['survey_response_status']['completely_responded'],
        nao_respondido  = stats['survey_response_status']['not_responded'],
        parcialmente_respondido  = stats['survey_response_status']['partially_responded'],
        descadastrados = stats['mail_status']['opted_out'],
        cliques_no_Link  = stats['mail_status']['link_clicked']
        )




