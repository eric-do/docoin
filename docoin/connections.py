from urllib.parse import urlparse


class ConnectionPool:
    """Class for maintaining connection to peers

    Peers are other nodes in the network. The purpose of this class
    is to store, add, remove peers from network.

    Attributes:
     connection_pool: a dictionary of all peers
    """

    def __init__(self):
        self.connection_pool = set()

    @staticmethod
    def get_address(url: str) -> str:
        """Returns the domain from url

        :param url: <str> url to be parsed
        :return: <str> domain parsed from url
        """
        return urlparse(url).netloc

    def add_peer(self, url) -> None:
        """Adds peer to connection pool

        :param url: <str> url from peer request
        :return: None
        """
        self.connection_pool.add(self.get_address(url))

    def remove_peer(self, url) -> None:
        """Remove peer from connection pool

        :param url: <str> url from peer request
        :return: None
        """
        self.connection_pool.remove(self.get_address(url))
