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

"""Example for using the Google Url Crawl Erros Counts API (part of Search Console API).
This example demonstrates how to query Google
search results data for your property. Learn more at
https://developers.google.com/webmaster-tools/
To use:
1) Install the Google Python client library, as shown at https://developers.google.com/webmaster-tools/v3/libraries.
2) Sign up for a new project in the Google APIs console at https://code.google.com/apis/console.
3) Register the project to use OAuth2.0 for installed applications.
4) Copy your client ID, client secret, and redirect URL into the client_secrets.json file included in this package.
5) Run the app in the command-line as shown below.
Sample usage:
  $ python api_sample.py 'https://www.example.com/' '2015-05-01' '2015-05-30'
"""

#Insert in command line the code below (you must be in the same directory this file)
#   python GSC_API_errors.py http://www.buscape.com.br/ 2017-05-10 2017-05-30    ###url must end in '/' and parameters can't be inside quotes
#Files "client_id.json" and "client_secrets.json" should also be in the same folder. Follow the links in the beginning to create those files
#A file named "webmasters.dat" will be generated, and it should remain in the same folder. It's the authentication file
#in a first moment you will need to enter the website and authorize the request from this API

import argparse
import time, datetime
import sys
from googleapiclient import sample_tools
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from lib import google_api as myGoogleApi

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('property_url', type=str, help=('Site or app URL to query data for (including trailing slash).'))
argparser.add_argument('error', type=str, help=('Error type to get the sample.'))
argparser.add_argument('platform', type=str, help=('Platform type to get the sample.'))

def main(argv):
    service, flags = myGoogleApi.myServiceFlags(argv, 'webmasters', parents=[argparser], site=sys.argv[1])
    # service, flags = sample_tools.init(
    #     argv, 'webmasters', 'v3', __doc__, __file__, parents=[argparser],
    #     scope='https://www.googleapis.com/auth/webmasters.readonly')
    # This query shows data for the entire range, grouped and sorted by day,
    # descending; any days without data will be missing from the results.

    response = execute_request(service, flags.property_url, flags.error, flags.platform)
    if response != {}:
        if 'urlCrawlErrorSample' in response:
            response = response['urlCrawlErrorSample']
            response = sorted(response, key=lambda k: k['last_crawled'], reverse=True)[0:3]
                                                                                       
            for line in response:
                if 'urlDetails' in line and 'responseCode' in line:
                    if 'containingSitemaps' in line['urlDetails']:
                        print(str(line['responseCode']) + '\t' + str(line['last_crawled']) + '\t' + '/'+line['pageUrl']  + '\t' + str(line['urlDetails']['linkedFromUrls'][0:5]) + '\t' + str(line['urlDetails']['containingSitemaps']))
                    else:
                        print(str(line['responseCode']) + '\t' + str(line['last_crawled']) + '\t' + '/'+line['pageUrl']  + '\t' + str(line['urlDetails']['linkedFromUrls'][0:5]))
                elif 'urlDetails' in line and 'responseCode' not in line:
                    if 'containingSitemaps' in line['urlDetails']:
                        print('---' + '\t' + str(line['last_crawled']) + '\t' + '/'+line['pageUrl']  + '\t' + str(line['urlDetails']['linkedFromUrls'][0:5]) + '\t' + str(line['urlDetails']['containingSitemaps']))
                    else:
                        print('---' + '\t' + str(line['last_crawled']) + '\t' + '/'+line['pageUrl']  + '\t' + str(line['urlDetails']['linkedFromUrls'][0:5]))
                elif 'urlDetails' not in line and 'responseCode' in line:
                    print(str(line['responseCode']) + '\t' + str(line['last_crawled']) + '\t' + '/'+line['pageUrl'])

def execute_request(service, property_url, catg, type_platform):
    """Executes a urlcrawlerroscount.query request.
    Args:
      service: The webmasters service to use when executing the query.
      property_url: The site or app URL to request data for.
      request: The request to be executed.
    Returns:
      An array of response rows.
    """

    return service.urlcrawlerrorssamples().list(siteUrl=property_url,category=catg,platform=type_platform).execute()

if __name__ == '__main__':
  main(sys.argv)
