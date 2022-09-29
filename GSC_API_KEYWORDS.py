#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Google Inc. All Rights Reserved.
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

"""Example for using the Google Search Analytics API (part of Search Console API).
A basic python command-line example that uses the searchAnalytics.query method
of the Google Search Console API. This example demonstrates how to query Google
search results data for your property. Learn more at
https://developers.google.com/webmaster-tools/
To use:
1) Install the Google Python client library, as shown at https://developers.google.com/webmaster-tools/v3/libraries.
2) Sign up for a new project in the Google APIs console at https://code.google.com/apis/console.
3) Register the project to use OAuth2.0 for installed applications.
4) Copy your client ID, client secret, and redirect URL into the client_secrets.json file included in this package.
5) Run the app in the command-line as shown below.
Sample usage:
  $ python GSC_API_q.py http://www.buscape.com.br/ 2017-05-10 2017-05-30 branded
"""

#Insert in command line the code below (you must be in the same directory this file)
#   python GSC_API_q.py http://www.buscape.com.br/ 2017-05-10 2017-05-30 branded   ###url must end in '/' and parameters can't be inside quotes
#Files "client_id.json" and "client_secrets.json" should also be in the same folder. Follow the links in the beginning to create those files
#A file named "webmasters.dat" will be generated, and it should remain in the same folder. It's the authentication file
#in a first moment you will need to enter the website and authorize the request from this API

import argparse
import sys
from googleapiclient import sample_tools
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from lib import google_api as myGoogleApi
from operator import itemgetter



# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_url', type=str, help=('Site or app URL to query data for (including trailing slash).'))
argparser.add_argument('start_date', type=str,  help=('Start date of the requested date range in YYYY-MM-DD format.'))
argparser.add_argument('end_date', type=str,  help=('Start date of the requested date range in YYYY-MM-DD format.'))
argparser.add_argument('brand_term', type=str, help=('Sets if the data to be analyzes is branded or non branded'))


def main(argv):
    service, flags = myGoogleApi.myServiceFlags(argv, 'webmasters', parents=[argparser], site=sys.argv[1])
    # service, flags = sample_tools.init(
    #     argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
    #     scope = 'https://www.googleapis.com/auth/webmasters.readonly')
    brand_term = flags.brand_term

    request = {
        'startDate': flags.start_date,
        'endDate': flags.end_date,
        'sort': 'impressions',
        'dimensions': ['query'],
        'dimensionFilterGroups':
        [{
            'filters':
            [{
                 'dimension': 'query',
                 'operator': 'notcontains',
                 'expression': brand_term    #insert main brand term here
            }]
        }],
        'rowLimit': 500
    }
    response = execute_request(service, flags.property_url, request)
    print_table(response)
    # a secondary term filter must be applied in the python script which calls this one (on its line 66)
  
def execute_request(service, property_url, request):
    """Executes a searchAnalytics.query request.
    Args:
      service: The webmasters service to use when executing the query.
      property_url: The site or app URL to request data for.
      request: The request to be executed.
    Returns:
      An array of response rows.
    """
    return service.searchanalytics().query(siteUrl=property_url, body=request).execute()


def print_table(response):
    """Prints out a response table.
    Each row contains key(s), clicks, impressions, CTR, and average position.
    Args:
      response: The server response to be printed as a table.
    """

    if 'rows' not in response:
        print ('EMPTY RESPONSE')
        return

    dict_rows = {}
    rows = response['rows']
    
    for row in rows:
        keys = ''
        # Keys are returned only if one or more dimensions are requested.
        if 'keys' in row:
          keys = (row['keys'])[0]
        dict_rows[keys]=int(row['impressions'])

    rows_list = (sorted(dict_rows.items(), key=itemgetter(1)))[::-1]
    for row in rows_list:
        print(row[0]+'\t'+str(row[1]))
  
if __name__ == '__main__':
    main(sys.argv)

