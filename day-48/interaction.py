from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create and configure the Chrome webdriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to Wikipedia
driver.get("https://en.wikipedia.org/wiki/Main_Page")

# Hone in on anchor tag using CSS selectors
article_count = driver.find_element(By.CSS_SELECTOR, value="#articlecount a")
# article_count.click()

# Search input is hidden when small screen
search_icon = driver.find_element(By.CSS_SELECTOR, value="#p-search a")
search_icon.click()

search = driver.find_element(By.NAME, value="search")
search.send_keys("Python")