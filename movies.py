import requests
from bs4 import BeautifulSoup
import re
import csv
import matplotlib.pyplot as plt

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.content, "html.parser")

movies_divs = soup.find_all("div", class_="cli-title")
information_divs = soup.find_all("div", class_="cli-title-metadata")
ratings_spans = soup.find_all("span", attrs={"aria-label": re.compile(r"IMDb rating: \d+\.\d+")})

movies_data = []

for movie_div, info_div, rating_span in zip(movies_divs, information_divs, ratings_spans):
    title_tag = movie_div.find("h3", class_="ipc-title__text")
    title = title_tag.text.strip()
    
    metadata_items = info_div.find_all("span", class_="sc-b189961a-8 kLaxqf cli-title-metadata-item")
    
    year = metadata_items[0].text.strip() if len(metadata_items) > 0 else "No disponible"
    duration = metadata_items[1].text.strip() if len(metadata_items) > 1 else "No disponible"
    classification = metadata_items[2].text.strip() if len(metadata_items) > 2 else "No disponible"

    rating = rating_span['aria-label'].replace("IMDb rating: ", "").strip()

    movies_data.append([title, year, duration, classification, rating])

    print(f"Título: {title}, Año: {year}, Duración: {duration}, Clasificación: {classification}, Rating: {rating}")


with open('imdb_top_movies.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Título", "Año", "Duración", "Clasificación", "Rating"])
    writer.writerows(movies_data)

ratings = [float(movie[4]) for movie in movies_data]
plt.hist(ratings, bins=10, edgecolor='black')
plt.xlabel('Rating de IMDb')
plt.ylabel('Número de películas')
plt.title('Distribución de las calificaciones de IMDb para las mejores películas')
plt.show()
