import os
import requests
import datetime as dt
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


def call_api_stock(apikey)-> dict:
    ENDPOINT_STOCK = "https://www.alphavantage.co/query"
    params = {
        "function" : "TIME_SERIES_DAILY",
        "symbol" : STOCK,
        "apikey": apikey
    }
    response = requests.get(url=ENDPOINT_STOCK, params=params)
    response.raise_for_status()
    return response.json() if response.status_code == 200 else None

def news_api(apikey)-> dict:
    endpoint = "https://newsapi.org/v2/everything"
    now = str(dt.date.today()).split("-")
    now[-1] = int(now[-1]) -3

    now = list(map(int, now))

    t=  dt.date(year=now[0], month=now[1], day=now[-1])
    d = dt.date(year=now[0], month=now[1], day=now[-1]- 3)
    
    params = {
        "apiKey": apikey,
        "q": "\"Tesla Inc\"" ,
        "language": "en",
        "from": d,
        "to": t,
        "sortBy": "relevancy",
        "searchIn": "title,description,content"
    }

    response = requests.get(url=endpoint, params=params)
    response.raise_for_status()
    # print(response.text)

    return response.json() if response.status_code == 200 else None

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stock_percent(data: dict) -> float:
    prices = []
    for c,i in enumerate(data["Time Series (Daily)"]):
        if c == 2:
            break
        prices.append(data["Time Series (Daily)"][i]["4. close"])

    # print(prices)
    yesterday, day_before_yesterday = map(float,prices)

    total = day_before_yesterday - yesterday

    formula = round((abs(total)/day_before_yesterday) * 100, 2)

    if str(total).startswith("-"):
        return float(f"-{formula}")
    return formula


def main():
    down_up = ["🔺", "🔻"]
    # apikey_stock = os.environ.get("API_KEY")
    apikey_stock = os.getenv(key="TESLA")
    apikey_news = os.getenv(key="NEWS")
    stock = call_api_stock(apikey=apikey_stock)
    print(stock)
    news = news_api(apikey=apikey_news)
    # if stock == None:
    #     print("Check the url you provided")
    #     return
    # get_percent = get_stock_percent(data=stock)
    print(news)
    # if get_percent < -5 or get_percent > 5:
    #     # do something get the news
    #     print("Got something")

    # else:
    #     print("Nothing to be told")

    account_sid = os.getenv("SID")
    auth_token = os.getenv("API")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="+12566854735",
        body="Hello moshifa",
        to='+27607047759',
        
    )
    # print(message.sid)
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

if __name__ == '__main__':
    main()