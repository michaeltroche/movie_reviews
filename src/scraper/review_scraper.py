### --- In this file, we scrape the rotten tomatoes website for user reviews --- ###
### --- Importing modules --- ###
import sys
sys.path.append('C:/Users/micha/Documents/Code/GitHub')

import json
import os
import random
import re
import time
from rotten_tomatoes_client import RottenTomatoesClient

import numpy as np
import pandas as pd
import requests

from movie_reviews.src.scraper.movie_scraper import get_next_movie



### --- This function allows vague movie title search and provides the movie name and url --- ###
def search_for_movie(search_name, movie_year):
    """
        search_for_movie finds basic movie info by sending non-exact movie search term to the RT API.

        Parameters
        ----------
        searchterm : str
            Any string corresponding to a movie title - doesn't need to be exact.

        Returns
        -------
        tuple
            (movie_name, url_id, meter_score)
        
        movie_name : str
            The name of the movie on RT.
        url_id : str
            The url code for the movie that allows for scraping on RT.
        meter_score : int
            The movie RT meter score.

        Examples
        --------
        >>> search_for_movie('Indiana Jones Raiders of the Lost Ark')
        ('Raiders of the Lost Ark', '/m/raiders_of_the_lost_ark')
    """

    movie_year = int(movie_year)

    # Provides search results for up to 5 movies
    result = RottenTomatoesClient.search(term=search_name, limit=5)
    
    # No movies found from search
    if result['movieCount'] == 0:
        movie_name = ''
        url_id = ''
        meter_score = 0
        return movie_name, url_id, meter_score

    # Finding exact movie by using corresponding release year
    for i in range(len(result['movies'])):
        if result['movies'][i]['year'] == movie_year:
            n = i
            break
    else:
        n = 0

    movie_name  = result['movies'][n]['name']
    url_id      = result['movies'][n]['url']
    meter_score = result['movies'][n]['meterScore']

    movie_name = movie_name.lower().replace(' ','_')
    print('current movie:',movie_name)

    return movie_name, url_id, meter_score



### --- get_movie_info function provides the movie id and movie name --- ###
def get_movie_id(url_id):
    """
    get_movie_id finds the unique movie id from RT.

    Parameters
    ----------
    url_id : str
        Used for the get request to the RT website.

    Returns
    -------
    movie_id : str
        Unique movie id required for scraping movie on RT.
    """
    # Requesting the HTML documentation
    response = requests.get(f'https://www.rottentomatoes.com/{url_id}/reviews?type=user')

    # Searching the HTML doc to extract the movie_id
    html_data  = json.loads(re.search('movieReview\s=\s(.*);', response.text).group(1))
    movie_id   = html_data['movieId']

    return movie_id



### --- get_reviews function flicks through the review pages --- ###
def get_review_page(endCursor, movie_id):
    """
    Changes the movie review page to the next one automatically.

    Parameters
    ----------
    endCursor : str
        Input to change onto next review page.
    movie_id : str
        Unique movie id required for scraping movie on RT.

    Returns
    -------
    reviews_page : dict
        dictionary containing reviews from one page of RT.
    """
    r = requests.get(f'https://www.rottentomatoes.com/napi/movie/{movie_id}/reviews/user',
    params = {
        "direction": "next",
        "endCursor": endCursor,
        "startCursor": ""
    })

    reviews_page = r.json()
    return reviews_page



### --- get_all_reviews function uses get_review_page to loop through thousands of review pages for our chosen movie --- ###
def get_all_reviews(movie_id):
    """
    get_all_reviews scrapes the current movie information.

    Parameters
    ----------
    movie_id : str
        Unique movie id required for scraping movie on RT.

    Returns
    -------
    reviews : list
        contains all the review information of one movie. This includes the review, user id 
        and user rating.
    """
    reviews = []
    result  = {}
    
    i = 0
    while True:
        try:
            # Random no. generator created to pause code and prevent overloading servers
            r = np.abs(np.random.randn()/3 + 1)
            time.sleep(r) #[s]

            # Gathering all movie review information into list, reviews
            result = get_review_page(result['pageInfo']['endCursor'] if i != 0  else '', movie_id)
            reviews.extend([t for t in result['reviews']])

            # Stopping loop at final page or after 5,000 pages
            if result['pageInfo']['hasNextPage']==False or i > 4999:
                break
            # Pausing for a minute after 10,000 reviews (100 pages)
            i += 1
            if i%1000==0:
                print(i)
                time.sleep(60)
        
        except requests.exceptions.RequestException:
            print('Wifi out, waiting...')
            time.sleep(30)
    
    return reviews



### --- Parsing function that obtains relevant data and puts it into a dataframe --- ###
def parse_reviews(movie_name, movie_id, movie_year, meter_score):
    """
    parses the reviews for chosen movie and saves information in a dataframe.

    Parameters
    ----------
    movie_name : str
        The name of the movie.
    movie_id : str
        Unique movie id required for scraping movie on RT.
    movie_year : str
        The year of release for the movie.
    meter_score : int
        The movie RT meter score.

    Returns
    -------
    df : DataFrame
        review dataframe for one movie.
    """
    reviews = get_all_reviews(movie_id)
    N = len(reviews)

    data = {}

    data['movie_name'] = [movie_name]*N
    data['movie_year'] = [movie_year]*N
    data['meter_score'] = [meter_score]*N

    # User id
    users_all = [reviews[i]['user']['userId'] for i in range(N)]
    users     = [reviews[i]['user']['userId'] 
                if len(users_all[i]) == 9 
                else np.nan 
                for i in range(N)]
    data['user'] = users

    # Review date
    date = [reviews[i]['updateDate'][:9] for i in range(N)]
    data['post_date'] = date

    # Verified
    verified = [reviews[i]['isVerified'] for i in range(N)]
    verified = [int(x) for x in verified]
    data['verified'] = verified

    # Super reviewer
    super_reviewer = [reviews[i]['isSuperReviewer'] for i in range(N)]
    super_reviewer = [int(x) for x in super_reviewer]
    data['super_reviewer'] = super_reviewer

    # Spoilers
    spoilers = [reviews[i]['hasSpoilers'] for i in range(N)]
    spoilers = [int(x) for x in spoilers]
    data['spoilers'] = spoilers

    # Profanity
    profanity = [reviews[i]['hasProfanity'] for i in range(N)]
    profanity = [int(x) for x in profanity]
    data['profanity'] = profanity

    # Written Review
    review         = [reviews[i]['review'] for i in range(N)]
    data['review'] = review

    # Star rating
    star_rating    = [reviews[i]['rating'] for i in range(N)]
    star_rating    = [float(x.replace('STAR_','').replace('_','.')) for x in star_rating]
    data['rating'] = star_rating
 
    # Creating dataframe of reviews
    df = pd.DataFrame(data)
    df.to_pickle(f'./review_dfs/{movie_name}.pkl')
    return df



# ### --- Run Code --- ###
if __name__ == '__main__':
    n = 100 - len(os.listdir('./review_dfs'))
    for i in range(n):
        search_name, movie_year = get_next_movie()
        movie_name, url_id, meter_score = search_for_movie(search_name, movie_year)

        # Can't find movie from automated search
        if movie_name == '':
            print('movie not found')
            search_name = search_name.lower().replace(' ','_')
            df = pd.DataFrame()
            df.to_pickle(f'./review_dfs/{search_name}.pkl')
            continue

        movie_id = get_movie_id(url_id)
        parse_reviews(movie_name, movie_id, movie_year, meter_score)