from docoin.peers import P2PProtocol
from docoin.blockchain import Blockchain
from docoin.connections import ConnectionPool
from time import time


def test_handle_transaction(blockchain, transaction):
    peers = ConnectionPool()
    protocol = P2PProtocol(blockchain, peers)

    protocol.handle_transaction(transaction)
    assert len(blockchain.current_transactions) == 1


def test_handle_block(block, blockchain: Blockchain):
    block_count = len(blockchain.chain)
    peers = ConnectionPool()
    protocol = P2PProtocol(blockchain, peers)
    protocol.handle_block(block)

    assert len(blockchain.chain) == block_count + 1


def test_handle_invalid_block(invalid_block, blockchain: Blockchain):
    block_count = len(blockchain.chain)
    peers = ConnectionPool()
    protocol = P2PProtocol(blockchain, peers)
    protocol.handle_block(invalid_block)

    assert len(blockchain.chain) == block_count
