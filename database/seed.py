import psycopg2
import hashlib
import random
import datetime

conn = psycopg2.connect(
    dbname="docoin",
    user="postgres"
)

cur = conn.cursor()


def create_transaction(i):
    output = float("{:.8f}".format(random.randrange(1, 1000000)/100))
    input = output + random.randrange(1000)

    tx = {
        'hash': hashlib.sha256(str(i).encode()).hexdigest(),
        'confirmed': random.choice([True, False]),
        'received_time': f'{str(datetime.datetime.now())} UTC',
        'size': random.randrange(1000),
        'total_inputs': random.randrange(1, 5),
        'total_outputs': random.randrange(1, 5),
        'total_btc_output': output,
        'total_btc_input': input,
        'fees': input - output,
        'transacted_value_usd': float("{:.2f}".format(output / 100))
    }

    return tx


def create_utxo(i, transactions):
    utxo = {
        "address": hashlib.sha256(str(i).encode()).hexdigest(),
        "tx_hash": transactions[random.randrange(1000)]['hash'],
        "tx_time": f'{str(datetime.datetime.now())} UTC',
        "script": hashlib.sha256(str(i+1).encode()).hexdigest(),
        "value": float("{:.8f}".format(random.randrange(1, 1000000)/100)),
        "spent": random.choice([True, False])
    }
    return utxo


transactions = [create_transaction(i) for i in range(1000)]
utxo = [create_utxo(i, transactions) for i in range(10000)]

for tx in transactions:
    cur.execute(
        'INSERT INTO transactions VALUES (%s, %s, %s, %s, %s,\
            %s, %s, %s, %s, %s)',
        list(tx.values())
    )

for utx in utxo:
    cur.execute(
        'INSERT INTO utxo (address, tx_hash, tx_time, script, value, spent)\
         VALUES (%s, %s, %s, %s, %s, %s)',
        list(utx.values())
    )

conn.commit()
cur.close()
conn.close()
