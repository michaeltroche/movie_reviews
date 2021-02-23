### --- This file scrapes the names of IMDB's 100 most controversial movies --- ###
### --- Importing modules --- ###
import os
import requests
import pickle
from bs4 import BeautifulSoup


### --- Scraping the movie data --- ###


# # Defining URL and requesting data
# url      = 'https://www.imdb.com/list/ls063133606/'
# response = requests.get(url)

# # Brewing the soup
# soup = BeautifulSoup(response.text, 'html.parser')

# # Parsing the film titles
# movie_all   = soup.find_all('div', {'class': 'lister-item mode-detail'})
# movie_names = []
# # Looping through every movie entry
# for movie in movie_all:
#     title_full = movie.find('h3', {'class': 'lister-item-header'}).text
#     title_full = title_full.split('\n')
#     title      = title_full[2]
    
#     # Appending the movie titles to movie_names
#     movie_names.append(title)


### --- Pickling the data for further use to prevent having to re-scrape code --- ###


# # Pickling
# with open('movies.txt', 'wb') as movie_file:
#     pickle.dump(movie_names, movie_file)

# Unpickling movie name file
with open('movies.txt', 'rb') as movie_file:
    movie_names = pickle.load(movie_file)

# Counting how many movie reviews have already been scraped
path, dirs, files = next(os.walk("./review_dfs"))
file_count = len(files)

# Movie to scrape next
print(movie_names[file_count])