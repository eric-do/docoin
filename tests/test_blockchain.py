import pytest
import re
from docoin.blockchain import Blockchain, TransactionMinimumLengthError
from docoin.transactions import create_transaction


class TestBlockchain:

    def test_blockchain_initialization(self, blockchain):
        assert len(blockchain.chain) == 1
        assert len(blockchain.current_transactions) == 0
        assert len(blockchain.nodes) == 0

    def test_register_node(self, blockchain):
        address = 'http://testdomain.com/path/to/data'
        blockchain.register_node(address)
        assert len(blockchain.nodes) == 1
        assert "testdomain.com" in blockchain.nodes

    def test_successful_proof_of_work(self, blockchain):
        last_proof = blockchain.chain[0]['proof']
        proof = blockchain.proof_of_work(last_proof)

        assert isinstance(proof, int)
        assert blockchain.valid_proof(last_proof, proof) is True

    def test_create_new_block(self, blockchain, private_key, public_key):
        transaction_length = len(blockchain.current_transactions)
        last_proof = blockchain.chain[0]['proof']
        proof = blockchain.proof_of_work(last_proof)
        length = len(blockchain.chain)
        tx = create_transaction(
            sender_private_key=private_key,
            sender_public_key=public_key,
            recipient_public_key=public_key,
            amount=50
        )
        blockchain.current_transactions.append(tx)
        block = blockchain.new_block(proof)
        keys = [
            'index',
            'timestamp',
            'transactions',
            'proof',
            'previous_hash'
        ]
        assert all(k in block for k in keys)
        assert len(blockchain.chain) == length + 1
        assert len(block.get('transactions')) == transaction_length + 1

    def test_valid_proof(self, blockchain):
        last_proof = blockchain.chain[0]['proof']
        proof = blockchain.proof_of_work(last_proof)

        assert blockchain.valid_proof(last_proof, proof) is True
        assert blockchain.valid_proof(last_proof, 123456) is False

    def test_new_transaction(
        self,
        transaction,
        blockchain,
        private_key,
        public_key
    ):
        tx_length = len(blockchain.current_transactions)
        index = blockchain.new_transaction(transaction)
        assert len(blockchain.current_transactions) == tx_length + 1
        print(blockchain.chain)
        assert index == 2

    def test_add_block(self, block, blockchain):
        num_blocks = len(blockchain.chain)
        blockchain.add_block(block)

        assert len(blockchain.chain) == num_blocks + 1

    def test_add_invalid_block(self, invalid_block, blockchain):
        num_blocks = len(blockchain.chain)
        blockchain.add_block(invalid_block)

        assert len(blockchain.chain) == num_blocks

    def test_merkle_odd_count(self, blockchain):
        blockchain.current_transactions = [
            {
                'sender': 'eric',
                'recipient': 'tina',
                'amount': 4
            },
            {
                'sender': 'tina',
                'recipient': 'jessica',
                'amount': 5
            },
            {
                'sender': 'jessica',
                'recipient': 'amanda',
                'amount': 5
            },
        ]
        root = blockchain.merkle()

        assert re.match('^[A-Fa-f0-9]{64}$', root)
        assert root == '7d9a290b5b5e963b7bd1' +\
                       'b5411f073a19c37e6bda' +\
                       '789bce7eca05344088e7e6bd'

    def test_merkle_even_count(self, blockchain):
        blockchain.current_transactions = [
            {
                'sender': 'eric',
                'recipient': 'tina',
                'amount': 4
            },
            {
                'sender': 'tina',
                'recipient': 'jessica',
                'amount': 5
            }
        ]
        root = blockchain.merkle()

        assert re.match('^[A-Fa-f0-9]{64}$', root)

    def test_merkle_no_transactions(
        self,
        blockchain,
        private_key,
        public_key
    ):
        with pytest.raises(TransactionMinimumLengthError):
            blockchain.merkle()
