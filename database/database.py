import psycopg2
from loguru import logger


class Database:
    """PSQL DB class

    This class is meant to connect to a Postgres DB.
    Its intended to be generic
    """

    def __init__(self, config):
        self.username = config.DATABASE_USERNAME
        self.dbname = config.DATABASE_NAME
        self.conn = None

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.username
                )
            except psycopg2.DatabaseError as e:
                logger.error(e)
                raise e
            finally:
                logger.info('Successfully connected to DB')

    def select_rows(self, query):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query)
            records = [row for row in cur.fetchall()]
        return records

    def update_rows(self, query, params):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            self.conn.commit()
        return f"{cur.rowcount} rows affected."


class UTXO:
    """UTXO class for handling unspent transactions
    """

    def __init__(self, session: Database):
        self.session = session

    def add_unspent_transaction(self, utxo):
        query = 'INSERT INTO utxo (address, tx_hash, \
                                   tx_time, script, \
                                   value, spent) \
                 VALUES (%s, %s, %s, %s, %s, %s)'
        params = (
            utxo["address"], utxo["tx_hash"], utxo["tx_time"],
            utxo["script"], utxo["value"], utxo["spent"]
        )
        message = self.session.update_rows(query, params)
        print(message)

    def get_unspent_transaction_outputs(self, address):
        query = "SELECT * FROM utxo \
                 WHERE address = '{}' \
                 AND spent = FALSE \
                 ORDER BY amount"
        utxo = self.session.select_rows(query.format(address))
        return utxo

    def get_unspent_transaction_outputs(self, address):
        txo = self.get_transaction_outputs(address)
