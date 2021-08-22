import json
import hashlib
import datetime
import random
from docoin.transactions import (
    create_transaction,
    verify_transaction,
    get_utxo_for_address,
    get_valid_utxo_for_address_and_amount
)
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey
from nacl.signing import SigningKey
from time import time


def test_create_transaction():
    sender = PrivateKey.generate()
    recipient = PrivateKey.generate()
    keys = ['sender', 'recipient', 'amount', 'timestamp']
    transaction_processed = create_transaction(
        bytes(sender).hex(),
        bytes(sender.public_key).hex(),
        bytes(recipient.public_key).hex(),
        10
    )
    assert all(k in transaction_processed for k in keys) is True


def test_verify_transaction():
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

    assert verify_transaction(tx) is True


def test_get_all_utxo_for_address(utxo_model):
    address = hashlib.sha256("address".encode()).hexdigest()

    def generate_random_utxo():
        return {
            "address": address,
            "tx_hash": hashlib.sha256("hash".encode()).hexdigest(),
            "tx_index": random.randrange(10),
            "tx_time": f'{str(datetime.datetime.now())} UTC',
            "script": hashlib.sha256("script".encode()).hexdigest(),
            "value": float("{:.8f}".format(random.randrange(1, 1000000)/100)),
        }

    utxo_input = [generate_random_utxo() for _ in range(10)]
    for ui in utxo_input:
        utxo_model.add_utxo(ui)
    utxo = get_utxo_for_address(utxo_model, address)
    assert len(utxo) == len(utxo_input)


def test_get_valid_utxo_when_all_are_less_than_or_equal_to_amount(
    utxo_model
):
    address = hashlib.sha256("testvalidutxo".encode()).hexdigest()

    def generate_random_utxo(i):
        return {
            "address": address,
            "tx_hash": hashlib.sha256("hash".encode()).hexdigest(),
            "tx_index": random.randrange(10),
            "tx_time": f'{str(datetime.datetime.now())} UTC',
            "script": hashlib.sha256("script".encode()).hexdigest(),
            "value": i + 1,
        }

    utxo_input = [generate_random_utxo(i) for i in range(10)]
    for ui in utxo_input:
        utxo_model.add_utxo(ui)
    utxo, change = get_valid_utxo_for_address_and_amount(
        utxo_model,
        address,
        11
    )
    assert len(utxo) == 2
    assert change >= 0
