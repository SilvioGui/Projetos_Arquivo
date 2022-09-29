from datetime import datetime, timedelta
from app.ftp import create_ftp
from app.config import planilhas_dir
from datetime import datetime, timedelta
import sys
from app.survey import Api
import logging
from app.config import config, assets_dir
from app.model import Collector, Pecuaristas, SiglasModel, Answers
import csv
import os
from app.jbs import JBSNotificacao

jbs_notificacao = JBSNotificacao()
today = datetime.today()
try:
    collectorRow = Collector.select().where(Collector.date == today).get()
    logging.info('emails foram enviados na data de hoje')
    sys.exit()
except Collector.DoesNotExist as e:
    logging.info('processando perguntas na surveymonkey')

ftp = create_ftp()
# ftp.cwd('PesquisaSatisfacao')
allfiles = ftp.nlst()    #gets all files in the current directory ordering from newest to oldest
logging.info('there are {} files in the selected directory'.format(len(allfiles)))

date = datetime.now()
filename = 'Cadastro Pecuarista - Pesquisa de Satisfacao_{}.csv'.format(date.strftime('%Y-%m-%d'))
logging.info("requesting {}".format(filename))

filename_fullpath = '{}/{}'.format(planilhas_dir, filename)
if os.path.exists(filename_fullpath):
    logging.info('{} is already present in the current directory'.format(filename))
    sys.exit()

#The above will connect you to your remote server. You can then change into PESQUISA_ABATE_2018_05_29.xlsx specific directory with:
logging.info("downloading file... {}".format(filename))
try:
    with open(filename_fullpath, 'wb') as file:
        ftp.retrbinary("RETR " + filename, file.write)
        file.close()
    logging.info("downloaded succesfully")
except Exception as e:
    logging.error('o arquivo {} não existe no FTP'.format(filename))
    sys.exit()

# trecho responsavel pelo envio do questionario por e-mail (via surveymonkey)
key = config['survey_monkey_key']

f = open(filename_fullpath, encoding='utf-8-sig')
entries = [entry.strip() for entry in f.readlines()]
headers = entries[0].split(';')
col_nCdPecuarista = 0
col_codigo_pecuarista = headers.index('nCdPecuarista')
col_email = headers.index('cEMail.Pecuarista')
col_pecuarista = headers.index('Pecuarista')
col_empresa = headers.index('Empresa')
col_telefone = headers.index('cTelefone.Pecuarista')
col_endereco = headers.index('Endereço.Pecuarista')
col_telefone2 = headers.index('cTelefone2.Pecuarista')
col_celular = headers.index('cTelefoneCelular.Pecuarista')
col_numero = headers.index('cNumero.Pecuarista')
col_complemento = headers.index('cComplemento.Pecuarista')
col_bairro = headers.index('cBairro.Pecuarista')
col_cep = headers.index('cCEP.Pecuarista')
col_cidade = headers.index('Cidade.Pecuarista')
col_uf = headers.index('UF.Pecuarista')
col_pais = headers.index('Pais.Pecuarista')
col_data = headers.index('DataUltimoAbate')
col_pedido = headers.index('nCdPedidoComercial')
col_fazenda = headers.index('nCdFazenda')
col_instrucao = headers.index('nCdInstrucao')

