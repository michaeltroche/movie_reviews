### --- This file finds the movie url and name --- ###
### --- Importing modules --- ###
from rotten_tomatoes_client import RottenTomatoesClient


### --- This function allows vague movie title search and provides the movie name and url --- ###


def search_for_movie(search_name, movie_year):
    """
        Send any search term to the RT API.

        Parameters
        ----------
        searchterm : str
            Any string corresponding to a movie title.
            Doesn't need to be exact

        Returns
        -------
        tuple
            (name : str, url : str)

        Examples
        --------
        >>> search_for_movie('Indiana Jones Raiders of the Lost Ark')
        ('Raiders of the Lost Ark', '/m/raiders_of_the_lost_ark')
    """
    
    movie_year = int(movie_year)

    # Provides search results for up to 5 movies
    result = RottenTomatoesClient.search(term=search_name, limit=10)

    # Finding exact movie by using corresponding release year
    for i in range(len(result['movies'])):
        if result['movies'][i]['year'] == movie_year:
            n = i
            break
        else:
            n = 0

    movie_name = result['movies'][n]['name']
    url_id     = result['movies'][n]['url']
    
    return movie_name, url_id