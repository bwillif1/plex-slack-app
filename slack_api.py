import os
import requests
from requests.exceptions import HTTPError
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

TVDB_API = "https://api.thetvdb.com"
MOVIEDB_API = "https://api.themoviedb.org/3/search/movie"
SLACK_API = "https://hooks.slack.com/services/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"
TVDB_API_KEY = os.environ["TVDB_API_KEY"]
MOVIEDB_API_KEY = os.environ["MOVIEDB_API_KEY"]
LANGUAGE = "en-US"
MOVIE_IMG = "https://image.tmdb.org/t/p/original"

slack_title = ""
slack_overview = ""
query = "White Men Can't Jump"
result_count = ""
movie_img_url = ""
movie_release_date = ""

def read_input():
    print("something")

def get_tv_series():
    try:
        payload = {
        "language": "en-US",
        "include_adult": "false",
        "query": ""
        }
        headers = {
        "api_key": TVDB_API_KEY,
        "Accept": "application/json", 
        "Content-Type": "application/json"
        }
        requests.get(url = TVDB_API, headers = headers, json = payload, timeout = 1.0)
    except TimeoutError as e:
        print(f"Exception Raised: ", e)
        raise

def get_movie():
    global query
    try:
        payload = {}
        headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
        }
        r = requests.get(url = MOVIEDB_API + f"?api_key={MOVIEDB_API_KEY}&include_adult=false&query={query}", headers = headers, data = payload, timeout = 5.0)
        response = r.json()
        global slack_title
        global slack_overview
        global result_count
        global movie_img_url
        global movie_release_date
        result_count = response["total_results"]
        results = response["results"]
        for i in results:
            if i["poster_path"] != "null":
                slack_title = i["title"]
                slack_overview = i["overview"]
                movie_img_url = MOVIE_IMG + i["poster_path"]
                movie_release_date = i["release_date"]
                movie_release_date = datetime.strptime(movie_release_date, "%Y-%m-%d")
                movie_release_date = movie_release_date.strftime('%B %d, %Y')
                print(movie_release_date)
                print(movie_img_url)
                post_to_slack()
        print(result_count)
    except TimeoutError as e:
        print(f"Exception Raised: ", e)
        raise

def post_to_slack():

    try:
        payload = {
        
        "text": f"*I found {result_count} movie title(s) with the name* `{query}` :smile:",
        "attachments": [
            {
                "title": f"{slack_title} \nRelease Date: {movie_release_date}",
                "text": f"{slack_overview}",
                "color": "#3AA3E3",
                "actions": [
                    {
                        "type": "button",
                        "text": "Download",
                        "style": "primary",
                        "url": "https://flights.example.com/book/r123456"
                    }
                ],
                "image_url": f"{movie_img_url}"
            },
        ]
    }

        headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json"
        }
        requests.post(url = SLACK_API, headers = headers, json = payload, verify = False, timeout = 5.0)
        #r.raise_for_status() # Raise an HTTPError if receive a status of 4xx or 5xx
    except TimeoutError as e:
        print(f"Exception Raised: ", e)
        raise

get_movie()


#	"type": "section",
#		"text": {
#			"type": "plain_text",
#			"text": f"We found {result_count} movies the name {query} in it",
 #           "emoji": "true"
#		    },