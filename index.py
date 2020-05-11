import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import datetime
import requests 
import time


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
    'id':'WCXLnBRhrYE',
    'key':key.read()
} 

while True:
    now = datetime.datetime.today()

    r = requests.get(url = URL, params = PARAMS) 
    data = r.json() 
    viewCount = data['items'][0]['statistics']["viewCount"]
    likeCount = data['items'][0]['statistics']["likeCount"]
    commentCount = data['items'][0]['statistics']["commentCount"]
    title = "On " +  str(now.ctime()) +" IST, This Video has "+ str(viewCount)+ " Views and "+ str(commentCount)+" Comments"

    request = youtube.videos().update(
        part="snippet,status,localizations",
        body={
          "id": "Lw62SRyLHe8",
          "snippet": {
            "categoryId": 22,
            "defaultLanguage": "en",
            "description": "This title tells the correct time",
            "tags": [
              "new tags"
            ],
            "title": title
          }
        }
    )
    response = request.execute()

    print(response)
    time.sleep(10)

