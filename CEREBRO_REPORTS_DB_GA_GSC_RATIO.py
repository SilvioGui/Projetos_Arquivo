#imports all the libraries from calling script
from __main__ import *

# Determines Time and Day Running
date = datetime.now().date()
weekday = str(date.today().weekday())

dict_colunas = { 
    #first subdivision
    'semantic':{'en':
                    {'ga_gsc_ratio':'SEO Ratio GSC/GA',
                    },
                'pt':
                    {'ga_gsc_ratio':'Razão SEO GSC/GA',
                    }
                },
    #second subdivision
    'format':
            {'ga_gsc_ratio':float,
            },
    }

dict_texts = {'text1':{
                        'en':'<br>There is still not enough information to follow on <a href="%s">%s</a>',
                        'pt':'<br>Ainda não há dados suficientes para acompanhar em <a href="%s">%s</a>',
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
table_name, script_type = 'ga_gsc_seo_ratio', 'reports'
reports = email_to_send['gsc']
if reports == None:
    raise RuntimeError('Report not enabled')
file_emailtext = ''
time_step = 1 

report_dict = yaml.load(reports)

for report in report_dict.keys():
    graph_title = report
    metrics = report_dict[report]['metrics']
    if metrics[0] != 'ga_gsc_ratio' or len(metrics) > 1:
        continue
    report_interval = int(report_dict[report]['period'])
    url_ids = report_dict[report]['urls']
    statistics = report_dict[report]['stats']

    url_ids = list(set(url_ids) & set(allowed_url_ids))
    if url_ids == []:
        continue
    url_id = url_ids[0]

    if url_id not in reports_summary:
        reports_summary[url_id] = []

    cursor.execute('select max(date) from ga_gsc_seo_ratio where url_id = %s;' , [url_id])
    end_date = cursor.fetchall()
    if end_date[0]['max(date)'] == None:
        logging.info('There is still not enough information to follow url_id: %s...' %url_id)
        continue
    end_date = end_date[0]['max(date)']
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

    #Graph with 1 metrics. It can use various dimensions
    if len(metrics) == 1:
        metric = metrics[0]
        format_type = dict_colunas['format'][metric]
        siteurls = []
        report_values = []

        cursor.execute('select * from ga_gsc_seo_ratio where url_id = %s and date > %s order by date asc;' , (url_id, start_date))
        results = cursor.fetchall()
        if results == ():
            logging.info('There isn\'t any information to follow on url id: %s' %(url_id))
            continue

        siteurl = results[0]['url']
        if len(results) < 5:
            file_emailtext += dict_texts['text1'][language] %(siteurl, siteurl)
            logging.info('There is still not enough information to follow on %s' %(siteurl))
            continue

        available_dates = []
        for result in results:
            available_dates.append(str(result['date']))
        not_available_dates = [x for x in dates if x not in available_dates]

        date_i = 0
        for date in dates:
            if date in not_available_dates:
                report_values.append(None)
            else:
                result_dimension = format_type(results[date_i][metric])
                report_values.append(result_dimension)
                date_i += 1

        if 'smooth' in statistics and 'avg' in statistics:
            logging.info("It's not possible to apply exponencial smoothing and moving average simultaneously")
        elif 'smooth' in statistics and 'avg' not in statistics:
            correct_values = report_values
            smooth_curve = smooth_list(correct_values, float(statistics['smooth']))
            report_values = smooth_curve
        elif 'avg' in statistics and 'smooth' not in statistics:
            correct_values = report_values
            avg_curve = moving_average(correct_values, int(statistics['avg']))
            report_values = avg_curve
                                    
        dict_urls[url_id] = str(date1)
        analyzed_urls[execute_file[2]] = dict_urls
        reports_summary[url_id].append(metrics)

        siteurls = [siteurl]
        if report_values != []:
            plot_n_curves(list(range(0,len(dates))), [report_values], x_label_dates, n, siteurls)
            file_emailtext += '<img src="cid:Graph%s.png"><br>' %n
            n += 1

#------------ AFTER TESTS ARE MADE, CHECKS IF IT IS NECESSARY TO SEND EMAIL ---------------
if file_emailtext != '':
    title = title_to_email_section('Google Search Console and Google Analytics SEO Ratio','report')
    file_emailtext = title + file_emailtext
else:
    file_emailtext = ''
    logging.info("No data sent to %s on email group %s" %(toaddr, email_group_id))
