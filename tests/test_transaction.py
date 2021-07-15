from docoin.transactions import create_transaction, verify_transaction
from nacl.encoding import HexEncoder
from nacl.public import PrivateKey
from nacl.signing import SigningKey, VerifyKey
from time import time
import json


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
