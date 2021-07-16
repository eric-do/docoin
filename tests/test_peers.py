import pytest
from docoin.peers import P2PProtocol
from docoin.blockchain import Blockchain
from docoin.connections import ConnectionPool


def test_handle_transaction(transaction):
    bc = Blockchain()
    peers = ConnectionPool()
    protocol = P2PProtocol(bc, peers)

    protocol.handle_transaction(transaction)
    assert len(bc.current_transactions) == 1
