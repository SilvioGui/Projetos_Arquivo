from datetime import datetime, timedelta
import sys
from app.survey import Api
import logging
from app.config import config
from app.model import Collector, Pecuaristas, Answers
from app.jbs import JBSNotificacao

dict_resps = {
    'Péssimo': 1,
    'Ruim': 2,
    'Bom': 3,
    'Muito Bom': 4,
    'Excelente': 5,
    '': None,
    None: None,
}
def get_in_dict(p):
    return dict_resps[p] if p in dict_resps else p

def get_resposta_numero(x, y):
    return get_in_dict(y[x]) if x in y else None

key = config['survey_monkey_key']
api = Api(key)
jbs_notification = JBSNotificacao()


try:
    collector_all = Collector.select().where(Collector.date >= datetime.now() - timedelta(days=60)) #.where(Collector.date >= '2018-07-27')
except Collector.DoesNotExist as e:
    logging.info('nao existem registros para processar')
    sys.exit()


for c in collector_all:
    if c.collector_id == 0:
        logging.error('isso não é legal, collector_id esta zerado id na tabela {}'.format(c.id))
        continue

    logging.info('consultando respostas collector_id {} referente a data {}'.format(c.collector_id, c.date))
    api.collector_id = c.collector_id
    responses = api.get_responses_with_collector()
    recipients = api.collector_recipients()
    for r in recipients:
        answers = Answers()
        try:
            answers = Answers.get(Answers.id_response == r['id'])
        except Answers.DoesNotExist:
            try:
                # nao foi registrado na tabela, então preciso pegar por data e e-mail, esses são os antigos
                pecuarista_model = Pecuaristas.get(Pecuaristas.email.contains(r['email']), Pecuaristas.data_ultimo_abate == c.date - timedelta(days=1))
                answers.pecuarista_id = pecuarista_model.id
                answers.id_response = r['id']
            except Pecuaristas.DoesNotExist:
                logging.error('id_response: {} nao existe na tabela answers e nao foi possivel identificar o pecuarista pelo e-mail e data de abate {} {}'
                              .format(r['id'], r['email'], (c.date - timedelta(days=1)).strftime('%d/%m/%Y')))
                continue

        answers.survey_response_status = r['survey_response_status']
        answers.mail_status = r['mail_status']

        try:
            survey = next((item for item in responses if item['recipient_id'] == r['id']))
            respostas_dict = api.get_answers(survey)
            answers.date_created = datetime.strptime(survey['date_created'][:-6], '%Y-%m-%dT%H:%M:%S') if survey['date_created'] else None
            answers.date_modified = datetime.strptime(survey['date_modified'][:-6], '%Y-%m-%dT%H:%M:%S') if survey['date_modified'] else None
            answers.resposta_1 = get_resposta_numero('r_1', respostas_dict)
            answers.resposta_2 = get_resposta_numero('r_2', respostas_dict)
            answers.resposta_3 = get_resposta_numero('r_3', respostas_dict)
            answers.comentario_1 = get_resposta_numero('c_1', respostas_dict)
            answers.comentario_2 = get_resposta_numero('c_2', respostas_dict)
            answers.comentario_3 = get_resposta_numero('c_3', respostas_dict)
            answers.total_time = survey['total_time']

            if len(list(filter(lambda x: x in [1, 2], [answers.resposta_1, answers.resposta_2, answers.resposta_3]))) > 0:
                jbs_notification.add_notification(answers.pecuarista_id, jbs_notification.TIPO_PROPOSITO_AVALIACAO)

        except StopIteration:
            logging.debug('nenhuma resposta email_status {} survey_response_status: {} para response_id {}'.format(r['mail_status'], r['survey_response_status'], r['id']))

        try:
            answers.save()
        except Exception as e:
            logging.exception(e)

