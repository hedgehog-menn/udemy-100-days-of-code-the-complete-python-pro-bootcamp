import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "__YOUR_STOCK_API_KEY__"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "__YOUR__NEWS_API_KEY__"

TWILIO_SID = "__YOUR_TWILIO_ACCOUNT_ID__"
TWILO_AUTH_TOKEN = "__YOUR_TWILIO_AUTH_TOKEN__"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)


## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.

    formatted_articles = [f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}\nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles[2])

    # Send each article as a separate message via Twilo
    client = Client(TWILIO_SID, TWILO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages \
            .create(
            body=articles,
            from_="YOUR TWILIO VIRTUAL NUMBER",
            to="YOUR TWILIO VERIFIED REAL NUMBER"
        )

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
