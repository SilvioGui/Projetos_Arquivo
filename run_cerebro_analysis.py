#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Importing Libraries for All Scripts Called
from datetime import datetime, timedelta
import time
import pytz
import sys, os
import difflib
import html
import ast
import yaml, json
import numpy
import scipy
import math
from scipy import stats
from scipy.interpolate import spline, interp1d
import subprocess
import MySQLdb
import warnings
from warnings import filterwarnings
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from lib import auth, logger, models
import logging
import urllib
from urllib.parse import urlparse
import textwrap
from regressions import *
import random
import matplotlib, logging
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches
from matplotlib.ticker import MultipleLocator

exec(open('cerebro_chat_options.py', encoding='utf-8').read())

# Determines Time and Day Running
date = datetime.now().date()
email_check_date = datetime.now().date()- timedelta(days=4)
weekday = str(datetime.today().weekday())
logging.info("\n\n ++++++++++++++++++++++++++++++++++++++ Running %s on %s +++++++++++++++++++++++++++++++++++++++++ " %(str(os.path.basename(__file__)), date))

# Ignores the Warnings Showed by MySQL and Python
filterwarnings('ignore', category = MySQLdb.Warning)
warnings.filterwarnings("ignore")
    
# Sets Database Credentials
db = auth.getConnection()
cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("set time_zone = 'America/Sao_Paulo';")

dict_weekdays = {
    '0':'Mondays',
    '1':'Tuesdays',
    '2':'Wednesdays',
    '3':'Thursdays',
    '4':'Fridays',
    '5':'Saturdays',
    '6':'Sundays'
}

def get_set_tz_email(email_group_id):
    cursor.execute("select timezone_id from email_groups where id = %s;" %email_group_id)
    timezone_id = cursor.fetchall()[0]['timezone_id']
    cursor.execute("select timezone from timezones where id = %s;" %timezone_id)
    timezone = cursor.fetchall()[0]['timezone']
    cursor.execute("set time_zone = '%s';" %timezone)
    return timezone

def get_semantic_dimention(type_alert):
    dimension_condition = 'dimension_on'
    if type(type_alert[1]) == list:
        try:
            semantic_var = dict_types[language][type_alert[1][1]] + ' ' + type_alert[1][0]
        except:
            semantic_var = type_alert[1][1] + ' ' + type_alert[1][0]
    elif type(type_alert[1]) == str:
        try:
            semantic_var = dict_types[language][type_alert[1]]
        except:
            semantic_var = type_alert[1]

    if semantic_var == 'Overall All Devices':
        semantic_var = ''
    elif 'All Devices' in semantic_var:
        semantic_var = semantic_var.replace(' All Devices','')
        semantic_var = semantic_var.replace('All Devices ','')

    elif 'Overall' in semantic_var:
        semantic_var = semantic_var.replace('Overall ','')
        semantic_var = semantic_var.replace(' Overall','')

    if semantic_var == ' ':
        semantic_var = ''

    if semantic_var == '':
        dimension_condition = 'dimension_off'

    return semantic_var, dimension_condition


