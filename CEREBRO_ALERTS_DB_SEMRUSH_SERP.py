#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(datetime.today().weekday())

#function to create png images with graphics
def volatility_graph(maxdate, device, variable, x, y, dates, n):
    analysisperiod = 'the last %s days' %len(dates)
    graph_title = get_graph_values(domain, variable, '', dates, analysis, weekday, 'outlier')

    font1 = FontProperties()
    font1.set_family('arial')
    font1.set_size(15)
    font1.set_weight('bold')        

    #creates constant arrays with the integers below
    y0 = []
    y1 = []
    y2 = []
    y3 = []
    for number in x:
        y0.append(2)
        y1.append(5)
        y2.append(8)
        y3.append(10)

    fig = plt.figure(figsize=(len(x)-0.5, 4))
    plt.rcParams['axes.facecolor'] = 'w'

    ax = fig.add_subplot(111)
    #fills the curves determined between the function (constant functions). Alpha is used for transparency
    ax.fill_between(x, 0, y0, color ="deepskyblue", alpha=0.5)
    ax.fill_between(x, y0, y1, color ="lime", alpha=0.5)
    ax.fill_between(x, y1, y2, color ="orange", alpha=0.5)    
    ax.fill_between(x, y2, y3, color ="red", alpha=0.5)    

    #adds legend to the graph
    low_patch = mpatches.Patch(color='deepskyblue', label='Low')
    medium_patch = mpatches.Patch(color='lime', label='Medium')
    high_patch = mpatches.Patch(color='orange', label='High')
    veryhigh_patch = mpatches.Patch(color='red', label='Very High')
    #plots the legend. loc defines where it appears
    plt.legend(handles=[low_patch,medium_patch,high_patch,veryhigh_patch], loc=3)

    #removes white margins from graphs
    plt.autoscale()
    plt.margins(0, 0)

    plt.xticks(range(len(x)), dates, rotation = 20)    #enables ploting float vs string
    #graph information
    plt.title(graph_title[0] , color = 'black' , fontproperties = font1)
    ax.set_ylabel('SERP Volatility Score', fontproperties = font1)
    
    #plots the points in black as circles
    plt.plot(x, y, linestyle='--', marker = 'o', color = 'black')

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight')
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

# -------------------------- SEMRUSH DATA --------------------------------
dict_texts = {'en':
                  {'text1':'<br><span style="font-size:15px"><b>SEMRush SERP volatility is facing high oscilations</b></span><br>',
                   'text2':'<br><b>%s %s</b> is showing a %s volability score',
                   'text3':'<br><span style="font-size:15px"><b>Some categories SERP show anormal values for HTTPS occurence</b></span><br>',
                   'text4':'<br><span style="font-size:15px"><b>Some categories SERP are in a changing trend regarding HTTPS occurences </b></span><br>',
                   },
              'pt':
                  {'text1':'<br><span style="font-size:15px"><b>A volatilidade da SERP está passando por grandes oscilações</b></span><br>',
                   'text2':'<br><b>%s %s</b> está mostrando um score de volatilidade de %s',
                   'text3':'<br><span style="font-size:15px"><b>A SERP de algumas categorias têm mostrado valores anormais para ocorrência de HTTPS</b></span><br>',
                   'text4':'<br><span style="font-size:15px"><b>A SERP de algumas categorias têm mostrado tendência de mudança nos resultados HTTPS</b></span><br>',
                   },
            }

logging.info("Checking if SERP data is covered by %s" %toaddr)
url_id = email_to_send['sem_rush_serp']
table_name, script_type = 'sem_rush_serp', 'alerts'

if str(url_id) != '0':
    raise RuntimeError("SERP data tracking is not enabled for %s" %toaddr)

cursor.execute("select distinct(category) from sem_rush_serp;")
categories = cursor.fetchall()
categorias = []
for categoria in categories:
    categorias.append(categoria['category'])

cursor.execute("select distinct(device) from sem_rush_serp;")
dispositivos = cursor.fetchall()
devices = []
for device in dispositivos:
    devices.append(device['device'])
        
#sets all the columns to compare data
colunas = ['All categories', 'Shopping']
format_type = float
domain = ''
color = 'blue'
traffic_type = ''
analysis = 'days'
file_emailtext = ''

if 0 not in alerts_summary:
    alerts_summary[0] = []

cursor.execute('select max(date) from sem_rush_serp;')
maxdate = cursor.fetchall()[0]['max(date)'].strftime("%Y-%m-%d")

