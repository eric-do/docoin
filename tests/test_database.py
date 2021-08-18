import hashlib
import datetime
import random


def test_successful_database_connection(session):
    cur = session.conn.cursor()
    cur.execute('SELECT 1 + 1 AS solution')
    assert cur.fetchone()[0] == 2


def test_insert_utxo_to_database(utxo_model):
    utxo = {
        "address": hashlib.sha256("address".encode()).hexdigest(),
        "tx_hash": hashlib.sha256("hash".encode()).hexdigest(),
        "tx_time": f'{str(datetime.datetime.now())} UTC',
        "script": hashlib.sha256("script".encode()).hexdigest(),
        "value": float("{:.8f}".format(random.randrange(1, 1000000)/100)),
        "spent": random.choice([True, False])
    }
    utxo_model.add_unspent_transaction(utxo)
    cur = utxo_model.session.conn.cursor()
    print(utxo["address"])
    cur.execute(
        "SELECT * FROM utxo WHERE address = %s", [utxo["address"]]
    )
    print(cur.query)
    rows = cur.fetchall()
    cur.execute(
        "DELETE FROM utxo WHERE address = %s", [utxo["address"]]
    )
    print(cur.query)
    assert len(rows) == 1