def extreme_value_graph(weekday, variable, var_type, x, y, dates, limit_value, direction_limit, analysis, n):
    graph_title, expected_value, upper_limit, lower_limit = get_graph_values(domain, variable, var_type, dates, analysis, weekday, 'outlier')
        
    font1 = FontProperties()
    font1.set_family('verdana')
    font1.set_size(12)
    font1.set_weight('bold')        

    plt.figure(figsize=(len(x)-0.5, 3))
    plt.rcParams['axes.facecolor'] = 'w'

    plt.xticks(range(len(x)), dates, rotation = 20)    #enables ploting float vs string
    #graph information
    plt.title(graph_title , color = 'navy' , fontproperties = font1)
    plt.axhline(y = limit_value, color = 'red', linewidth = 2,linestyle='-') #lower limit
        
    #plots the points in black as diamonds
    outliers_over_time = []
    i = 0
    for number in y:
        if direction_limit == 'high-value' and number > limit_value:
            outliers_over_time.append(1)
            plt.plot(i, number, 'H', color = 'red')
        elif direction_limit == 'low-value' and number < limit_value:
            outliers_over_time.append(-1)
            plt.plot(i, number, 'H', color = 'red')
        else:
            plt.plot(i, number, 'h', color = 'green')
            outliers_over_time.append(0)
        i += 1
    
    #formats the axis to display big numbers with coma separating every 3 values. This also excludes scientific notation use 
    ax = plt.subplot()
    if format_type == float:
        ax.set_yticklabels(['{:0,.2f}'.format(float(x)) for x in ax.get_yticks().tolist()])
    elif format_type == int:
        ax.set_yticklabels(['{:0,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

    return outliers_over_time

#function to create png images with graphics
def outlier_graph(weekday, variable, var_type, x, y, dates, trim, up, down, analysis, n):
    graph_title, expected_value, upper_limit, lower_limit = get_graph_values(domain, variable, var_type, dates, analysis, weekday, 'outlier')
        
    font0 = FontProperties()
    font0.set_family('verdana')
    font0.set_size(10)
    font0.set_style('italic')        
    font0.set_weight('bold')        
    
    font1 = FontProperties()
    font1.set_family('verdana')
    font1.set_size(12)
    font1.set_weight('bold')        

    plt.figure(figsize=(len(x)-0.5, 3))
    plt.rcParams['axes.facecolor'] = 'w'

    plt.xticks(range(len(x)), dates, rotation = 20)    #enables ploting float vs string
    #graph information
    if type_alert[3] == False:
        plt.title(graph_title , color = 'black' , fontproperties = font1)
    else:
        plt.title(graph_title , color = 'red' , fontproperties = font1)

    y_varriations = []
    for value in y:
        try:
            y_varriation = (value/trim_var)-1
        except:
            y_varriation = float("inf")
        y_varriations.append(abs(y_varriation))        
    if down/up > 0.975 or max(y_varriations) > 5 or down == up:
    #Text in graph
        plt.annotate(expected_value, color = 'gray', xy = ((len(x))/3, trim), fontproperties = font0)
        plt.axhline(y = trim, color = 'black', linewidth = 2, linestyle='--') #trimean
    else:
        plt.axhline(y = trim, color = 'gray', linewidth = 2, linestyle='--') #trimean
        plt.axhline(y = up, color = 'black', linewidth = 2,linestyle='-.') #upper limit
        plt.axhline(y = down, color = 'black', linewidth = 2,linestyle='-.') #lower limit
        plt.annotate(expected_value, color = 'gray', xy = ((len(x))/3, trim+(up-trim)/10), fontproperties = font0)
        plt.annotate(upper_limit, color = 'black', xy = ((len(x))/3, up-((up-trim)/10)), fontproperties=font0)
        plt.annotate(lower_limit, color = 'black', xy = ((len(x))/3, down+((trim-down)/10)), fontproperties=font0)

    #plots the points in black as diamonds
    outliers_over_time = []
    i = 0
    for number in y:
        if number > up:
            outliers_over_time.append(1)
            plt.plot(i, number, 'H', color = 'red')
        elif number < down:
            outliers_over_time.append(-1)
            plt.plot(i, number, 'H', color = 'red')
        else:
            plt.plot(i, number, 'h', color = 'green')
            outliers_over_time.append(0)
        i += 1
    
    #formats the axis to display big numbers with coma separating every 3 values. This also excludes scientific notation use 
    ax = plt.subplot()
    if format_type == float:
        ax.set_yticklabels(['{:0,.2f}'.format(float(x)) for x in ax.get_yticks().tolist()])
    elif format_type == int:
        ax.set_yticklabels(['{:0,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

    return outliers_over_time

#function to plot graph from data trends
def trend_graph(weekday, variable, var_type, x, y, dates, trend_line, r, linecolor, analysis, n):
    graph_title = get_graph_values(domain, variable, var_type, dates, analysis, weekday, 'trend')

    font0 = FontProperties()
    font0.set_family('verdana')
    font0.set_size(12)
    font0.set_weight('bold')        

    plt.figure(figsize=(len(x)-0.5, 3))
    plt.rcParams['axes.facecolor'] = 'w'

    plt.xticks(range(len(x)), dates, rotation = 20)    #enables ploting float vs string
    #graph information
    plt.title(graph_title , color = 'black' , fontproperties = font0)
    plt.annotate('R² = %s' %round(r,3), color = 'black', style = 'italic', xy = (max(x)*0.4, min(trend_line)+(max(trend_line)-min(trend_line))*0.4))

    #plots the points in black as diamonds
    plt.plot(x,y,'h', color = linecolor)
    plt.plot(trend_line, color = linecolor, linestyle='-.')

    #formats the axis to display big numbers with coma separating every 3 values. This also excludes scientific notation use 
    ax = plt.subplot()
    if format_type == float:
        ax.set_yticklabels(['{:0,.2f}'.format(float(x)) for x in ax.get_yticks().tolist()])
    elif format_type == int:
        ax.set_yticklabels(['{:0,}'.format(int(x)) for x in ax.get_yticks().tolist()])

    #save image as png and cuts off the white margins on the sides to otimize the view to the content
    plt.savefig("Graph%s.png" %n, bbox_inches='tight', transparent=True)
    plt.clf()   #clear the plot so the next image produced won't overwrite the previous one

#updates alerts_analysis_history and reports_analysis_history with information used on emails
def email_database_update(table_name, table_type, max_id, dict_urls, date1):
    id_date = str(max_id)+'|' +str(date1)

    for url_id in dict_urls.keys():
        cursor.execute("select * from %s_analysis_history where url_id = %s;" %(table_type ,url_id))
        finding_dict = cursor.fetchall()[0][table_name]
        if finding_dict == None:
            finding_dict = {}
        else:
            finding_dict = yaml.load(finding_dict)
        finding_dict[email_group_id] = id_date
        if 'force_receiver' not in sys.argv:
            cursor.execute("update {}_analysis_history set {} = %s where url_id = %s;".format(table_type, table_name), (yaml.dump(finding_dict), url_id))
            logging.info("%s_analysis_history was updated for url_id %s" %(table_type, url_id))

def avoid_same_content(last_emails_content, type_alert):
    #anything considered critical will be sent to email
    var_email = False
    if type_alert[3] == True:
        url_email = True
        var_email = True
    #if it is not critical, the last emails content will be checked. It the alert was not pointed in the last 3 days, and email will be sent
    else:
        new_content = True
        for last_email_content in last_emails_content:
            try:
                sent_date = last_email_content['sent_date']
                content = yaml.load(last_email_content['content'])[url_id]
            except:
                logging.info("%s url id (%s) was not found in the email sent on %s " %(siteurl, url_id, sent_date))
                continue
            if type_alert in content:
                new_content = False
                logging.info("There is a recent email sent on %s to %s concerning the same issue (%s). A new alert won't be sent now" %(sent_date, toaddr, type_alert))
                break
        if new_content == True:
            var_email = True
    return var_email

#get url_ids (simple code used in all scripts)
def get_url_ids(table_name, semantic_table_name, get_type):
    if get_type == str:
        try:
            url_ids = email_to_send[table_name].split(',')
            logging.info("Checking urls data covered by %s on %s" %(email_group['receivers'], email_group['client_name']))
            return url_ids
        except:
            raise RuntimeError("No %s data tracking is enabled for %s" %(email_group['receivers'], semantic_table_name))
    elif get_type == dict:
        try:
            url_ids = yaml.load(email_to_send[table_name]).keys()
            logging.info("Checking urls data covered by %s on %s" %(email_group['receivers'], email_group['client_name']))
            return url_ids
        except:
            raise RuntimeError("No %s data tracking is enabled for %s" %(email_group['receivers'], semantic_table_name))

#gets domain name from siteurl
def get_domain_name(url):
    if 'sc-domain:' in url:
        domain = str(url.split(':')[1].split('.')[0].title())
    else:
        try:
            domain = str(urlparse(url).netloc).split('.')[1].title()
        except:
            domain = str(url.split('.')[1].title())       
        if domain in ['Com','Net','Org']:
            domain = str(urlparse(url).netloc).split('.')[0].title()
        #if domain == "Shopping": domain = "Rakuten"
        if 'travaux' in url: domain = 'HomeGenius'        
    return domain

#sorts email content based on 2 lists, 1 with contents and other with indexes
def sort_email_from_list(email_prior_pieces, email_pieces, *args):
    #sorts pieces from strongest to weakest
    email_sorted_pieces = sorted(email_prior_pieces)
    email_prior_pieces = numpy.array(email_prior_pieces)
    sorted_pieces = []
    index_numbers = []
    for number, line in enumerate(email_prior_pieces):
        index_number = numpy.where(email_prior_pieces == email_sorted_pieces[number])[0]
        for occurence in index_number:
            if occurence not in index_numbers:
               index_numbers.append(occurence)

    #in case the optional arguments are provided (strings to subsections), there is a loop for each of them, inserting the values in the ordered list
    if len(args) > 0:
        for text_arg in args:
            for index in index_numbers:
                if text_arg in email_pieces[index]:
                    sorted_pieces.append(email_pieces[index])
    #in case there are no optional arguments provided, sorts everything by percentual change value
    else:
        for index in index_numbers:
            sorted_pieces.append(email_pieces[index])

    for piece in email_pieces:
        if piece not in sorted_pieces:
            sorted_pieces.append(piece)

    return sorted_pieces

def drop_similar_dim_alerts(url_text, url_prior_changes, type_check, dimension, limit, traffic_types, type_check_dict):
    additional_text = []
    detected_stuff = []
    ext_detected_stuff = []
    criticals = []
    summary_dict = {}
    type_summary_dict = {}
    
    for term in alerts_summary[url_id]:
        if type_check_dict == str:
            if term[1] in traffic_types:
                if type_check == 'outlier':
                    if term[2] not in ['up', 'down']:
                        continue
                elif type_check == 'trends':
                    if term[2] not in ['rising', 'falling']:
                        continue
                detected_stuff.append(term[:-1])
                criticals.append(term[3])
            else:
                if type_check == 'outlier':
                    if term[2] not in ['up', 'down']:
                        continue
                elif type_check == 'trends':
                    if term[2] not in ['rising', 'falling']:
                        continue
                ext_detected_stuff.append(term)
        elif type_check_dict == list:
            if term[1][1] in traffic_types:
                if type_check == 'outlier':
                    if term[2] not in ['up', 'down']:
                        continue
                elif type_check == 'trends':
                    if term[2] not in ['rising', 'falling']:
                        continue
                detected_stuff.append(term[:-1])
                criticals.append(term[3])
            else:
                if type_check == 'outlier':
                    if term[2] not in ['up', 'down']:
                        continue
                elif type_check == 'trends':
                    if term[2] not in ['rising', 'falling']:
                        continue
                ext_detected_stuff.append(term)

    for term in detected_stuff:
        key = term[0] + "-" + term[2]
        if key not in summary_dict:
            summary_dict[key] = []
            type_summary_dict[key] = []
        if type_check_dict == str:
            summary_dict[key].append(term[1])
            type_summary_dict[key].append('string')
        elif type_check_dict == list:
            summary_dict[key].append(term[1][1])
            type_summary_dict[key].append(term[1][0])
            
    joined_alerts = []
    for key1 in summary_dict.keys():
        details = summary_dict[key1]
        for type_details in type_summary_dict[key1]:
            if len(details) >= limit:
                for key2 in details:
                    metric = key1.split('-')[0]
                    direction = key1.split('-')[1]

                    if type_check_dict == str:
                        try:
                            index = detected_stuff.index([metric, key2, direction])
                            type_alert = [metric, details, direction, criticals[index]]
                        except:
                            continue
                                        
                    elif type_check_dict == list:
                        try:
                            index = detected_stuff.index([metric, [type_details, key2], direction])
                            type_alert = [metric, [type_details, details], direction, criticals[index]]
                        except:
                            continue

                    #When joining alerts of any type, if there is distortions is the overall figure, it won't take out the overall from the email
                    if key2 == 'Overall':
                        continue
                    detected_stuff = [x for i,x in enumerate(detected_stuff) if i!=index]
                    url_text = [x for i,x in enumerate(url_text) if i!=index]
                    url_prior_changes = [x for i,x in enumerate(url_prior_changes) if i!=index]
                    criticals = [x for i,x in enumerate(criticals) if i!=index]

                    var_email = avoid_same_content(last_emails_content, type_alert)
                    if var_email == True:
                        #includes the dimensions grouped in a variable that will update alerts_summary
                        if url_id not in auxiliar_alerts_summary[type_check]:
                            auxiliar_alerts_summary[type_check][url_id] = [type_alert]
                            
                        if type_alert not in auxiliar_alerts_summary[type_check][url_id]:
                            if type_alert[3] == True and (type_alert[:-1]+[False]) in auxiliar_alerts_summary[type_check][url_id]:
                                auxiliar_alerts_summary[type_check][url_id].remove(type_alert[:-1]+[False])
                                auxiliar_alerts_summary[type_check][url_id] += [type_alert]
                            elif type_alert[3] == False and (type_alert[:-1]+[True]) in auxiliar_alerts_summary[type_check][url_id]:
                                pass
                            else:
                                auxiliar_alerts_summary[type_check][url_id] += [type_alert]
                        joined_alert = [details, metric]
                        if joined_alert not in joined_alerts:
                            additional_text.append(comment_similar_alerts(dict_colunas['semantic'][language][metric], direction, details, dimension))
                            joined_alerts.append(joined_alert)
                            logging.info("%s detection on %s seems not be connected to %s" %(", ".join(details), metric, dimension))

    for term in detected_stuff:
        index = detected_stuff.index(term)
        term.append(criticals[index])
        
    if additional_text != []:
        additional_text[0] = fill_up_similar_comment(len(additional_text), len(url_text), type_check) + additional_text[0]    

    #joins the new grouped distortion with the other ones (individual ones)
    if url_id not in auxiliar_alerts_summary[type_check]:
        auxiliar_alerts_summary[type_check][url_id] = ext_detected_stuff + detected_stuff
    else:
        auxiliar_alerts_summary[type_check][url_id] += ext_detected_stuff + detected_stuff    

    return url_text, url_prior_changes, additional_text
    #return url_text, url_prior_changes, additional_text, criticals

def consolidate_devices_alerts(url_text, url_prior_changes, type_check):
    detected_stuff = []
    criticals = []
    summary_dict = {}

    for term in alerts_summary[url_id]:
        if type_check == 'outlier':
            if term[2] not in ['up', 'down']:
                continue
        elif type_check == 'trends':
            if term[2] not in ['rising', 'falling']:
                continue
        detected_stuff.append(term[:-1])
        criticals.append(term[3])

    for term in detected_stuff:
        if type(term[1][1]) == str:
            key = term[0] + "-" + term[1][1] + "-" + term[2]
            if key not in summary_dict:
                summary_dict[key] = []
            summary_dict[key].append(term[1][0])

    for key1 in summary_dict.keys():
        details = summary_dict[key1]
        metric = key1.split('-')[0]
        details_dim = key1.split('-')[1]
        direction = key1.split('-')[2]

        remove_values = []
        if len(details) == 1:
            continue
        elif len(details) > 2 and set(details) != set(['Desktop','Mobile','Tablet']):
            remove_values = list(set(details) - set(['All Devices']))
        elif len(details) == 2 and 'All Devices' in details:
            remove_values = ['All Devices']
        elif set(details) == set(['Desktop','Mobile','Tablet']):
            logging.info("Although there were distortions on %s in desktop, mobile and tablet, statiscally it didn\'t affect the all devices scenario" %metric)
            continue
        else:
            continue

        remaining = list(set(details) - set(remove_values))[0]
        critical_situation = False
        for value in remove_values:
            index = detected_stuff.index([metric, [value, details_dim], direction])
                
            detected_stuff = [x for i,x in enumerate(detected_stuff) if i!=index]
            url_text = [x for i,x in enumerate(url_text) if i!=index]
            url_prior_changes = [x for i,x in enumerate(url_prior_changes) if i!=index]

            if criticals[index] == True:
                critical_situation = True
            criticals = [x for i,x in enumerate(criticals) if i!=index]
            logging.info("%s detections on %s %s %s was consolidated on %s, regarding devices" %(value, metric, details_dim, direction, remaining))

        #the consolidating dimension is switched from the consolidated alerts_summary, but it remains on the email
        index_consolidated = detected_stuff.index([metric, [remaining, details_dim], direction])
        type_alert = [metric, [details, details_dim], direction, critical_situation]                  

        detected_stuff[index_consolidated] = type_alert
        criticals[index_consolidated] = critical_situation
                
        var_email = avoid_same_content(last_emails_content, type_alert)
        if var_email == False:
            detected_stuff = [x for i,x in enumerate(detected_stuff) if i!=index_consolidated]
            criticals = [x for i,x in enumerate(criticals) if i!=index_consolidated]
            url_text = [x for i,x in enumerate(url_text) if i!=index_consolidated]
            url_prior_changes = [x for i,x in enumerate(url_prior_changes) if i!=index_consolidated]

    for term in detected_stuff:
        if len(term) == 3:
            index = detected_stuff.index(term)
            term.append(criticals[index])
            
    #joins the new grouped distortion with the other ones (individual ones)
    if url_id not in auxiliar_alerts_summary[type_check]:
        auxiliar_alerts_summary[type_check][url_id] = detected_stuff
    else:
        auxiliar_alerts_summary[type_check][url_id] += detected_stuff

    return url_text, url_prior_changes
    #return url_text, url_prior_changes, criticals

def kpi_connections(metric_details):
    metrics_check = []
    metric_details = alerts_summary[url_id]

    for term in metric_details:
        check_list = False
        if type(term[1]) == list:
            check_list = True
        if check_list == True and type(term[1][0]) == list:    
            continue
            
        else:
            metric = term
            index = metric_details.index(metric)
            check_metrics = [x for i,x in enumerate(metric_details) if i > index]
            for check_metric in check_metrics:

                pivot_metric_dim = metric[1]
                if type(pivot_metric_dim) == list:
                    if pivot_metric_dim[0] in ['Desktop', 'Mobile', 'Tablet', 'All Devices', 'Overall']:
                        pivot_metric = metric[0]
                        pivot_metric_dim = metric[1][1]
                        pivot_metric_dir = metric[2]
                    else:
                        break
                else:
                    pivot_metric = metric[0]
                    pivot_metric_dir = metric[2]

                comparison_metric_dim = check_metric[1]
                if type(comparison_metric_dim) == list:
                    if comparison_metric_dim[0] in ['Desktop', 'Mobile', 'Tablet', 'All Devices', 'Overall']:
                        comparison_metric = check_metric[0]
                        comparison_metric_dim = check_metric[1][1]
                        comparison_metric_dir = check_metric[2]
                    else:
                        continue
                else:
                    comparison_metric = check_metric[0]
                    comparison_metric_dir = check_metric[2]

                if pivot_metric_dir in ['up', 'down'] and comparison_metric_dir in ['up', 'down']:
                    type_check = 'outlier'
                elif pivot_metric_dir in ['rising', 'falling'] and comparison_metric_dir in ['rising', 'falling']:
                    type_check = 'trends'
                else:
                    continue

                metrics_check = set([pivot_metric, comparison_metric, pivot_metric_dir, comparison_metric_dir])  #insert values as tuples so the order of terms doesn't matter
                if metrics_check not in already_commented:
                    if type(pivot_metric_dim) == list or type(comparison_metric_dim) == list:
                        logging.info("The selected KPIs can't be analyzed because one of the dimensions is a list")
                        continue
                    cursor.execute("select * from kpis_correlation where ((metric1, dimension1) = (%s, %s) and (metric2, dimension2) = (%s, %s) or \
                    (metric2, dimension2) = (%s, %s) and (metric1, dimension1) = (%s, %s)) and url_id1 = %s;",\
                    [pivot_metric, pivot_metric_dim, comparison_metric, comparison_metric_dim, pivot_metric, pivot_metric_dim, comparison_metric, comparison_metric_dim, url_id])
                    connections = cursor.fetchall()
                    if connections == ():
                        logging.info("The selected KPIs correlation is not available in the database")
                        continue
                    r_lin = float(connections[0]['r_lin'])
                    r_exp = float(connections[0]['r_exp'])
                    if abs(r_lin - r_exp) <= 0.04:  #if the difference between linear and exponencial is small, consider it linear
                        r_exp = 0

                    if abs(r_lin) >= abs(r_exp): 
                        r_kpis = r_lin
                    else:
                        r_kpis = r_exp
                                
                    if abs(r_kpis) < 0.8: #weak connection between kpis, skips to the next
                        continue
                    if r_kpis > 0:
                        connection_sign = 'same'
                    else:
                        connection_sign = 'opposite'
                    connection_text = associate_findings(pivot_metric_dim, comparison_metric_dim, dict_colunas['semantic'][language][pivot_metric], dict_colunas['semantic'][language][comparison_metric], pivot_metric_dir, comparison_metric_dir, connection_sign)
                    if connection_text != None:
                        metric_comments[type_check].append(connection_text)
                        already_commented.append(metrics_check)


#determines which files will be ran
def get_execute_files(email_configuration, check_scripts):
    if email_configuration == 'group' and check_scripts == 'day':
        #The number of emails sent will be reduced by grouping similar alerts in blocks
        execute_files = {
            # 1st Block: Google Analytics
            'Google Analytics':{
            'files':[#['CEREBRO_ALERTS_DB_GA_GSC_RATIO.py','CEREBRO_REPORTS_DB_GA_GSC_RATIO.py','ga_rat'],
                     ['CEREBRO_ALERTS_DB_GA_CHANNELS.py','CEREBRO_REPORTS_DB_GA_CHANNELS.py','ga_ch'],
                     ['CEREBRO_ALERTS_DB_GA_TEMPLATES.py','CEREBRO_REPORTS_DB_GA_TEMPLATES.py','ga_tp'],
                     ['CEREBRO_ALERTS_DB_GA_BROWSERS.py','CEREBRO_REPORTS_DB_GA_BROWSERS.py','ga_br'],
                     ['CEREBRO_ALERTS_DB_GA_REFERRALS.py','CEREBRO_REPORTS_DB_GA_REFERRALS.py','ga_ref']],
            'subject':'Google Analytics Report'
            },
            'Google Adwords':{
            # 2nd Block: Google Adwords
            'files':[['CEREBRO_ALERTS_DB_GA_CAMPAIGNS.py','skip.py','ga_ads']],
            'subject':'Google Adwords Report',
            },
            # 2nd Block: Google Search Console
            'Google Search Console':{
            'files':[#['CEREBRO_ALERTS_DB_GSC_ERRORS.py','skip.py','gsc_er'],
                     ['CEREBRO_ALERTS_DB_GSC_STATS.py','CEREBRO_REPORTS_DB_GSC_STATS.py','gsc_st'],
                     ['CEREBRO_ALERTS_DB_GSC_KPIS.py','CEREBRO_REPORTS_DB_GSC_KPIS.py','gsc_kpi'],
                     ['CEREBRO_ALERTS_DB_GSC_INDEX.py','CEREBRO_REPORTS_DB_GSC_INDEX.py','gsc_idx']],
            'subject':'Google Search Console Report',
            },
            # 3rd Block: Performance
            'Performance':{
            'files':[['CEREBRO_ALERTS_DB_PAGESPEED.py','skip.py','perf_pg'],
                     ['CEREBRO_ALERTS_DB_PERFORMANCE.py','CEREBRO_REPORTS_DB_PERFORMANCE.py','perf_pf'],
                     ['CEREBRO_ALERTS_DB_LIGHTHOUSE.py','CEREBRO_REPORTS_DB_LIGHTHOUSE.py','perf_lg']],
            #['CEREBRO_ALERTS_DB_YSLOW.py','skip.py','perf_ys'],['CEREBRO_ALERTS_DB_TTFB_NOBJ.py','skip.py','perf_tt'],
            'subject':'Performance Report',
            },
            # 4th Block: SEO Tags
            'SEO Contents':{
            'files':[['CEREBRO_ALERTS_DB_ROBOTS.py','skip.py','seo_rb'],['CEREBRO_ALERTS_DB_SEO_CRAWL.py','skip.py','seo_tag']],
            'subject':'SEO Contents Report',
            },
            # 5th Block: External Sources
            'External Sources':{
            'files':[['CEREBRO_ALERTS_DB_SEMRUSH_SERP.py','skip.py','ext_serp'],
                     ['CEREBRO_ALERTS_DB_SEMRUSH_DASHBOARD.py','CEREBRO_REPORTS_DB_SEMRUSH_DASHBOARD.py','ext_sr'],
                     ['CEREBRO_ALERTS_DB_SEARCH_METRICS.py','CEREBRO_REPORTS_DB_SEARCH_METRICS.py','ext_sm'],
                     ['CEREBRO_ALERTS_DB_ALEXA.py','CEREBRO_REPORTS_DB_ALEXA.py','ext_al']],
            'subject':'External Sources Report',
            },
            # 6th Block: Security
            'Security':{
            'files':[['CEREBRO_ALERTS_DB_OBSERVATORY.py','CEREBRO_REPORTS_DB_OBSERVATORY.py','sec_ob']],
            'subject':'Security Report',
            },
            # 7th Block: Keywords Report
            'Search Keywords':{
            'files':[['','CEREBRO_REPORTS_INTERNAL_SEARCHES.py','key_ie']],
            'subject':'Search Keywords Report',
            },
        }
    elif email_configuration == 'split' and check_scripts == 'day':
        #the emails will all be sent split
        execute_files = {
            #'ga_rat':{'files':[['CEREBRO_ALERTS_DB_GA_GSC_RATIO.py','CEREBRO_REPORTS_DB_GA_GSC_RATIO.py','ga_rat']],'subject':"GA-GSC Ratio Report"},
            'ga_br':{'files':[['CEREBRO_ALERTS_DB_GA_BROWSERS.py','CEREBRO_REPORTS_DB_GA_BROWSERS.py','ga_br']],'subject':"Google Analytics Browsers Report"},
            'ga_tp':{'files':[['CEREBRO_ALERTS_DB_GA_TEMPLATES.py','CEREBRO_REPORTS_DB_GA_TEMPLATES.py','ga_tp']],'subject':"Google Analytics Templates Report"},
            'ga_ch':{'files':[['CEREBRO_ALERTS_DB_GA_CHANNELS.py','CEREBRO_REPORTS_DB_GA_CHANNELS.py','ga_ch']],'subject':"Google Analytics Channels Report"},
            'ga_ad':{'files':[['CEREBRO_ALERTS_DB_GA_CAMPAIGNS.py','skip.py','ga_ch']],'subject':"Google Adwords Report"},
            'ga_ref':{'files':[['CEREBRO_ALERTS_DB_GA_REFERRALS.py','CEREBRO_REPORTS_DB_GA_REFERRALS.py','ga_ref']],'subject':"Google Images Referral Report"},
            'gsc_idx':{'files':[['CEREBRO_ALERTS_DB_GSC_INDEX.py','CEREBRO_REPORTS_DB_GSC_INDEX.py','gsc_idx']],'subject':"Google Search Console Index Report"},
            'gsc_st':{'files':[['CEREBRO_ALERTS_DB_GSC_STATS.py','CEREBRO_REPORTS_DB_GSC_STATS.py','gsc_st']],'subject':"Google Search Console Stats Report"},
            'gsc_kpi':{'files':[['CEREBRO_ALERTS_DB_GSC_KPIS.py','CEREBRO_REPORTS_DB_GSC_KPIS.py','gsc_kpi']],'subject':"Google Search Console KPIs Report"},
            'perf_lg':{'files':[['CEREBRO_ALERTS_DB_LIGHTHOUSE.py','CEREBRO_REPORTS_DB_LIGHTHOUSE.py','perf_lg']],'subject':"Lighthouse Report"},
            'perf_pf':{'files':[['CEREBRO_ALERTS_DB_PERFORMANCE.py','CEREBRO_REPORTS_DB_PERFORMANCE.py','perf_pf']],'subject':"Performance Report"},
            'seo_rb':{'files':[['CEREBRO_ALERTS_DB_ROBOTS.py','skip.py','seo_rb']],'subject':"Robots-txt Report"},
            'seo_tag':{'files':[['CEREBRO_ALERTS_DB_SEO_CRAWL.py','skip.py','seo_tag']],'subject':"SEO Crawler Report"},
            'ext_serp':{'files':[['CEREBRO_ALERTS_DB_SEMRUSH_SERP.py','skip.py','ext_serp']],'subject':"SERP Report"},
            'ext_sr':{'files':[['CEREBRO_ALERTS_DB_SEMRUSH_DASHBOARD.py','CEREBRO_REPORTS_DB_SEMRUSH_DASHBOARD.py','ext_sr']],'subject':"SEM Rush Report"},
            'ext_sm':{'files':[['CEREBRO_ALERTS_DB_SEARCH_METRICS.py','CEREBRO_REPORTS_DB_SEARCH_METRICS.py','ext_sm']],'subject':"Search Metrics Report"},
            'ext_al':{'files':[['CEREBRO_ALERTS_DB_ALEXA.py','CEREBRO_REPORTS_DB_ALEXA.py','ext_al']],'subject':"Alexa Report"},
            'sec_ob':{'files':[['CEREBRO_ALERTS_DB_OBSERVATORY.py','CEREBRO_REPORTS_DB_OBSERVATORY.py','sec_ob']],'subject':"Observatory Report"},
            'key_ie':{'files':[['skip.py','CEREBRO_REPORTS_INTERNAL_SEARCHES.py','key_ie']],'subject':"Search Keywords Report"},
            }
           
    elif email_configuration == 'group' and check_scripts == 'hour':
        #The number of emails sent will be reduced by grouping similar alerts in blocks
        execute_files = {
            # 4th Block: SEO Tags
            'SEO Contents':{
            'files':[['CEREBRO_ALERTS_DB_ROBOTS.py','skip.py','seo_rb'],['CEREBRO_ALERTS_DB_SEO_CRAWL.py','skip.py','seo_tag']],
            'subject':'SEO Contents Report',
            },
            # 3rd Block: Performance
            'Performance':{
            'files':[['CEREBRO_ALERTS_DB_PERFORMANCE.py','skip.py','perf_pf'],
                    ['CEREBRO_ALERTS_DB_LIGHTHOUSE.py','skip.py','perf_lg']],
            'subject':'Performance Report',
            },         
            # 6th Block: Security
            'Security':{
            'files':[['CEREBRO_ALERTS_DB_OBSERVATORY.py','skip.py','sec_ob']],
            'subject':'Security Report',
            },
        }

    elif email_configuration == 'split' and check_scripts == 'hour':
        #the emails will all be sent split
        execute_files = {
            'seo_rb':{'files':[['CEREBRO_ALERTS_DB_ROBOTS.py','skip.py','seo_rb']],'subject':"Robots-txt Report"},
            'seo_tag':{'files':[['CEREBRO_ALERTS_DB_SEO_CRAWL.py','skip.py','seo_tag']],'subject':"SEO Crawler Report"},
            'perf_lg':{'files':[['CEREBRO_ALERTS_DB_LIGHTHOUSE.py','skip.py','perf_lg']],'subject':"Lighthouse Report"}, 
           'perf_pf':{'files':[['CEREBRO_ALERTS_DB_PERFORMANCE.py','skip.py','perf_pf']],'subject':"Lighthouse Report"},
            'sec_ob':{'files':[['CEREBRO_ALERTS_DB_OBSERVATORY.py','skip.py','sec_ob']],'subject':"Observatory Report"},
        }

    return execute_files

def get_stats_values(var, coefficient, format_type):
    #uses trimmean to get expected value
    trim_var = format_type(round(stats.trim_mean(var[:-1], 0.25),2))
    #uses interquartile range to estimate if values are outliers or not
    q75 = numpy.percentile(var, 75)
    q25 = numpy.percentile(var, 25)
    iqr = q75 - q25
    upperlimit = q75 + coefficient*iqr
    lowerlimit = q25 - coefficient*iqr
    crit_upperlimit = q75 + 2*coefficient*iqr
    crit_lowerlimit = q25 - 2*coefficient*iqr
    return trim_var, upperlimit, lowerlimit, crit_upperlimit, crit_lowerlimit
        
# -------------------------- RUNNING THE CEREBRO PROCESS FOR EMAILS --------------------------------
#sys.argv.append('single_user')
#sys.argv.append('single_email_group')
#sys.argv.append('single_email')
#sys.argv.append('single_script')
#sys.argv.append('reports')
#sys.argv.append('alerts')
#sys.argv.append('force_daily_scripts')
#sys.argv.append('force_receiver')

if 'single_user' in sys.argv:
    single_user = input('Insert user id to be analyzed: ')
    cursor.execute("select * from users where id = %s and active = 1;" %single_user)
else:
    cursor.execute("select * from users where active = 1;")
active_users = cursor.fetchall()

for active_user in active_users:
    owner_id = active_user['id']
    logging.info("\n----------------------------- ANALYZING ACTIVE USER %s... ---------------------------------" %owner_id)
    if 'single_email_group' in sys.argv or 'single_email' in sys.argv:
        single_email_group = input('Insert email group id to be analyzed on user %s: ' %owner_id)
        cursor.execute("select * from email_groups where (owner, id) = (%s,%s) and active = 1;" %(owner_id, single_email_group))
    else:
        cursor.execute("select * from email_groups where owner = %s and active = 1;" %owner_id)
    email_groups = cursor.fetchall()
    for email_group in email_groups:
        if 'force_receiver' not in sys.argv:
            toaddr = email_group['receivers']
            cc = email_group['cc']
            bcc = email_group['bcc']
            language = email_group['language']            
        elif 'force_receiver' in sys.argv and 'toaddr' not in locals():
            toaddr = input('Insert the email address who will receive everything: ')
            if 'simplex.live' in toaddr or 'simplexanalytics.com.br' in toaddr:
                logging.info('Starting debugging process...')
            else:
                logging.info('This email domain is not available for this feature... process was shut down')
                sys.exit()
            cc = None
            bcc = None
            language = input('Insert the language of the emails(pt/en): ')
            if language not in ['en','pt']:
                logging.info('This language is not available... process was shut down')
                sys.exit()
        email_group_id = email_group['id']
        client_name = email_group['client_name']

        timezone = get_set_tz_email(email_group_id)        
        sending_dict = {}
        n = 1

        if 'single_email' in sys.argv:
            single_email = input('Insert email id to be analyzed on email_group %s: ' %email_group_id)
            if 'alerts' in sys.argv:
                cursor.execute("select * from email_delivery where (email_group, id, email_type) = (%s,%s,'alert') and active = 1;" %(email_group_id, single_email))
            elif 'reports' in sys.argv:
                cursor.execute("select * from email_delivery where (email_group, id, email_type) = (%s,%s,'report') and active = 1;" %(email_group_id, single_email))
            else:
                cursor.execute("select * from email_delivery where (email_group, id) = (%s,%s);" %(email_group_id, single_email))
        else:                
            if 'alerts' in sys.argv:
                cursor.execute("select * from email_delivery where (email_group, email_type) = (%s,'alert') and active = 1;" %email_group_id)
            elif 'reports' in sys.argv:
                cursor.execute("select * from email_delivery where (email_group, email_type) = (%s,'report') and active = 1;" %email_group_id)
            else:
                cursor.execute("select * from email_delivery where email_group = %s and active = 1;" %email_group_id)
        emails_to_send = cursor.fetchall()

        logging.info("\n\n------------- Analyzing email_group %s to %s on %s ---------------" %(email_group_id, toaddr, client_name))
        if emails_to_send == ():
            logging.info("There are no emails setup for email group %s to %s" %(email_group_id, toaddr))
        for email_to_send in emails_to_send:
            send_hour = email_to_send['hour']
            hour_monitoring = email_to_send['hour_monitoring']
            weekdays = email_to_send['weekdays']
            email_configuration = email_to_send['delivery']
            name_greetings = email_to_send['greetings']
            email_type = email_to_send['email_type']
            email_id = email_to_send['id']
            alert_configuration = email_to_send['delivery']

            if weekdays == None or weekday not in weekdays and 'force_daily_scripts' not in sys.argv:
                logging.info("Email alert id %s is not enabled for group %s - %s on %s" %(email_id, email_group_id, toaddr, dict_weekdays[weekday]))
                continue
            elif weekdays == None or weekday not in weekdays and 'force_daily_scripts' in sys.argv:
                run_decision = input("Email alert id %s is not enabled for group %s - %s on %s. Do you want to run it anyway?(Y/N): " %(email_id, email_group_id, toaddr, dict_weekdays[weekday]))
                if run_decision != 'Y':
                    continue    

            #conditions for running the script in the moment
            current_send_hour = str(datetime.now(pytz.timezone(timezone)).strftime("%H:00"))

            daily_run_time = False
            if current_send_hour == send_hour or "force_daily_scripts" in sys.argv:
                daily_run_time = True

            if daily_run_time == True:
                if 'single_script' in sys.argv:
                    single_script = input('Insert script group initials: ')
                    execute_files = {}
                    pre_execute_files = get_execute_files('split')
                    pre_execute_files = pre_execute_files[single_script]
                    execute_files[single_script] = pre_execute_files
                else:
                    time_check = 'day'
                    execute_files = get_execute_files(alert_configuration, time_check)
                exec_keys = execute_files.keys()
                logging.info("Running daily scripts for user %s, email group %s, email id %s, alert %s, at %s (%s Time Zone)" %(owner_id, email_group_id, email_id, email_type, current_send_hour, timezone))
            elif hour_monitoring == None:
                logging.info("Hourly scripts for user %s, email group %s, email id %s, alert %s, at %s (%s Time Zone) are not set" %(owner_id, email_group_id, email_id, email_type, current_send_hour, timezone))
                continue
            else:
                time_check = 'hour'
                execute_files = get_execute_files(alert_configuration, time_check)
                exec_keys = execute_files.keys()
                logging.info("Running hourly scripts for user %s, email group %s, email id %s, alert %s, at %s (%s Time Zone)" %(owner_id, email_group_id, email_id, email_type, current_send_hour, timezone))

            #execute_files = {
            #'ga_rat':{'files':[['CEREBRO_ALERTS_DB_GA_GSC_RATIO.py','CEREBRO_REPORTS_DB_GA_GSC_RATIO.py','ga_rat']],'subject':"GA-GSC Ratio Report"},
            #'ga_br':{'files':[['CEREBRO_ALERTS_DB_GA_BROWSERS.py','CEREBRO_REPORTS_DB_GA_BROWSERS.py','ga_br']],'subject':"Google Analytics Browsers Report"},
            #'ga_tp':{'files':[['CEREBRO_ALERTS_DB_GA_TEMPLATES.py','CEREBRO_REPORTS_DB_GA_TEMPLATES.py','ga_tp']],'subject':"Google Analytics Templates Report"},
            #'ga_ads':{'files':[['CEREBRO_ALERTS_DB_GA_CAMPAIGNS.py','skip.py','ga_ch']],'subject':"Google Adwords Report"},
            #'ga_ch':{'files':[['CEREBRO_ALERTS_DB_GA_CHANNELS.py','CEREBRO_REPORTS_DB_GA_CHANNELS.py','ga_ch']],'subject':"Google Analytics Channels Report"},
            #'ga_ref':{'files':[['CEREBRO_ALERTS_DB_GA_REFERRALS.py','CEREBRO_REPORTS_DB_GA_REFERRALS.py','ga_ref']],'subject':"Google Images Referral Report"},
            #'gsc_idx':{'files':[['CEREBRO_ALERTS_DB_GSC_INDEX.py','CEREBRO_REPORTS_DB_GSC_INDEX.py','gsc_idx']],'subject':"Google Search Console Index Report"},
            #'gsc_st':{'files':[['CEREBRO_ALERTS_DB_GSC_STATS.py','CEREBRO_REPORTS_DB_GSC_STATS.py','gsc_st']],'subject':"Google Search Console Stats Report"},
            #'gsc_kpi':{'files':[['CEREBRO_ALERTS_DB_GSC_KPIS.py','CEREBRO_REPORTS_DB_GSC_KPIS.py','gsc_kpi']],'subject':"Google Search Console KPIs Report"},
            #'perf_pg':{'files':[['CEREBRO_ALERTS_DB_PAGESPEED.py','CEREBRO_REPORTS_DB_PAGESPEED.py','perf_pg']],'subject':"Pagespeed Report"},
            #'perf_lg':{'files':[['CEREBRO_ALERTS_DB_LIGHTHOUSE.py','CEREBRO_REPORTS_DB_LIGHTHOUSE.py','perf_lg']],'subject':"Lighthouse Report"},
            #'perf_pf':{'files':[['CEREBRO_ALERTS_DB_PERFORMANCE.py','CEREBRO_REPORTS_DB_PERFORMANCE.py','perf_pf']],'subject':"Performance Report"},
            #'seo_rb':{'files':[['CEREBRO_ALERTS_DB_ROBOTS.py','skip.py','seo_rb']],'subject':"Robots-txt Report"},
            #'seo_tag':{'files':[['CEREBRO_ALERTS_DB_SEO_CRAWL.py','skip.py','seo_tag']],'subject':"SEO Crawler Report"},
            #'ext_serp':{'files':[['CEREBRO_ALERTS_DB_SEMRUSH_SERP.py','skip.py','ext_serp']],'subject':"SERP Report"},
            #'ext_sr':{'files':[['CEREBRO_ALERTS_DB_SEMRUSH_DASHBOARD.py','CEREBRO_REPORTS_DB_SEMRUSH_DASHBOARD.py','ext_sr']],'subject':"SEM Rush Report"},
            #'ext_sm':{'files':[['CEREBRO_ALERTS_DB_SEARCH_METRICS.py','CEREBRO_REPORTS_DB_SEARCH_METRICS.py','ext_sm']],'subject':"Search Metrics Report"},
            #'ext_al':{'files':[['CEREBRO_ALERTS_DB_ALEXA.py','CEREBRO_REPORTS_DB_ALEXA.py','ext_al']],'subject':"Alexa Report"},
            #'sec_ob':{'files':[['CEREBRO_ALERTS_DB_OBSERVATORY.py','CEREBRO_REPORTS_DB_OBSERVATORY.py','sec_ob']],'subject':"Observatory Report"},
            #'key_ie':{'files':[['skip.py','CEREBRO_REPORTS_INTERNAL_SEARCHES.py','key_ie']],'subject':"Search Keywords Report"},
            #}
            #exec_keys = execute_files.keys()
            
            # TEM Q MUDAR ESSE SELECT DEPOIS
            # TEM Q MUDAR ESSE SELECT DEPOIS
            # TEM Q MUDAR ESSE SELECT DEPOIS, não é pra ser na monitoring_links
            allowed_url_ids = []
            cursor.execute("select id from monitoring_links where owner_id = %s;" %owner_id)
            allowed_urls = cursor.fetchall()
            for allowed_url in allowed_urls:
                allowed_url_ids.append(str(allowed_url['id']))
            # TEM Q MUDAR ESSE SELECT DEPOIS
            # TEM Q MUDAR ESSE SELECT DEPOIS
            # TEM Q MUDAR ESSE SELECT DEPOIS

            analyzed_urls = {}
            alerts_summary = {}
            reports_summary = {}
            already_commented = [] ##########

            for key in exec_keys:
                files_group = execute_files[key]['files']
                subject = email_to_send['subject']
                
                if subject == None:
                    subject = execute_files[key]['subject']
                    analyzed_urls = {}
                    alerts_summary = {}
                    reports_summary = {}

                if client_name != None:
                    subject = '%s - %s %s' %(subject, client_name, date)
                else:    
                    subject = '%s - %s' %(subject, date)
                subject_like = subject[:-11]    #removes the date from the string

                for execute_file in files_group:
                    dict_urls = {}
                    safe_analyzed_urls = analyzed_urls
                    file_emailtext = ''
                    try:
                        if email_type == 'alert' and execute_file[0] != '':
                            logging.info("\n\nRunning %s for email group %s, email id %s" %(execute_file[0], email_group_id, email_id))
                            exec(open(execute_file[0], encoding='utf-8').read())    #script for the alert
                        elif email_type == 'report' and execute_file[1] != '':
                            logging.info("\n\nRunning %s for email group %s, email id %s" %(execute_file[1], email_group_id, email_id))
                            exec(open(execute_file[1], encoding='utf-8').read())    #script for the alert
                        elif execute_file[0] != '' or execute_file[1] != '':
                            continue                       
                        else:
                            logging.error('Email configuration doesn\'t exist for email_group_id = %s, email_id = %s, owner_id = %s' %(email_group_id, email_id, owner_id))                            
                    except RuntimeError as e:
                        file_emailtext = ''
                        analyzed_urls = safe_analyzed_urls
                        logging.info('An Error was raised to escape child process: {}'.format(e))
                    except Exception as e:
                        file_emailtext = ''
                        analyzed_urls = safe_analyzed_urls
                        logging.error(e)
                        
                    if file_emailtext != '':
                        if subject not in sending_dict:
                            sending_dict[subject] = {'report':['','','',''],'alert':['','','','']}
                        cursor.execute("select max(id) from email_%s_history;" %script_type)
                        max_id = cursor.fetchall()[0]['max(id)'] + 1
                        
                        for email_subject in sending_dict.keys():
                            if sending_dict[email_subject][email_type][0] != '' and email_subject != subject:
                                max_id += 1
                            
                        email_database_update(table_name, script_type, max_id, dict_urls, date1)
                        sending_dict[subject][email_type][0] += file_emailtext
                        sending_dict[subject][email_type][1] = max_id
                        sending_dict[subject][email_type][2] = str(analyzed_urls)
                        if email_type == 'alert':
                            sending_dict[subject][email_type][3] = json.dumps(alerts_summary)
                        elif email_type == 'report':
                            sending_dict[subject][email_type][3] = json.dumps(reports_summary)
                    else:
                        logging.info("%s %s was not sent to email" %(subject_like, email_type))

        #after the entire block runs, an email is sent
        sending_keys = list(sending_dict.keys())
        for subject in sending_keys:
            emailtext = sending_dict[subject]['alert'][0] + sending_dict[subject]['report'][0]
            if sending_dict[subject]['alert'][0] != '' and sending_dict[subject]['report'][0] != '':
                email_issues = 'alert_and_report'
            elif sending_dict[subject]['alert'][0] != '' and sending_dict[subject]['report'][0] == '':
                email_issues = 'just_alert'
            elif sending_dict[subject]['alert'][0] == '' and sending_dict[subject]['report'][0] != '':
                email_issues = 'just_report'
            logging.info("\n\nCONSTRUCTING EMAIL '%s' FOR %s" %(subject.upper(), toaddr))
            exec(open("simplex_send_alert_email_v2.py").read())          #Runs the python script to send email
        if sending_dict != {}:
            exec(open('delete_images.py').read())

logging.info("All the processes were concluded")
