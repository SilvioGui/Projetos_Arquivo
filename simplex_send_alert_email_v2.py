import emails
from lib.Email import Email
from lib.Boto import Boto
from emails.template import JinjaTemplate as T
import random
import time
from datetime import datetime
import re
import base64

if subject == sending_keys[len(sending_keys)-1]:
    chosen_grettings, chosen_introduction, chosen_ending, chosen_goodbye = get_random_texts(name_greetings, email_issues)
    email_greetings = chosen_grettings+'<br>'+chosen_introduction+'<br><br>'
    email_ending = '<br><br>'+chosen_ending+'<br>'+chosen_goodbye+'<br>'
    emailtext = email_greetings + emailtext + email_ending
    chatbot_phrases = True

configEmail = auth.config['email']
fromEmail = configEmail['from']
fromName = configEmail['name']
to = toaddr

boto = Boto()
bucket = auth.config['do']['bucket']
dir = os.path.dirname(os.path.realpath(__file__))

# adaptando para pegar todos src existentes e converter em links enviando a imagem para o DO Spaces
if 'src="cid:' in emailtext:
    match = re.finditer('src="cid\:(Graph.*?.png)"', emailtext)
    logging.info('Replacing images in code with cid for base64...')
    for m in match:
        file = m[1]
        fullFile = '{}/{}'.format(dir, file)
        if configEmail['dev']['enable']:
            with open(fullFile, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            logging.info('Encoding image {}'.format(file))
            emailtext = emailtext.replace('cid:{}'.format(file), 'data:image/png;base64,{}'.format(encoded_string.decode("utf-8") ))
        else:
            nameSpace = 'cerebro/{}/{}_{}'.format('{:%Y/%m/%d}'.format(
                datetime.today()),
                str(random.random())[2:],
                file)
            logging.info('Sending image {} to spaces{}'.format(file, nameSpace))
            boto.upload(fullFile, nameSpace)
            link = 'https://space-files.nyc3.cdn.digitaloceanspaces.com/{}'.format(nameSpace)
            emailtext = emailtext.replace('cid:{}'.format(file), link)

dir = os.path.dirname(os.path.realpath(__file__))
#html code is received from a emailtext variable from the calling script
msg = emails.Message(html=T(open(dir + '/templates/mensagem_padrao.html').read()),
                  subject=subject,
                  mail_from=(fromName, fromEmail))

msg.render(mensagem=emailtext)
sent_date = datetime.now()
# caso esteja em ambiente de desenvolvimento o email sera enviado para o mailhog
if configEmail['dev']['enable']:
    msg.set_cc(cc)
    msg.set_bcc(bcc)
    response = msg.send(to=to, smtp={'host': configEmail['dev']['host'], 'timeout':60, 'port': configEmail['dev']['port']})
    logging.info('Email response status: {}'.format(response.status_code))

    #alerts database update
    email_details = sending_dict[subject]['alert']
    if email_details[0] != '' and 'force_receiver' not in sys.argv:
        cursor.execute("INSERT INTO email_alerts_history (id, sent_date, url_ids_dates_analyzed, subject, content, email_group, receiver, cc, bcc, html_email) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                       (email_details[1], sent_date, email_details[2], subject, email_details[3], email_group_id, toaddr, cc, bcc, msg.html_body))
        logging.info("email_alerts_history was updated")
    #reports database update
    email_details = sending_dict[subject]['report']
    if email_details[0] != '' and 'force_receiver' not in sys.argv:
        cursor.execute("INSERT INTO email_reports_history (id, sent_date, url_ids_dates_analyzed, subject, content, email_group, receiver, cc, bcc, html_email) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                       (email_details[1], sent_date, email_details[2], subject, email_details[3], email_group_id, toaddr, cc, bcc, msg.html_body))
        logging.info("email_reports_history was updated")
    db.commit()

else:
    e = Email()
    toDict = {}
    [toDict.update({d: ''}) for d in to.split(',')]
    ccDict = {}
    bccDict = {}
    if isinstance(cc, str):
        [ccDict.update({d: ''}) for d in cc.split(',')]
    if isinstance(bcc, str):
        [bccDict.update({d: ''}) for d in bcc.split(',')]
    e.send(toDict, subject, msg.html_body, cc=ccDict, bcc=bccDict)
    if 'code' in e.result and e.result['code'] == 'success':
        idEmail = e.result['data']['message-id']

        #alerts database update
        email_details = sending_dict[subject]['alert']
        if email_details[0] != '' and 'force_receiver' not in sys.argv:
            cursor.execute("INSERT INTO email_alerts_history (id, sent_date, url_ids_dates_analyzed, subject, content, email_group, receiver, cc, bcc, html_email) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                       (email_details[1], sent_date, email_details[2], subject, email_details[3], email_group_id, toaddr, cc, bcc, msg.html_body))
            logging.info("email_alerts_history was updated")
        #reports database update
        email_details = sending_dict[subject]['report']
        if email_details[0] != '' and 'force_receiver' not in sys.argv:
            cursor.execute("INSERT INTO email_reports_history (id, sent_date, url_ids_dates_analyzed, subject, content, email_group, receiver, cc, bcc, html_email) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                       (email_details[1], sent_date, email_details[2], subject, email_details[3], email_group_id, toaddr, cc, bcc, msg.html_body))
            logging.info("email_reports_history was updated")
        db.commit()
    else:
        logging.error('nao foi possivel enviar o email', e.result)

