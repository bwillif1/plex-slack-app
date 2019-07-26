import os
import requests
from requests.exceptions import HTTPError
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

TVDB_API = "https://api.thetvdb.com"
MOVIEDB_API = "https://api.themoviedb.org/3/search/movie"
MOVIEDB_URL = "https://www.themoviedb.org/movie/"
SLACK_API = "https://hooks.slack.com/services/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"
TVDB_API_KEY = os.environ["TVDB_API_KEY"]
MOVIEDB_API_KEY = os.environ["MOVIEDB_API_KEY"]
LANGUAGE = "en-US"
MOVIE_IMG = "https://image.tmdb.org/t/p/original"

slack_title = ""
slack_overview = ""
query = "Shaft"
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
        global moviedb_url
        global movie_release_date
        global page_one_results
        global result_response
        result_count = response["total_results"]
        results = response["results"]
        page_one_results = len(response["results"])
        if result_count > page_one_results:
            result_response = f"\n But I'll only show you the first {page_one_results} :smile:"
        else:
            result_response = ""
        for i in results:
            slack_title = i["title"]
            slack_overview = i["overview"]
            if i["poster_path"]:
                movie_img_url = MOVIE_IMG + i["poster_path"]
            moviedb_url = MOVIEDB_URL + str (i["id"]) + "?language=en-US"
            if i["release_date"]:
                movie_release_date = i["release_date"]
                movie_release_date = datetime.strptime(movie_release_date, "%Y-%m-%d").strftime('%B %d, %Y')
            post_to_slack()
        print(result_count)
        print(page_one_results)
    except TimeoutError as e:
        print(f"Exception Raised: ", e)
        raise

def post_to_slack():

    try:
        payload = {   

            "text": f"*I found {result_count} movie title(s) with the name* `{query}`{result_response}",
            "attachments": [
                {
                    "title": f"{slack_title}",
                    "title_link": f"{moviedb_url}",
                    "text": f"*Release Date: {movie_release_date}*",
                    "color": "#36a64f",
                    "fields": [
                        {
                            "value": f"{slack_overview}"
                        }
                    ],
                    "actions": [
                        {
                            "type": "button",
                            "text": "Download",
                            "style": "primary",
                            "url": "https://flights.example.com/book/r123456"
                        }
                    ],
                    "image_url": f"{movie_img_url}"
                }
            ],
            "type": "divider"
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

# Problems to solve:
#
# Storing each movie result as an attachment one at a time
#   Ideas:
#   1. Keep movie results in variable and post to slack the result at array 0
#      Add a "next" button which allows user to display the result at array 1
#      And so on for the next button