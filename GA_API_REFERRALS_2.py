#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reference command-line example for Google Analytics Core Reporting API v3.

This application demonstrates how to use the python client library to access
all the pieces of data returned by the Google Analytics Core Reporting API v3.

The application manages autorization by saving an OAuth2.0 token in a local
file and reusing the token for subsequent requests.

Before You Begin:

Update the client_secrets.json file

  You must update the clients_secrets.json file with a client id, client
  secret, and the redirect uri. You get these values by creating a new project
  in the Google APIs console and registering for OAuth2.0 for installed
  applications: https://code.google.com/apis/console

  Learn more about registering your analytics application here:
  http://developers.google.com/analytics/devguides/reporting/core/v3/gdataAuthorization

Supply your TABLE_ID

  You will also need to identify from which profile to access data by
  specifying the TABLE_ID constant below. This value is of the form: ga:xxxx
  where xxxx is the profile ID. You can get the profile ID by either querying
  the Management API or by looking it up in the account settings of the
  Google Anlaytics web interface.

Sample Usage:

  $ python core_reporting_v3_reference.py ga:xxxx

Where the table ID is used to identify from which Google Anlaytics profile
to retrieve data. This ID is in the format ga:xxxx where xxxx is the
profile ID.

Also you can also get help on all the command-line flags the program
understands by running:

  $ python core_reporting_v3_reference.py --help
"""
from __future__ import print_function

__author__ = 'api.nickm@gmail.com (Nick Mihailovski)'

import argparse
import sys
import datetime
from datetime import datetime, timedelta

from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from lib import google_api as myGoogleApi

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('table_id', type=str,  help=('The table ID of the profile you wish to access. Format is ga:xxx where xxx is your profile ID.'))
argparser.add_argument('start_date', type=str,  help=('The start date for data extraction in "yyyy-mm-dd" format.'))
argparser.add_argument('end_date', type=str,  help=('The end date for data extraction in "yyyy-mm-dd" format.'))
argparser.add_argument('site', type=str,  help=('Site'))
argparser.add_argument('ga_ua', type=str,  help=('ga_ua'))
argparser.add_argument('query_metric', type=str,  help=('Metric for the API query'))
argparser.add_argument('query_segment', type=str,  help=('Filter for the API query'))

#'ga:medium==referral;deviceCategory==mobile'

def main(argv):

    # Authenticate and construct service.
    service, flags = myGoogleApi.myServiceFlags(argv, 'analytics', parents=[argparser], site=sys.argv[4], ua=sys.argv[5])
    # service, flags = sample_tools.init(
    #     argv, 'analytics', 'v3', __doc__, __file__, parents=[argparser],
    #     scope='https://www.googleapis.com/auth/analytics.readonly')

    # Try to make some requests to the API. Print the results or handle errors.
    # each request extracts data from 1 channel
    try:
        #date1 = datetime.strptime(str(flags.end_date), "%Y-%m-%d").date()
        #query_dates = [str(date1)]
        #date0 = datetime.strptime(str(flags.start_date), "%Y-%m-%d").date()
        #while date1 != date0:
        #    date1 = date1 - timedelta(days=1)
        #    query_dates.append(str(date1))

        results = get_api_query(service, flags.table_id, flags.end_date, flags.end_date, 'sessions', flags.query_segment,'sessions', 5).execute()
        query_dims = print_rows(results, flags.query_metric, True)
        
        #for query_date in query_dates:      
        #    #Total Traffic
        #    results = get_api_query(service, flags.table_id, query_date, flags.query_metric, flags.query_filter, 50).execute()
        #    print(query_date, "All Devices Referral:")
        #    print_rows(results, flags.query_metric, False)    
        for query_dim in query_dims:      
            #Total Traffic
            results = get_api_query(service, flags.table_id, flags.start_date, flags.end_date, flags.query_metric, flags.query_segment + ';ga:source==' + query_dim, 'date', 100).execute()
            print(flags.query_segment + ';ga:source==' + query_dim)
            print_rows(results, flags.query_metric, False)    

    except TypeError as error:
        # Handle errors in constructing a query.
        print(('There was an error in constructing your query : %s' % error))

    except HttpError as error:
        # Handle API errors.
        print(('Arg, there was an API error : %s : %s' %
             (error.resp.status, error._get_reason())))

    except AccessTokenRefreshError:
        # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
               'the application to re-authorize')
  
def get_api_query(service, table_id, startdate, enddate, metric, segmento, sort_by, n_results):
    """Returns a query object to retrieve data from the Core Reporting API.

    Args:
      service: The service object built by the Google API Python client library.
      table_id: str The table ID form which to retrieve data.
    """
    
    if metric != 'sessions':
        return service.data().ga().get(
              ids=table_id,
              start_date = startdate,
              end_date = enddate,
              metrics='ga:sessions,ga:'+metric,
              dimensions='ga:date,ga:source',
              sort='-ga:'+sort_by,
              segment=segmento,
              #filters=channel,     #separates similar filters by coma (dimensions) and different by dotcoma (metrics)
              start_index='1',
              max_results= n_results)
    else:
        return service.data().ga().get(
              ids=table_id,
              start_date = startdate,
              end_date = enddate,
              metrics='ga:'+metric,
              dimensions='ga:date,ga:source',
              sort='-ga:'+sort_by,
              segment=segmento,
              #filters=channel,     #separates similar filters by coma (dimensions) and different by dotcoma (metrics)
              start_index='1',
              max_results= n_results)

def print_rows(results, metric, get_condition):
    query_dims = []
    if results.get('rows', []):
        for row in results.get('rows'):
            if get_condition == False:
                date = row[0][0:4]+'-'+row[0][4:6]+'-'+row[0][6:8]
                if metric != 'sessions':
                    print(date+'\t'+row[1]+'\t'+row[2]+'\t'+row[3])
                else:
                    print(date+'\t'+row[1]+'\t'+row[2])
            elif get_condition == True:
                query_dims.append(row[1])
        if get_condition == True:
            print("\n".join(query_dims))
        print('No Rows Found')
        return query_dims

if __name__ == '__main__':
    main(sys.argv)
