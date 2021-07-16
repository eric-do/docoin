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


def test_handle_block(block, blockchain: Blockchain):
    block_count = len(blockchain.chain)
    peers = ConnectionPool()
    protocol = P2PProtocol(blockchain, peers)
    protocol.handle_block(block)

    assert len(blockchain.chain) == block_count + 1
