import requests
from datetime import datetime
import re
from app.model import Collector
from app.config import config


key = config['survey_monkey_key']

data = requests.get('https://api.surveymonkey.com/v3/surveys/151068121/collectors?per_page=200', headers={'Authorization': 'bearer {}'.format(key)}).json()
print('request: ',data)

for d in data['data']:
    if 'feedback_' in d['name']:
        date_string = re.findall('feedback_(\d+)_', d['name'])[0]
        da = datetime.strptime(date_string, '%Y%m%d')
        #print(d['name'], d['id'], da.strftime('%y-%m-%d'))
        print(da)
        try:
            id = Collector.select().where(Collector.collector_id == d['id']).get()
        except Exception:
            print('nao existe')
            Collector.insert(collector_id=d['id'], collector_name=d['name'], date=da).execute()
