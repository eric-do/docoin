from docoin.transactions import create_transaction, verify_transaction
from docoin.blockchain import Blockchain
from docoin.connections import ConnectionPool
import requests


class P2PProtocol:
    """Class for handling interactions with peers

    Attributes
      server: server class instance
      blockchain: blockchain class instance
      connections: connections class instance
    """

    def __init__(
        self,
        blockchain: Blockchain,
        connections: ConnectionPool
    ) -> None:
        self.blockchain = blockchain
        self.connections = connections

    def send_message(self, peer, message, payload=None) -> None:
        """Sends message to a specified peer
        """
        pass

    def handle_transaction(self, tx) -> None:
        """Handles transaction sent by peer

        We speed the distribution of transactions by helping to propogate
        the transaction to other peers - i.e. we do not want one node
        attempting to distribute to every peer.

        If the transaction does not exist in pending transactions, we
        propogate, else we stop.

        :param tx: <dict> transaction object
        :return: None
        """

        if verify_transaction(tx):
            if tx not in self.blockchain.current_transactions:
                self.blockchain.current_transactions.append(tx)
                # for peer in self.connections.connection_pool:
                #     requests.post()
