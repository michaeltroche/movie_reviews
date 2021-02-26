### --- This file scrapes the names of IMDB's 100 most controversial movies --- ###
### --- Importing modules --- ###
import os
import requests
import pickle
from bs4 import BeautifulSoup


## --- Scraping the movie names and years of release  --- ###
def get_movies():
    # Defining URL and requesting data
    url      = 'https://www.imdb.com/list/ls063133606/'
    response = requests.get(url)

    # Brewing the soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Parsing the movie info
    movie_all   = soup.find_all('div', {'class': 'lister-item mode-detail'})

    # Looping over every movie to parse the name and year
    movie_names = []
    movie_years = []
    for movie in movie_all:
        title_full = movie.find('h3', {'class': 'lister-item-header'}).text
        title_full = title_full.split('\n')
        title      = title_full[2]

        year_full = movie.find('span', {'class': 'lister-item-year'}).text
        year      = year_full[1:5]

        movie_names.append(title)
        movie_years.append(year)


    ### --- Pickling the data for further use to prevent having to re-scrape code --- ###
    with open('movies.pkl', 'wb') as movie_file:
        pickle.dump([movie_names, movie_years], movie_file)


### --- Function to find next movie to scrape in review_scraper file --- ###
def get_next_movie():
    if 'movies.pkl' not in os.listdir():
        get_movies()

    # Unpickling movie names and release
    with open('movies.pkl', 'rb') as movie_file:
        movie_names, movie_years = pickle.load(movie_file)
    
    file_count = len(os.listdir('./review_dfs'))

    # Returns the next movie to scrape
    return movie_names[file_count], movie_years[file_count]