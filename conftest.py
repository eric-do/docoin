import os
from dotenv import load_dotenv
import pytest
import json
from nacl.public import PrivateKey
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder
from time import time
from docoin import blockchain
from docoin.blockchain import Blockchain

load_dotenv()
bc = Blockchain(
    os.environ.get('PRIVATE_KEY'),
    os.environ.get('PUBLIC_KEY'),
)

private_key = PrivateKey.generate()
private_key_hex = bytes(private_key).hex()
public_key = SigningKey(private_key_hex, encoder=HexEncoder)
public_key_hex = bytes(public_key.verify_key).hex()


@pytest.fixture
def transaction():
    sender = PrivateKey.generate()
    sender_private_key = bytes(sender).hex()
    recipient = PrivateKey.generate()
    signing_key = SigningKey(sender_private_key, encoder=HexEncoder)

    tx = {
        'sender': bytes(signing_key.verify_key).hex(),
        'recipient': bytes(recipient.public_key).hex(),
        'amount': 10,
        'timestamp': int(time())
    }

    tx_bytes = json.dumps(tx, sort_keys=True).encode('ascii')
    signed_hex = signing_key.sign(tx_bytes, encoder=HexEncoder)
    signature_bytes = HexEncoder.decode(signed_hex.signature)
    signed_ascii = HexEncoder.encode(signature_bytes).decode('ascii')

    tx['signature'] = signed_ascii
    return tx


@pytest.fixture
def block():
    last_block = bc.last_block
    last_proof = last_block['proof']
    proof = bc.proof_of_work(last_proof)
    previous_hash = bc.hash(bc.last_block)
    block = {
        'index': len(bc.chain) + 1,
        'timestamp': time(),
        'transactions': bc.current_transactions,
        'proof': proof,
        'previous_hash': previous_hash or bc.hash(bc.chain[-1])
    }
    return block


@pytest.fixture
def invalid_block():
    return {
        'index': len(bc.chain) + 1,
        'timestamp': time(),
        'transactions': bc.current_transactions,
        'proof': 'fake_proof',
        'previous_hash': 'fake_hash'
    }


@pytest.fixture
def blockchain():
    return Blockchain(
        os.environ.get('PRIVATE_KEY'),
        os.environ.get('PUBLIC_KEY'),
    )


@pytest.fixture
def private_key():
    return private_key_hex


@pytest.fixture
def public_key():
    return public_key_hex
