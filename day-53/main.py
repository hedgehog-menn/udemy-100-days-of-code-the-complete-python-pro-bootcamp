# BeautifulSoup (Part 1)
from bs4 import BeautifulSoup
import requests
# Selenium (Part 2)
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfFYTVRhySKy9ZeUxKjWUacsEpcNzD1LL5t9TUrCTzZ5Ec_sg/viewform?usp=header"

# Part 1 - Scrape the links, addresses, and prices of the rental properties

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

# Use our Zillow-Clone website (instead of Zillow.com)
response = requests.get(ZILLOW_URL, headers=header)

data = response.text
soup = BeautifulSoup(data, "html.parser")

address_tags = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
link_list = [address_a.get("href") for address_a in address_tags]
price_tags = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
price_list = [
    price_span.getText().replace("+", "")
                        .replace("1bd", "")
                        .replace("1 bd", "")
                        .replace("/mo", "").strip() for price_span in price_tags
    ]
address_list = [address_a.getText().strip() for address_a in address_tags]

# Part 2 - Fill in the Google Form using Selenium

chrome_options = webdriver.ChromeOptions()
# (Optional/Dev mode) Keep Chrome browser open after program finishes
# chrome_options.add_experimental_option("detach", True)
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM_URL)

for index in range(len(link_list)):
    all_input = driver.find_elements(By.TAG_NAME, "input")
    if all_input[3]: # fixed if there are hidden inputs
        all_input[3].clear()
        all_input[4].clear()
        all_input[5].clear()
        all_input[3].send_keys(address_list[index])
        all_input[4].send_keys(price_list[index])
        all_input[5].send_keys(link_list[index])
    else:
        all_input[0].clear()
        all_input[1].clear()
        all_input[2].clear()
        all_input[0].send_keys(address_list[index])
        all_input[1].send_keys(price_list[index])
        all_input[2].send_keys(link_list[index])
    # Click Submit
    submit_btn = driver.find_element(By.CSS_SELECTOR, "[aria-label='Submit']")
    submit_btn.click()
    time.sleep(0.125) # optional, adjust preferred speed

    # Restart another form
    restart_a_tag = driver.find_element(By.TAG_NAME, "a") # the first one
    restart_a_tag.click()
    time.sleep(0.125) # optional, adjust preferred speed
