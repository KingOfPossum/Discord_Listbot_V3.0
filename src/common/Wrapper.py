from wrapper import IGDBWrapper

class Wrapper:
    """
    A static wrapper for IGDB API requests.
    """
    wrapper = IGDBWrapper("vhxxz4jvptvoj99f6arnjii3wgzq47",
                          "ydclz2x5k42rru95bzgr6kqvxfmum9")

    @staticmethod
    def request(endpoint, query) -> dict:
        """
        Makes a request to the IGDB API using the static wrapper instance.
        :param endpoint: The API endpoint to query.
        :param query: The query string to send to the endpoint.
        :return: The response from the IGDB API.
        """
        return Wrapper.wrapper.request(endpoint=endpoint, query=query)