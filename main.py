import os
import requests
import datetime as dt
from twilio.rest import Client
from dotenv import load_dotenv
import smtplib
import pprint
from email.message import EmailMessage

load_dotenv()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

def get_news(data: dict) -> dict:

    news = {}

    for i in data["articles"][:3]:
        if "brief" not in news.keys():
            news["brief"] = f"{i["title"]}. "

        else:
            news["brief"] += f"{i["title"]}. "

        if "headline" not in news.keys():
            news["headline"] = f"{i["description"]}. "
        else:
            news["headline"] += f"{i["description"]}. "
    return news



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
        "q": "\"Tesla Inc\"" "+Tesla Inc",
        "language": "en",
        "from": d,
        "to": t,
        "sortBy": "relevancy",
        "searchIn": "title,description,content"
    }

    response = requests.get(url=endpoint, params=params)
    response.raise_for_status()

    return response.json() if response.status_code == 200 else None

def get_stock_percent(data: dict) -> float:
    prices = []
    for c,i in enumerate(data["Time Series (Daily)"]):
        if c == 2:
            break
        prices.append(data["Time Series (Daily)"][i]["4. close"])

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
    password = os.getenv(key="PASS")
    mail = os.getenv(key="USER")
    stock = call_api_stock(apikey=apikey_stock)
    # print(stock)
    news = news_api(apikey=apikey_news)
    if stock == None:
        print("Check the url you provided")
        return
    get_percent = get_stock_percent(data=stock)
    percent = down_up[-1] if get_percent < 0 else down_up[0]
    clean =  get_news(data=news)

    if get_percent < -5 or get_percent+10 > 5:
        print("we are here")

        msg = EmailMessage()
        msg["subject"] = f"Tesla Inc: {percent}{get_percent}%"
        msg["From"] = mail
        msg["To"] = mail
        msg.set_content(
            f"""
Brief: {clean['brief']}\n
Headline: {clean['headline']}"""
        )

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls(),
            connection.login(user=mail, password=password)
            connection.send_message(msg)

        print("Message sent successfuly")

    else:
        print("Nothing to be told")

if __name__ == '__main__':
    main()