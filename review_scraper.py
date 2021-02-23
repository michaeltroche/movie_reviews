### --- In this file, we scrape the rotten tomatoes website for user reviews --- ###
### --- Importing modules --- ###


import json
import random
import re
import time
from collections import defaultdict

import pandas as pd
import requests

# Scrape time
start = time.time()


### --- Scraping the movie review pages for our chosen movie --- ###


# Defining the URL and requesting the HTML documentation
url      = 'https://www.rottentomatoes.com/m/clockwork_orange/reviews?type=user'
response = requests.get(url)

# Searching the HTML doc to extract the movie_id
html_data  = json.loads(re.search('movieReview\s=\s(.*);', response.text).group(1))
movie_id   = html_data['movieId']
# Extracting movie_name for file saving
movie_name = html_data['title']
movie_name = movie_name.lower().replace(' ','_')


### --- Defining function to flick through the review pages --- ###


def get_reviews(endCursor):
    r = requests.get(f'https://www.rottentomatoes.com/napi/movie/{movie_id}/reviews/user',
    params = {
        "direction": "next",
        "endCursor": endCursor,
        "startCursor": ""
    })
    return r.json()


### --- Using get_reviews to loop through thousands of review pages for our chosen movie --- ###


# Empty reviews list and result dictionary
reviews = []
result  = {}
   
# Looping over review pages until final page or once 5,000 pages scraped
i = 0
while True:
    # Random no. generator created to pause code and prevent overloading servers
    # 0 < r < 1 
    r = random.random()
    time.sleep(2*r) #[s]

    # Gathering all movie review information into list: reviews
    result = get_reviews(result['pageInfo']['endCursor'] if i != 0  else '')
    reviews.extend([t for t in result['reviews']])

    # Stopping loop at final page or after 5,000 pages
    if result['pageInfo']['hasNextPage']==False:
        break
    elif i > 5000:
        break

    # Pausing for a minute after 1,000 reviews (100 pages)
    i += 1
    if i%100==0:
        time.sleep(60)


### --- Parsing the relevant data and putting it into a dataframe --- ###


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
df.to_pickle(f'./review_dfs/{movie_name}.pkl')


### --- Testing run time for movies --- ###


end = time.time()
print(f'Time to run:{(start-end)/3600:.2f} hrs')