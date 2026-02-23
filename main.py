import os
import requests


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


apikey = os.environ.get("API_KEY")

# TIME_SERIES_DAILY_ADJUSTED
ENDPOINT = "https://www.alphavantage.co/query"

params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey": apikey
}

response = requests.get(url=ENDPOINT, params=params)
response.raise_for_status()
# print(response.status_code)
# print(response.text)
data = None
if response.status_code == 200:
    data = response.json()
# print(data)


1000-900/900 * 100
# start = None
# end

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
    get_percent = get_stock_percent(data=data)

    if get_percent < -5 or get_percent > 5:
        # do something get the news
        print("Got something")

    else:
        print("Nothing to be told")


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