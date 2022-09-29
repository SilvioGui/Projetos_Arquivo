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

from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from lib import google_api as myGoogleApi
import datetime
from datetime import datetime, timedelta
import time
        
# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('table_id', type=str,  help=('The table ID of the profile you wish to access. Format is ga:xxx where xxx is your profile ID.'))
argparser.add_argument('site', type=str,  help=('Site'))
argparser.add_argument('start_date', type=str,  help=('Date of data extraction. Format is YYYY-MM-DD.'))
argparser.add_argument('end_date', type=str,  help=('Date of data extraction. Format is YYYY-MM-DD.'))
argparser.add_argument('ga_ua', type=str,  help=('ga_ua'))


def main(argv):
    service, flags = myGoogleApi.myServiceFlags(argv, 'analytics', parents=[argparser], site=sys.argv[2], ua=sys.argv[5])

    global start_date, end_date
    start_date = flags.start_date
    end_date = flags.end_date    

    try:
        results = get_api_query(service, flags.table_id).execute()
        print_rows(results)
        
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

  
def get_api_query(service, table_id):
    """Returns a query object to retrieve data from the Core Reporting API.

    Args:
      service: The service object built by the Google API Python client library.
      table_id: str The table ID form which to retrieve data.
    """

    return service.data().ga().get(
          ids=table_id,
          start_date = str(start_date),
          end_date = str(end_date),
          metrics='ga:searchUniques',
          dimensions='ga:searchKeyword',
          sort='-ga:searchUniques',
          start_index='1',
          max_results='500')

def print_rows(results):
    if results.get('rows', []):
        for row in results.get('rows'):            
            print(row[0].replace("_"," ").replace("landing page moteur ","")+'\t'+row[1])
            #print(row[0].replace("_"," ")+'\t'+row[1])
      
      

if __name__ == '__main__':
    main(sys.argv)
