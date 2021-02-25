### --- In this file, we scrape the rotten tomatoes website for user reviews --- ###
### --- Importing modules --- ###


import json
import random
import re
import time
from collections import defaultdict

import pandas as pd
import requests

from movie_scraper import get_next_movie 
from api_call import search_for_movie


### --- get_movie_info function provides the movie id and movie name --- ###


def get_movie_info(url_id):
    # Requesting the HTML documentation
    response = requests.get(f'https://www.rottentomatoes.com/{url_id}/reviews?type=user')

    # Searching the HTML doc to extract the movie_id
    html_data  = json.loads(re.search('movieReview\s=\s(.*);', response.text).group(1))
    movie_id   = html_data['movieId']
    # Extracting movie_name for file saving
    movie_name = html_data['title']
    movie_name = movie_name.lower().replace(' ','_')

    print(f'Saving name is: {movie_name}')

    # Returning movie_id and movie_name
    return movie_name, movie_id


### --- get_reviews function flicks through the review pages --- ###


def get_review_page(endCursor, movie_id):
    r = requests.get(f'https://www.rottentomatoes.com/napi/movie/{movie_id}/reviews/user',
    params = {
        "direction": "next",
        "endCursor": endCursor,
        "startCursor": ""
    })
    return r.json()


### --- get_all_reviews function uses get_review_page to loop through thousands of review pages for our chosen movie --- ###


def get_all_reviews(movie_id):
    # Empty reviews list and result dictionary
    reviews = []
    result  = {}
    
    i = 0
    while True:
        try:
            # Random no. generator created to pause code and prevent overloading servers
            r = random.random()
            time.sleep(2*r) #[s]

            # Gathering all movie review information into list: reviews
            result = get_review_page(result['pageInfo']['endCursor'] if i != 0  else '', movie_id)
            reviews.extend([t for t in result['reviews']])

            # Stopping loop at final page or after 5,000 pages
            if result['pageInfo']['hasNextPage']==False:
                break
            elif i > 5000:
                break

            # Pausing for a minute after 10,000 reviews (100 pages)
            i += 1
            if i%1000==0:
                time.sleep(60)
        
        except requests.exceptions.RequestException:
            print('Wifi out, waiting...')
            time.sleep(30)
    
    return reviews


### --- Parsing function that obtains relevant data and puts it into a dataframe --- ###


def parse_reviews(save_name, movie_id):
    # Getting all reviews
    reviews = get_all_reviews(movie_id)

    # Empty data dictionary
    data = defaultdict(list)

    # Finding reviewers who have user id's 
    users_all = [reviews[i]['user']['userId'] for i in range(len(reviews))]
    idx       = [i for i in range(len(users_all)) if len(users_all[i]) == 9]
    users     = [reviews[i]['user']['userId'] for i in idx]
    data['user'].extend(users)

    # Verified
    super_reviewer = [reviews[i]['isSuperReviewer'] for i in idx]
    super_reviewer = [int(x) for x in super_reviewer]
    data['super_reviewer'].extend(super_reviewer)

    # Profanity
    profanity = [reviews[i]['hasProfanity'] for i in idx]
    profanity = [int(x) for x in profanity]
    data['profanity'].extend(profanity)

    # Written Review
    data['review'].extend([reviews[i]['review'] for i in idx])

    # Star rating
    star_rating = [reviews[i]['rating'] for i in idx]
    star_rating = [float(x.replace('STAR_','').replace('_','.')) for x in star_rating]
    data['rating'].extend(star_rating)

    # Creating dataframe of reviews
    df = pd.DataFrame(data)
    df.to_pickle(f'./review_dfs/{save_name}.pkl')
    return df


### --- Run Code --- ###


if __name__ == '__main__':
    start = time.time()

    # Calling functions
    search_name, movie_year = get_next_movie()
    movie_name, url_id      = search_for_movie(search_name, int(movie_year))
    save_name, movie_id     = get_movie_info(url_id)
    parse_reviews(save_name, movie_id)

    end = time.time()
    print(f'Time to run:{(start-end)/3600:.2f} hrs')