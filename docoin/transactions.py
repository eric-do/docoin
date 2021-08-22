from time import time
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError
import json

from database.database import UTXO


class Transaction:
    """Transaction class

    The transaction class is responsible for
    - Creating a transaction, given inputs
    - Validating inputs
    - Adding UTXO to UTXO DB???

    Attributes:
      inputs: UTXO inputs for the transaction
      outputs: UTXO outputs for the transaction
      fees: fees for the transaction
    """
    def __init__(
        inputs: list[str],

    ):
        pass


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


def get_utxo_for_address(
    UTXO_DB: UTXO,
    address: str
):
    """Gets utxo for a given address

    :param amount: <float> requested number of docoin
    :param address: <str> address to search by
    :return: <list[(string, int)]> list of tuples containing:
       - transaction hash
       - utxo index within transaction
    """
    utxo = UTXO_DB.get_all_utxo_for_address(address)
    return utxo


def get_utxo_from_smaller_amounts(utxo, minimum, sorted=False):
    """Gets a list of utxo that will sum to the minimum amount.
    All utxo in the list should be less than the minimum amount.

    :param amount: <list[utxo]> a list of utxo
    :param minimum: <float> minimum amount for desired total
    :param sorted: <bool> flag for whether provided utxo list is sorted
    :return: <tuple(list[dict], change)> tuple of valid utxo and change
    """
    total = 0
    result = []
    if not sorted:
        utxo = sorted(
            utxo,
            key=lambda u: u["value"],
            reverse=True
        )
    for u in utxo:
        result.append(u)
        total += u["value"]
        if total >= minimum:
            change = total - minimum
            return result, change
    return None, 0


def get_utxo_from_larger_amounts(utxo, minimum, sorted=False):
    """Gets a list of utxo that will sum to the minimum amount
    All utxo in the list should be greater than the minimum amount.

    :param amount: <list[utxo]> a list of utxo
    :param minimum: <float> minimum amount for desired total
    :param sorted: <bool> flag for whether provided utxo list is sorted
    :return: <tuple(list[dict], change)> tuple of valid utxo and change
    """
    if not sorted:
        utxo = sorted(utxo, key=lambda u: u["value"])
    change = utxo[0]["value"] - minimum
    return [utxo[0]], change


def get_valid_utxo_for_address_and_amount(
    UTXO_DB: UTXO,
    address: str,
    amount: float
):
    """Gets the smallest number of utxo given requested amount

    :param amount: <float> requested number of docoin
    :param address: <str> address to search by
    :return: <tuple(list[dict], change)> tuple of valid utxo and change
    """
    sorted_unspent = UTXO_DB.get_all_utxo_for_address(address)
    greaters = [utxo for utxo in sorted_unspent if utxo["value"] >= amount]
    lessers = [utxo for utxo in sorted_unspent if utxo["value"] < amount]
    if greaters:
        return get_utxo_from_larger_amounts(greaters, amount, True)
    return get_utxo_from_smaller_amounts(list(reversed(lessers)), amount, True)
