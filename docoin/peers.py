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

    def handle_transaction(self, transaction) -> None:
        """Handles transaction sent by peer

        We speed the distribution of transactions by helping to propogate
        the transaction to other peers - i.e. we do not want one node
        attempting to distribute to every peer.

        If the transaction already exists, we stop.

        :param transaction: <dict> transaction object
        :return: None
        """

        if verify_transaction(transaction):
            if transaction not in self.blockchain.current_transactions:
                self.blockchain.current_transactions.append(transaction)
                for peer in self.connections.connection_pool:
                    self.send_transaction(peer, transaction)

    def handle_block(self, block) -> None:
        """Handles block sent by peer

        We speed the distribution of blocks by helping to propogate
        the block to other peers - i.e. we do not want one node
        attempting to distribute to every peer.

        If the block cannot be added to the chain, we stop.

        :param block: <dict> transaction object
        :return: None
        """
        if self.blockchain.add_block(block):
            for peer in self.connections.connection_pool:
                self.send_block(peer, block)

    def send_transaction(self, peer, transaction) -> None:
        """Sends transaction to a peer

        :param peer: <str> url of peer
        :param transaction: <dict> transaction dict
        :return: None
        """
        requests.post(
            f'/{peer}/transaction',
            data=transaction,
            type='application/json'
        )

    def send_block(self, peer, block) -> None:
        """Sends block to a peer

        :param peer: <str> url of peer
        :param transaction: <dict> transaction dict
        :return: None
        """
        requests.post(
            f'/{peer}/block',
            data=block,
            type='application/json'
        )
