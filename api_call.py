from rotten_tomatoes_client import RottenTomatoesClient

def search_for_movie(searchterm):
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

    result = RottenTomatoesClient.search(term=searchterm, limit=5)
    url  = result['movies'][0]['url']
    name = result['movies'][0]['name']
    return name, url