email_set = []
ids_registrados = []
#pode existir e-mail duplicado
#quando existir o delimitador de colunas (;) dentro de uma coluna, por padrao do csv ele tem que ter um enclosed, nesse caso seria o caracter (")
for entry in csv.reader(entries[1::], quotechar='"', delimiter=";", quoting=csv.QUOTE_ALL, skipinitialspace=True):
    email = entry[col_email]
    if ',' in email:
        email = email.split(',')[0]

    email = email.strip()
    nome = entry[col_pecuarista]
    info_pecuarista = {}
    info_pecuarista['nome'] = nome
    info_pecuarista['email'] = email
    person_id = entry[col_nCdPecuarista]
    telefone = entry[col_telefone]
    telefone2 = entry[col_telefone2]
    celular = entry[col_celular]
    info_pecuarista['id'] = person_id
    info_pecuarista['telefone'] = telefone
    info_pecuarista['telefone2'] = telefone2
    info_pecuarista['celular'] = celular
    info_pecuarista['empresa'] = entry[col_empresa]
    info_pecuarista['pedido'] = entry[col_pedido]
    info_pecuarista['data'] = datetime.strptime(entry[col_data], '%d/%m/%Y')
    info_pecuarista['local'] = entry[col_cidade]
    info_pecuarista['fazenda'] = entry[col_fazenda]
    info_pecuarista['instrucao'] = entry[col_instrucao]

    #inserindo na tabela
    pecuarista_data = {
        Pecuaristas.codigo_pecuarista: entry[col_codigo_pecuarista],
        Pecuaristas.data_ultimo_abate: info_pecuarista['data'],
        Pecuaristas.empresa: entry[col_empresa],
        Pecuaristas.pedido_comercial: entry[col_pedido],
        Pecuaristas.fazenda: entry[col_fazenda],
        Pecuaristas.nome: entry[col_pecuarista],
        Pecuaristas.endereco: entry[col_endereco],
        Pecuaristas.email: entry[col_email],
        Pecuaristas.telefone: entry[col_telefone],
        Pecuaristas.telefone_2: entry[col_telefone2],
        Pecuaristas.celular: entry[col_celular],
        Pecuaristas.endereco_numero: entry[col_numero],
        Pecuaristas.complemento: entry[col_complemento],
        Pecuaristas.bairro: entry[col_bairro],
        Pecuaristas.cep: entry[col_cep],
        Pecuaristas.cidade: entry[col_cidade],
        Pecuaristas.uf: entry[col_uf],
        Pecuaristas.pais: entry[col_pais],
        Pecuaristas.instrucao: entry[col_instrucao],
    }
    try:
        query = Pecuaristas.select()
        for k, v in pecuarista_data.items():
            query = query.where(k == v)
        pecuarista_model = query.get()
    except Pecuaristas.DoesNotExist:
        pecuarista_id = Pecuaristas.insert(pecuarista_data).execute()
        pecuarista_model = Pecuaristas.get_by_id(pecuarista_id)

    # salva na tabela para posteriormente ser notificado para cadastro na JBS
    if email is '' or email is None:
        jbs_notificacao.add_notification(pecuarista_model.id, jbs_notificacao.TIPO_PROPOSITO_EMAIL_VAZIO)


    # verificando se o e-mail passou pelo loop
    if pecuarista_model.id not in ids_registrados and email != '' and email is not None:
        info_pecuarista['model_id'] = pecuarista_model.id
        email_set.append(info_pecuarista)
        ids_registrados.append(pecuarista_model.id)

email_body_date = today

api = Api(key)
p = []
siglas_empresa = {}
logging.info('Key do sistema '+key)
for s in SiglasModel.select():
    for a in s.sigla.split(','):
        siglas_empresa[a] = s.nome


for s in email_set:
    if s['empresa'].upper() not in siglas_empresa:
        continue

    logging.info('enviando email para {} <{}>'.format(s['nome'], s['email']))
    p.append({
        'email': s['email'],
        'first_name': s['nome'],
        'extra_fields': {
            'data_abate': s['data'].strftime('%d/%m/%Y'),
            'local': siglas_empresa[s['empresa'].upper()],
            'id': s['model_id'],
        }
    })

# api da surveymonkey nao permite envio com e-mail igual, criando um list de dict para separar e-mail repetido
emails_list = []
items = []
while True:
    for item in p:
        if len(list(filter(lambda x: item['email'] in x['email'], items))) == 0:
            items.append(item)
    for i in items:
        p.pop(p.index(i))
    if len(items) == 0:
        break
    emails_list.append(items)
    items = []


for emails in emails_list:
    if len(emails) > 0:
        if api.collector_id == 0:
            response_with_recipients = api.sendEmails(emails)
        else:
            try:
                response_with_recipients = api.send_emails_with_collector_id(emails)
            except Exception:
                break

        # caso collector_id seja 0 aconteceu algo de errado
        if api.collector_id == 0 or api.collector_id is None:
            raise RuntimeError('collector_id invalido: {}'.format(api.collector_id))

        logging.debug(response_with_recipients)
        recipients = api.get_recipients_with_collector_and_message()
        if len(recipients) > 0:
            for data in recipients:
                try:
                    model_id = next((d['extra_fields']['id'] for d in emails if data['email'] == d['email']))
                    Answers.insert(pecuarista_id=model_id, id_response=data['id']).execute()
                except StopIteration:
                    logging.error('nao foi possivel identificar o model_id com o data {} emails {}'.format(data, emails))

if len(emails_list) > 0:
    Collector.insert({
        Collector.collector_id: api.collector_id,
        Collector.collector_name: api.collector_name,
        Collector.date: today,
    }).execute()
    logging.info('salvando collector_id na tabela')