#since this script doenst use a loop. It's necessary to use an extra variable in order not to send duplicate alerts
skip = False
# ------------------------------- AVOIDING DUPLICATE ALERTS --------------------------------
cursor.execute("select sem_rush_serp from alerts_analysis_history where url_id = '%s';" %url_id)
last_alert_date = cursor.fetchall()
if last_alert_date != ():
    last_alert_date = last_alert_date[0]['sem_rush_serp']         #gets the last date from the alerts sent in past
    if last_alert_date != None:
        last_alert_date = yaml.load(last_alert_date)        #if there is no alert, moves on, if there is it turns the string stored into a dictionary
        try:                                                #tries to access the last date for the current email by dictionary key, if doesnt exist, moves on
            email_alert_id = last_alert_date[email_group_id].split('|')[0]
            last_analyzed_date = last_alert_date[email_group_id].split('|')[1]
            if last_analyzed_date == str(maxdate):            #in case there is a last date for the current email, checks if it is the same as the date being analyzed
                cursor.execute("select sent_date from email_alerts_history where id = '%s';" %email_alert_id)
                sent_date = cursor.fetchall()
                if sent_date != ():
                    sent_date = sent_date[0]['sent_date']
                    logging.info("There is already an email alert sent to %s about SEM Rush SERP data collected in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, maxdate, sent_date))                    
                    skip = True
                else:
                    logging.info("There is already an email alert sent to %s about SEM Rush SERP data collected in %s. \
A new alert on the same issue won't be sent." %(toaddr, maxdate))                    
                    skip = True
        except:
            pass

if skip == True:
    logging.info("There is already an email alert sent to %s about SEM RUSH SERP data collected in %s. \
This email was sent at %s. A new alert on the same issue won't be sent." %(toaddr, last_analyzed_date, sent_date))
    raise RuntimeError

# ------------------------------- AVOIDING REPETITIVE ALERTS ---------------------
# gets the last email types sent by subject and compares what is found now with the older findings, non critical findings won't be send in an interval of 3 days
cursor.execute('select sent_date,content from email_alerts_history where subject like %s and receiver = %s and sent_date > %s order by id desc;', ("%{}%".format(subject_like), toaddr, email_check_date))
last_emails_content = cursor.fetchall()

#SERP analysis
serptext = ''
logging.info("Analyzing %s SERP" %maxdate)
for categoria in categorias:
    if categoria in colunas:
        for device in devices:
            cursor.execute("select * from sem_rush_serp where (category,device) = (%s,%s) order by date desc limit 0,10;", (categoria,device))
            results = cursor.fetchall()
            date1 = results[0]['date']
            volatility = []
            x = []
            dates = []
            i = 0
            volatility1 = format_type(results[0]['volatility'])
            if volatility1 > 8:
                type_alert = 'volatility'
                logging.info("High volability SERP in %s for %s %s" %(maxdate, device, categoria))
                for result in results:
                    volatility[:0] = [format_type(result['volatility'])]
                    dates[:0] = [str(result['date'])]
                    x.append(i)
                    i += 1
                    if serptext == '':
                        serptext += dict_texts[language]['text1']
                serptext += dict_texts[language]['text2'] %(device.title(), categoria.title(), volatility1)
                serptext +='<br><img src="cid:Graph%s.png"><br>' %n
                volatility_graph(maxdate, device, categoria, x, volatility, dates, n)
                n += 1
                if type_alert not in alerts_summary[url_id]:
                    alerts_summary[url_id].append(type_alert)

#HTTPS analysis
httpstext = ''
outtext = ''

for categoria in categorias:
    if categoria in colunas:
        for device in devices:
            cursor.execute("select * from sem_rush_serp where (category,device) = (%s,%s) order by date desc limit 0,10;", (categoria,device))
            results = cursor.fetchall()
            https = []
            x = []
            dates = []
            i = 0
            for result in results:
                https[:0] = [format_type(result['https'])]
                dates[:0] = [str(result['date'])]
                x.append(i)
                i += 1
            https1 = format_type(results[0]['https'])
            try:
                trim_https, upperlimit, lowerlimit, x = get_stats_values(https, 1.75, format_type)
                if len(var) >= 5:
                    x, vect_reg, r_value, slope, p_value, trend_result, trend_type = best_curve_fit(https, 'all')             
            except:
                continue

            #Trend detection
            if r_value >= 0.9 and p_value < 0.05:
                type_alert = 'https trend'
                if slope < 0:
                    trend_type = 'falling'
                else:
                    trend_type = 'rising'                
                logging.info("Trend found: %s" %type_alert)

                # -------------- EMAIL CONSTRUCTING BLOCK (TRENDS) --------------
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    if httpstext == '':
                        httpstext += dict_texts[language]['text4']
                    httpstext += trend_phrase(device.title(), 'HTTPS ' + categoria , type_alert, color, trend_type, format_type)
                    #httpstext += '<span style="font-size:12px;color:blue"> <i>' + ("  -  ").join(str(i) for i in https) + "</i></span>"
                    httpstext += '<br><img src="cid:Graph%s.png"><br>' %n
                    trend_graph(maxdate, 'HTTPS', categoria, x, https, dates, vect_reg, r_value, color, analysis, n)
                    n += 1
                    if type_alert not in alerts_summary[url_id]:
                        alerts_summary[url_id].append(type_alert)

            #Outlier detection
            httpsabsdelta = https1 - trim_https
            try:
                httpspercdelta = (https1/trim_https)-1
            except:
                httpspercdelta = float("inf")

            if https1 < lowerlimit or https1 > upperlimit:
                type_alert = 'https outlier'
                if httpsabsdelta < 0:
                    type_alert += ' up'
                else:
                    type_alert += ' down'
                logging.info("Outlier found: %s" %type_alert)

                # -------------- EMAIL CONSTRUCTING BLOCK (TRENDS) --------------
                var_email = avoid_same_content(last_emails_content, type_alert)
                if var_email == True:
                    if outtext == '':
                        outtext = dict_texts[language]['text3']
                    if httpsabsdelta < 0:
                       sign = '-'
                    else:
                       sign = '+'
                    outtext += outlier_phrase(device.title(), type_alert, 'HTTPS '+ categoria, https1, date1, color, abs(httpspercdelta), trim_https, sign, format_type, 'dimension_on','yes')                
                    if type_alert not in alerts_summary[url_id]:
                        alerts_summary[url_id].append(type_alert)

#email sending part
if serptext != '' or outtext != '' or httpstext != '':
    dict_urls[url_id] = str(date1)
    analyzed_urls[execute_file[2]] = dict_urls 

    file_emailtext = serptext + '<br>' + httpstext + '<br>' + outtext + '<br>'
    title = title_to_email_section('SEM Rush SERP','unusual')
    file_emailtext = title + file_emailtext
else:
    logging.info("No data sent to email")
