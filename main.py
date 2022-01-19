import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
paramaters_for_stonkz= {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": os.environ.get("STOCKS"),
}
paramaters_for_news = {
    "apiKey": os.environ.get("NEWS"),
    "qInTitle": COMPANY_NAME
}
stock_info = requests.get(STOCK_ENDPOINT, params=paramaters_for_stonkz)
data = stock_info.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday = data_list[0]
two_days_ago = float(data_list[1]['4. close'])
three_days_ago = float(data_list[2]['4. close'])
positive_difference = abs(int(two_days_ago)- int(three_days_ago))
difference_of_percentage = (positive_difference / three_days_ago)*100
articles = []
if difference_of_percentage > 5:
    news_response = requests.get(NEWS_ENDPOINT, params=paramaters_for_news)
    news_response.raise_for_status()
    news = news_response.json()['articles']
    for news_articles in news[:3]:
        articles.append(news_articles)
new_list = [f"Headline: {article['title']}. \n Brief:{article['description']}" for article in articles]
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for article in new_list:
    messages = client.messages.create(
        body=article,
        from_=os.environ.get("SENDER_NUMBER"),
        to=os.environ.get("RECEIVE_NUMBER")
    )