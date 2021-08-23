import hashlib
import datetime
import random


def test_successful_database_connection(session):
    cur = session.conn.cursor()
    cur.execute('SELECT 1 + 1 AS solution')
    assert cur.fetchone()[0] == 2


def test_insert_utxo_to_database(utxo_model):
    utxo = {
        "address": hashlib.sha256(
            "test_insert_utxo_to_database".encode()
        ).hexdigest(),
        "tx_hash": hashlib.sha256("hash".encode()).hexdigest(),
        "tx_index": random.randrange(10),
        "tx_time": f'{str(datetime.datetime.now())} UTC',
        "script": hashlib.sha256("script".encode()).hexdigest(),
        "value": float("{:.8f}".format(random.randrange(1, 1000000)/100)),
    }
    utxo_model.add_utxo(utxo)
    rows = utxo_model.get_all_utxo_for_address(utxo["address"])

    assert len(rows) == 1
    assert rows[0]["address"] == utxo["address"]


def test_spend_transaction(utxo_model):
    utxo = {
        "address": hashlib.sha256(
            "test_spend_transaction".encode()
        ).hexdigest(),
        "tx_hash": hashlib.sha256("hash".encode()).hexdigest(),
        "tx_index": random.randrange(10),
        "tx_time": f'{str(datetime.datetime.now())} UTC',
        "script": hashlib.sha256("script".encode()).hexdigest(),
        "value": float("{:.8f}".format(random.randrange(1, 1000000)/100)),
    }
    utxo_model.add_utxo(utxo)
    utxo_model.spend_utxo(utxo["tx_hash"], utxo["tx_index"])
    rows = utxo_model.get_all_utxo_for_address(utxo["tx_hash"])
    assert len(rows) == 0
