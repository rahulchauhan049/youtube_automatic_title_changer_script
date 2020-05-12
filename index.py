import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import datetime
import requests 
import time
from datetime import timedelta  



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
    'id':'Lw62SRyLHe8',
    'key':key.read()
} 

viewCount = 0
commentCount = 0
likeCount = 0

while True:
    now = datetime.datetime.today() +  timedelta(minutes=330) 
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

    if('items' in list(data.keys())):
      viewCount = data['items'][0]['statistics']["viewCount"]
      likeCount = data['items'][0]['statistics']["likeCount"]
      commentCount = data['items'][0]['statistics']["commentCount"]

    title = "On " +  str(now.ctime()) +" IST, This Video has "+ str(viewCount)+ " Views, "+ str(commentCount)+" Comments and " + str(likeCount)+ " Likes"

    request = youtube.videos().update(
        part="snippet,status,localizations",
        body={
          "id": "Lw62SRyLHe8",
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
    time.sleep(300)

