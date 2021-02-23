import pandas as pd
from collections import defaultdict
import pickle

import requests
import urllib.request
import re
import json


# Defining the URL and requesting the HTML documentation
url = 'https://www.rottentomatoes.com/m/the_dig_2021/reviews?type=user'
response = requests.get(url)

# Searching the HTML doc to extract the movie_id
html_data  = json.loads(re.search('movieReview\s=\s(.*);', response.text).group(1))
movie_id  = html_data['movieId']
# Extracting movie_name for file saving
movie_name = html_data['title']
movie_name = movie_name.lower().replace(' ','_')

# Function to flick through the review pages
def getReviews(endCursor):
    r = requests.get(f'https://www.rottentomatoes.com/napi/movie/{movie_id}/reviews/user',
    params = {
        "direction": "next",
        "endCursor": endCursor,
        "startCursor": ""
    })
    return r.json()


# Empty reviews list and result dictionary
reviews = []
result = {}
   
# Looping over review pages until final page
i = 0
while True:
    result = getReviews(result['pageInfo']['endCursor'] if i != 0  else '')
    if result['pageInfo']['hasNextPage']==False:
        reviews.extend([t for t in result['reviews']])
        break
    reviews.extend([t for t in result['reviews']])
    i += 1


# Empty data dictionary
data = defaultdict(list)

# Finding reviewers who have user id's 
users_all = [reviews[i]['user']['userId'] for i in range(len(reviews))]
idx = [i for i in range(len(users_all)) if len(users_all[i]) == 9]
users = [reviews[i]['user']['userId'] for i in idx]
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