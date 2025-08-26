from bs4 import BeautifulSoup
import requests

response = requests.get(url="https://news.ycombinator.com/news")
yc_web_page = response.text
# print(yc_web_page)

soup = BeautifulSoup(yc_web_page, "html.parser")
# articles = soup.find_all(name="a", class_="storylink")
articles = soup.find_all(name="span", class_="titleline") # the resource had new structure
article_texts = []
article_links = []
for article_tag in articles:
    article_tag_a = article_tag.find(name="a")
    text = article_tag_a.getText()
    article_texts.append(text)
    link = article_tag_a.get("href")
    article_links.append(link)

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

largest_number = max(article_upvotes)
largest_index = article_upvotes.index(largest_number)

print(article_texts[largest_index])
print(article_links[largest_index])

# print(article_texts)
# print(article_links)
# print(article_upvotes)

