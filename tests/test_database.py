import hashlib
import datetime
import random


def test_successful_database_connection(session):
    cur = session.conn.cursor()
    cur.execute('SELECT 1 + 1 AS solution')
    assert cur.fetchone()[0] == 2


def test_insert_utxo_to_database(utxo_model, db_cleanup):
    utxo = {
        "address": hashlib.sha256("address".encode()).hexdigest(),
        "tx_hash": hashlib.sha256("hash".encode()).hexdigest(),
        "tx_time": f'{str(datetime.datetime.now())} UTC',
        "script": hashlib.sha256("script".encode()).hexdigest(),
        "value": float("{:.8f}".format(random.randrange(1, 1000000)/100)),
        "spent": random.choice([True, False])
    }
    utxo_model.add_unspent_transaction(utxo)
    rows = utxo_model.get_unspent_transaction_outputs(utxo["address"])

    print(rows)
    assert len(rows) == 1
    assert rows[0]["address"] == utxo["address"]
