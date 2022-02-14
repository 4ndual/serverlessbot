from urllib.request import urlopen
from boto3.dynamodb.conditions import Attr
import json
import boto3
import urllib
import random




API_KEY="INSERT YOUR APIKEY HERE"


dynamodb=boto3.resource("dynamodb")
table_rated=dynamodb.Table("RATED")
table_watchlist=dynamodb.Table("watchlist")


def lambda_handler(event, context):
    
    body=json.loads(event['body'])
    message=body['message']
    text=message["text"]
    chat_id=message['chat']['id']
    
    print(text,chat_id)
    
    if text=="/start":
  
      text=text.replace("/echo", "")
      start(chat_id)
 
    
    if "/echo" in text:
  
      text=text.replace("/echo", "")
      send_echo(text, chat_id)

    if "/recommend" in text:
      recommend(chat_id)
      
    if "/watchlist" in text:
      watchlist(chat_id)


 
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
def send_echo(text, chat_id):

    tot = urllib.parse.quote_plus(text)
    url = "https://api.telegram.org/bot{API_KEY}/".format(API_KEY) + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    urlopen(url)

def start(chat_id):

    tot = urllib.parse.quote_plus("/start see all commands  \n\n/echo is literally a echo \n\n/recommend  i'll recommend you a good movie from @ndual list in imdb \n\n/watchlist i'll show you a random movie that is in @ndual watchlist \n\n/search this feature is under development \n\n/post this feature is under development")
    url = "https://api.telegram.org/bot{API_KEY}/".format(API_KEY) + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    urlopen(url)

def recommend(chat_id):
    
    movielis=table_rated.scan(FilterExpression=Attr("Your Rating").between("7","9") | Attr("Your Rating").eq("10") )
    result=movielis["Items"]
        
    while "lastEvalutatedKey" in movielis:
        lis=table_rated.scan(FilterExpression=Attr("Your Rating".between("7","9")) | Attr("Your Rating").eq("10"), ExclusiveStartKey=movielis["lastEvalutatedKey"])
        result.extend(movielis["Items"])
    
    radomresult=random.choice(result)

    tot = urllib.parse.quote_plus(radomresult["URL"])
    url = "https://api.telegram.org/bot{API_KEY}/".format(API_KEY) + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    urlopen(url)
    
def watchlist(chat_id):
    
    movielis=table_watchlist.scan()
    result=movielis["Items"]
        
    while "lastEvalutatedKey" in movielis:
        lis=table_watchlist.scan(ExclusiveStartKey=movielis["lastEvalutatedKey"])
        result.extend(movielis["Items"])
    
    randomresult=random.choice(result)

    tot = urllib.parse.quote_plus(randomresult["name"])
    url = "https://api.telegram.org/bot{API_KEY}/".format(API_KEY) + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    urlopen(url)
    
    