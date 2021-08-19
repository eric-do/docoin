import psycopg2
import psycopg2.extras
from loguru import logger


class Database:
    """PSQL DB class

    This class is meant to connect to a Postgres DB.
    Its intended to be generic

    Methods
    - connect: establish connection to DB if none exists
    - select_rows: method for querying rows
    - update_rows: method for updating rows
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

    def select_rows(self, query, params):
        self.connect()
        with self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cur:
            cur.execute(query, params)
            records = cur.fetchall()
        return records

    def update_rows(self, query, params):
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            print(cur.query)
            self.conn.commit()
        return f"{cur.rowcount} rows affected."


class UTXO:
    """UTXO class for handling unspent transactions

    """

    def __init__(self, session: Database):
        self.session = session

    def add_utxo(self, utxo):
        query = 'INSERT INTO utxo (address, tx_hash, tx_index, \
                                   tx_time, script, value) \
                 VALUES (%s, %s, %s, %s, %s, %s)'
        print(utxo)
        params = (
            utxo["address"], utxo["tx_hash"], utxo["tx_index"],
            utxo["tx_time"], utxo["script"], utxo["value"]
        )
        message = self.session.update_rows(query, params)
        print(message)

    def get_utxo(self, address):
        query = "SELECT * FROM utxo \
                 WHERE address = %s \
                 ORDER BY value"
        utxo = self.session.select_rows(query, [address])
        return utxo

    def spend_utxo(self, address, tx_index):
        query = "DELETE FROM utxo \
                 WHERE address = %s \
                 AND tx_index = %s"
        message = self.session.update_rows(query, [address, tx_index])
        print(message)
