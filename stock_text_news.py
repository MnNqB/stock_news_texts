import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#Input from your own account
STOCK_API_KEY = ""
NEWS_API_KEY = ""
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

#Following website has api for getting stock data: https://www.alphavantage.co/documentation/#daily
#If stock price increase/decreases by x% between yesterday and the day before yesterday then retrieve news

#Yesterday's closing stock price
stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK_NAME,
    'apikey': STOCK_API_KEY,
    }

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

#Day before yesterday's closing stock price
db_yesterday_data = data_list[1]
db_yesterday_closing_price = db_yesterday_data["4. close"]

#Positive difference between the two
difference = abs(float(yesterday_closing_price) - float(db_yesterday_closing_price))
diff=float(yesterday_closing_price) - float(db_yesterday_closing_price)
if diff >0:
    trend = "🔺"
else:
    trend = "🔻"
    
#% difference in price
diff_pct = round((difference/float(yesterday_closing_price))*100)


#if % > set % - Get News
news_params = {
    'apiKey': NEWS_API_KEY,
    'qInTitle': COMPANY_NAME,
    }

if diff_pct > 5:
    news_response = requests.get(NEWS_ENDPOINT,params=news_params)
    articles = news_response.json()["articles"]
    print(articles)


#get first n articles
n=1
n_articles = articles[:n]
print(n_articles)

#Format retrieved data
formatted_article=[f"{STOCK_NAME}: {trend}{diff_pct}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in n_articles]


#Text stock, %trend and article
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for article in formatted_article:
    message = client.messages.create(
        body=article,
        from_="",#Twilio assigned no
        to="")#Receiving #
