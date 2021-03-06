from docoin.transactions import create_transaction
import os
import hashlib
import json
from attr import has
import requests
from time import time
from urllib.parse import urlparse
import hashlib


class TransactionMinimumLengthError(Exception):
    def __init__(self, message="Block must contain at least one transaction"):
        self.message = message


class Blockchain(object):
    """Blockchain class

    Attributes:
      chain: a list of all Blocks in the chain
      current_transactions: list of pending transactions
    """
    def __init__(
        self,
        private_key=os.environ.get('PRIVATE_KEY'),
        public_key=os.environ.get('PUBLIC_KEY'),
    ):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        tx = create_transaction(
            sender_private_key=private_key,
            sender_public_key=public_key,
            recipient_public_key=public_key,
            amount=1
        )
        self.current_transactions.append(tx)
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address) -> None:
        """Add a new node to the list of nodes

        :param address: <str> Address of node, e.g. 'http://192.168.0.5:5000'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain) -> bool:
        """Determin if a given blockchain is valid
        :param chain: <list> a blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

    def resolve_conflicts(self) -> bool:
        """Consensus Algorithm for resolving conflicts

        The algorithm replaces our chain with the longest chain in network.
        :return: <bool> True if our chain was replaced, False if not
        """
        neighbors = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        """Create a new Block in the Blockchain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'merkle_root': self.merkle(),
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def add_block(self, block) -> bool:
        """Add block to the blockchain

        Adds a block to the chain.

        If the new block does not contain all the current node's current
        transactions, the remaining transactions will be left in the
        pool.

        :param block: <dict> the block to be added to the chain
        """
        if self.valid_proof(self.last_block['proof'], block['proof']):
            self.current_transactions = [tx for tx in self.current_transactions
                                         if tx not in block['transactions']]
            self.chain.append(block)
            return True
        else:
            return False

    def new_transaction(self, transaction) -> int:
        """Add a transaction to the next mined Block

        :param transaction: <dict> the transaction dict
        :return: <int> The index of the Block for this transaction
        """
        self.current_transactions.append(transaction)

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof) -> int:
        """Simple Proof of Work Algorithm:

        - Find a number p' such that hash(pp') contains 4 leading 0s
        - p is the pr evious proof, p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    def merkle(self) -> str:
        """Calculates Merkle root hash

        :param: None
        :return: <str> Merkle root
        """
        if not self.current_transactions:
            raise TransactionMinimumLengthError

        hashes = [self.hash(t) for t in self.current_transactions]
        hashes.sort()
        while len(hashes) > 1:
            temp = []
            if len(hashes) % 2 == 1:
                hashes += [hashes[-1]]
            for i in range(0, len(hashes), 2):
                temp.append(
                    self.hash(
                        (hashes[i] + hashes[i + 1]).encode()
                    ))
            hashes = temp

        return hashes[0]

    @staticmethod
    def valid_proof(last_proof, proof) -> bool:
        """Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(input):
        """Creates a SHA-256 hash of a block

        :param block: <dict> Block
        :return: <str>
        """
        if isinstance(input, dict):
            string = json.dumps(input, sort_keys=True).encode()
        else:
            string = input
        return hashlib.sha256(
                hashlib
                .sha256(string)
                .hexdigest()
                .encode()
            ).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
