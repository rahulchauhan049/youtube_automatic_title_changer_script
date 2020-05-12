import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import datetime
import requests 
import time
from datetime import timedelta  
from datetime import datetime
import calendar



scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)


# api-endpoint 
URL = "https://www.googleapis.com/youtube/v3/videos"
key = open("api_key.txt", "r")
# defining a params dict for the parameters to be sent to the API 
PARAMS = {
    'part':'statistics',
    'id':'6o5oMFESgtQ',
    'key':key.read()
} 

viewCount = 0
commentCount = 0
likeCount = 0

while True:
    my_date = datetime.now() +  timedelta(minutes=330) 
    date = my_date.day
    year = my_date.year
    weekday = calendar.day_name[my_date.weekday()]
    month = calendar.month_name[my_date.month]

    ctime = str(weekday) + " " + str(month) + " " + str(date) + " " + str(year)

    try:
      r = requests.get(url = URL, params = PARAMS) 
    except requests.exceptions.HTTPError as errh:
      print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
      print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
      print ("OOps: Something Else",err)
    data = r.json() 

    print(data)

    if('items' in list(data.keys())):
      if viewCount == data['items'][0]['statistics']["viewCount"] and likeCount == data['items'][0]['statistics']["likeCount"] and commentCount == data['items'][0]['statistics']["commentCount"]:
        time.sleep(30)
        continue
      viewCount = data['items'][0]['statistics']["viewCount"]
      likeCount = data['items'][0]['statistics']["likeCount"]
      commentCount = data['items'][0]['statistics']["commentCount"]
    else:
      time.sleep(45)
      continue

    title = "On " + ctime +" IST, This Video has "+ str(viewCount)+ " Views, "+ str(commentCount)+" Comments and " + str(likeCount)+ " Likes"

    request = youtube.videos().update(
        part="snippet,status,localizations",
        body={
          "id": "6o5oMFESgtQ",
          "snippet": {
            "categoryId": 28,
            "defaultLanguage": "en",
            "description": "Download the Code from here: https://github.com/rahulchauhan049/youtube_automatic_title_changer_script",
            "tags": [
              "video, automatic subtitle, api, youtube api, changing title, youtube title change, automatic youtuble title change, titles"
            ],
            "title": title
          }
        }
    )
    response = request.execute()

    print(response)
    time.sleep(60)

