from bs4 import BeautifulSoup
import requests

URL="https://www.empireonline.com/movies/features/best-movies-2"

response = requests.get(URL)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

all_movies = soup.find_all(name="span", class_="content_content__i0P3p")
"""
movie_titles = []
for tag in all_movies:
    movie_title_tag = tag.select_one("h2 strong")
    if movie_title_tag:
        title = movie_title_tag.getText()
        print(title)
        movie_titles.append(title)
movie_titles.reverse()
"""
movie_titles = [tag.select_one("h2 strong").getText() for tag in all_movies[::-1] if tag.select_one("h2 strong") is not None]
with open("movies.txt", "w") as file:
    for title in movie_titles:
        file.write(f"{title}\n")
