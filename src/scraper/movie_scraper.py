### --- This file scrapes the names of IMDB's 100 most controversial movies --- ###
### --- Importing modules --- ###
import os
import pickle

import requests
from bs4 import BeautifulSoup


### --- Scraping the movie names and years of release  --- ###
def get_next_movie():
    """
    get_next_movie scrapes the list of 100 movies from IMDB using BeautifulSoup and saves them to file. It
    then finds and returns the next movie to be scraped using the file of already scraped movies.

    Returns
    -------
    tuple : (next_movie, next_movie_year)

    next_movie : str
        The next movie to be scraped.
    next_movie_year : str
        Year of release of the next movie.
    """

    if 'movies.pkl' not in os.listdir('./accesories'):
        # Defining URL and requesting data
        url      = 'https://www.imdb.com/list/ls063133606/'
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
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


        # Pickling the data for further use to prevent having to re-scrape code
        with open('./accesories/movies.pkl', 'wb') as movie_file:
            pickle.dump([movie_names, movie_years], movie_file)

    
    # Unpickling movie names and release
    with open('./accesories/movies.pkl', 'rb') as movie_file:
        movie_names, movie_years = pickle.load(movie_file)
    
    file_count = len(os.listdir('./review_dfs'))
    next_movie = movie_names[file_count]
    next_movie_year = movie_years[file_count]

    # Returns the next movie to scrape
    return next_movie, next_movie_year