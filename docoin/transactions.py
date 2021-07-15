from time import time
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError
import json


def create_transaction(
    sender_private_key: str,
    sender_public_key: str,
    recipient_public_key: str,
    amount: int
) -> dict:
    """Creates a new transaction

    :param sender_private_key: <str> private key of sender
    :param sender_public_key: <str> public key of sender
    :param recipient_public_key: <str> public key of recipient
    :param amount: <int> amount sent, in cents
    :return: <dict> our transaction
    """
    transaction = {
        'sender': sender_public_key,
        'recipient': recipient_public_key,
        'amount': amount,
        'timestamp': int(time())
    }

    signing_key = SigningKey(sender_private_key, encoder=HexEncoder)
    transaction_encoded = json.dumps(
        transaction,
        sort_keys=True
    ).encode("ascii")
    signature = signing_key.sign(transaction_encoded).signature
    transaction['signature'] = HexEncoder\
        .encode(signature)\
        .decode('ascii')

    return transaction


def verify_transaction(transaction) -> bool:
    """Verifies a given transaction

    :param transaction: <dict> dictionary representing a transaction
    :return: <bool> True for valid transaction, False if not
    """
    public_key = transaction['sender']
    verify_key = VerifyKey(public_key, encoder=HexEncoder)
    signature = transaction.pop('signature')
    signature_bytes = HexEncoder.decode(signature)
    tx_bytes = json.dumps(transaction, sort_keys=True).encode('ascii')

    try:
        verify_key.verify(tx_bytes, signature_bytes)
        return True
    except BadSignatureError:
        print(BadSignatureError)
        return False
