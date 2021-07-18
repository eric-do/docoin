import os
from .blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4
from dotenv import load_dotenv
from docoin.transactions import create_transaction, verify_transaction

load_dotenv()


def create_app(test_config=None):

    app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # Unique address for this node
    blockchain = Blockchain(os.environ.get('PRIVATE_KEY'))

    @app.route('/', methods=['GET'])
    def frontend():
        return "<h1>DOCOIN EXPLORER</h1>"

    @app.route('/mine', methods=['GET'])
    def mine():
        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        # Successful mining is rewarded with a single coin
        tx = create_transaction(
            sender_private_key=os.environ.get('PRIVATE_KEY'),
            sender_public_key=os.environ.get('PUBLIC_KEY'),
            recipient_public_key=os.environ.get('PUBLIC_KEY'),
            amount=1
        )

        if verify_transaction(tx):
            _ = blockchain.new_transaction(tx)

        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }
        return jsonify(response), 200

    @app.route('/transactions/new', methods=['POST'])
    def new_transaction():
        values = request.get_json()

        # Verify required inputs
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'Missing values', 400

        # Create new transaction
        tx = create_transaction(
            values['sender'],
            values['recipient'],
            values['amount']
        )

        if verify_transaction(tx):
            index = blockchain.new_transaction(tx)

        response = {
            'message': f'Transaction will be added to Block {index}'
        }

        return jsonify(response), 201

    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return jsonify(response), 200

    @app.route('/nodes/register', methods=['POST'])
    def register_nodes():
        values = request.get_json()
        nodes = values.get('nodes')

        if nodes is None:
            return "Error: Please supply valid list of nodes", 400

        for node in nodes:
            blockchain.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(blockchain.nodes)
        }
        return jsonify(response), 201

    @app.route('/nodes/resolve', methods=['GET'])
    def consensus():
        replaced = blockchain.resolve_conflicts()

        if replaced:
            response = {
                'message': 'Our chain was replaced',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'message': 'Our chain is authoritative',
                'chain': blockchain.chain
            }

        return jsonify(response), 200

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)

    return app
