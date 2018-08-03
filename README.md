# meetup2-chatbot
LINE Chatbot to Make QA Life Easier

## Prerequisuite
* Python 3.6

# Project Setup
#### Create Your Own LINE Channel (Messaging API)
Please follow the steps on this page: https://developers.line.me/en/docs/messaging-api/getting-started/

## Environment Variables
```
export LINE_CHANNEL_SECRET=<your channel secret>
export LINE_CHANNEL_ACCESS_TOKEN=<your channel access token>
export JENKINS_URL=<your Jenkins URL>
export JENKINS_USER=<your Jenkins Username>
export JENKINS_USER_TOKEN=<your Jenkins User Token> *
export VIDEO_BUCKET_URL_PREFIX=<Video Storage Url> *
```
* *JENKINS_USER_TOKEN:* You can create your own Jenkins User Token by following steps below
  1. Login to your Jenkins
  2. Click at your username
  3. Click **Configure**
  4. Click **Show API Token** or create a new one
  
* *VIDEO_BUCKET_URL_PREFIX:* I recommended using [Amazon S3](https://aws.amazon.com/s3/) or public cloud storage to store your recorded videos

## Create Python Virtual Environment
```
sh$ virtualenv -p python3 venv
sh$ source venv/bin/activate
sh$ pip install -r requirements.txt
sh$ python app.py
* Serving Flask app "app" (lazy loading)
* Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
* Debug mode: off
* Running on http://0.0.0.0:8666/ (Press CTRL+C to quit)
```

## Test Chatbot
```
sh$ curl -i -X GET http://localhost:8666/
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 16
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Fri, 03 Aug 2018 03:41:19 GMT

{"status":"up"}
```
