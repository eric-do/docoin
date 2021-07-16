from docoin.blockchain import Blockchain


class TestBlockchain:

    def test_blockchain_initialization(self):
        blockchain = Blockchain()
        assert len(blockchain.chain) == 1
        assert len(blockchain.current_transactions) == 0
        assert len(blockchain.nodes) == 0

    def test_register_node(self):
        blockchain = Blockchain()
        address = 'http://testdomain.com/path/to/data'
        blockchain.register_node(address)
        assert len(blockchain.nodes) == 1
        assert "testdomain.com" in blockchain.nodes

    def test_successful_proof_of_work(self):
        blockchain = Blockchain()
        last_proof = blockchain.chain[0]['proof']
        proof = blockchain.proof_of_work(last_proof)

        assert isinstance(proof, int)
        assert blockchain.valid_proof(last_proof, proof) is True

    def test_create_new_block(self):
        blockchain = Blockchain()
        transaction_length = len(blockchain.current_transactions)
        last_proof = blockchain.chain[0]['proof']
        proof = blockchain.proof_of_work(last_proof)
        length = len(blockchain.chain)

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
        # assert len(block.get('transactions')) == transaction_length + 1

    def test_valid_proof(self):
        blockchain = Blockchain()
        last_proof = blockchain.chain[0]['proof']
        proof = blockchain.proof_of_work(last_proof)

        assert blockchain.valid_proof(last_proof, proof) is True
        assert blockchain.valid_proof(last_proof, 123456) is False

    def test_new_transaction(self):
        blockchain = Blockchain()
        tx_length = len(blockchain.current_transactions)
        index = blockchain.new_transaction('eric_sender', 'eric_recipient', 10)
        assert len(blockchain.current_transactions) == tx_length + 1
        assert index == 2

    def test_add_block(self, block):
        blockchain = Blockchain()
        num_blocks = len(blockchain.chain)
        blockchain.add_block(block)

        assert len(blockchain.chain) == num_blocks + 1

    def test_add_invalid_block(self, invalid_block):
        blockchain = Blockchain()
        num_blocks = len(blockchain.chain)
        blockchain.add_block(invalid_block)

        assert len(blockchain.chain) == num_blocks
