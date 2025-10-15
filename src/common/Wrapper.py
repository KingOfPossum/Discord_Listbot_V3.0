from common.ConfigLoader import ConfigLoader
from wrapper import IGDBWrapper

class Wrapper:
    """
    A static wrapper for IGDB API requests.
    """
    wrapper = None

    @classmethod
    def init(cls):
        """
        Initializes the Wrapper by loading client_id and client_secret from config.
        """
        client_id = ConfigLoader.get_config().igdb_client_id
        client_secret = ConfigLoader.get_config().igdb_client_secret
        cls.wrapper = IGDBWrapper(client_id, client_secret)

    @staticmethod
    def request(endpoint, query) -> dict:
        """
        Makes a request to the IGDB API using the static wrapper instance.
        :param endpoint: The API endpoint to query.
        :param query: The query string to send to the endpoint.
        :return: The response from the IGDB API.
        """
        return Wrapper.wrapper.request(endpoint=endpoint, query=query)