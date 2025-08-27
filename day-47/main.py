from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the price below which you would like to get a notification
BUY_PRICE = 70

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/dp/B075CYMYK6"

# Replace with your browser's headers
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
}

# response = requests.get(practice_url)
response = requests.get(live_url, headers=header)

soup = BeautifulSoup(response.content, "html.parser")
price_tag = soup.find(name="span", class_="priceToPay")
price_text = price_tag.getText() # Don't know why, but add this extra line and then it works!
price = float(price_text.replace("$", ""))
print(price)

if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"

    # ====================== Send the email ===========================

    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        result = connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL_ADDRESS"],
            to_addrs=os.environ["EMAIL_ADDRESS"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )