import os
import requests
from requests.exceptions import HTTPError
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

TVDB_API = 'https://api.thetvdb.com'
MOVIEDB_API = 'https://api.themoviedb.org/3/search/movie'
SLACK_API = 'https://hooks.slack.com/services/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'
TVDB_API_KEY = ''
MOVIEDB_API_KEY = ''
LANGUAGE = 'en-US'

slack_title = ''
slack_overview = ''
query = ''


def get_tv_series():
    try:
        payload = {
        'language': 'en-US',
        'include_adult': 'false',
        'query': ''
        }
        headers = {
        'api_key': TVDB_API_KEY,
        'Accept': 'application/json', 
        'Content-Type': 'application/json'
        }
        requests.get(url = TVDB_API, headers = headers, json = payload, timeout = 1.0)
    except TimeoutError as e:
        print(f'Exception Raised: ', e)
        raise

def get_movie():
    global query
    query = 'Equalizer'
    try:
        payload = {}
        headers = {
        'Accept': 'application/json', 
        'Content-Type': 'application/json',
        }
        r = requests.get(url = MOVIEDB_API + f'?api_key={MOVIEDB_API_KEY}&include_adult=false&query={query}', headers = headers, data = payload, timeout = 5.0)
        response = r.json()
        global slack_title
        global slack_overview
        results = response['results']
        for i in results:
            print(i['title'])
            print(i['overview'])
            slack_title = i['title']
            slack_overview = i['overview']
            post_to_slack()
        print(response['total_results'])
    except TimeoutError as e:
        print(f'Exception Raised: ', e)
        raise

def post_to_slack():

    try:
        payload = {
        'attachments': [
            {
                'title': f'{slack_title}',
                'text': f'{slack_overview}',
                'actions': [
                    {
                        'name': 'action',
                        'type': 'button',
                        'text': 'Yes',
                        'style': '',
                        'value': 'complete'
                    }
                ]
            }
        ]
        }
        headers = {
        'Accept': 'application/json', 
        'Content-Type': 'application/json'
        }
        requests.post(url = SLACK_API, headers = headers, json = payload, verify = False, timeout = 5.0)
        #r.raise_for_status() # Raise an HTTPError if receive a status of 4xx or 5xx
    except TimeoutError as e:
        print(f'Exception Raised: ', e)
        raise

get_movie()
