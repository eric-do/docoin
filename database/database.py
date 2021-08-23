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
            self.conn.commit()
        return f"{cur.rowcount} rows affected."


class UTXO:
    """UTXO class for handling unspent transactions

    Attributes
      session: an instance of the DB connection class
    """

    def __init__(self, session: Database):
        self.session = session

    def add_utxo(self, utxo):
        """Method for adding utxo to the DB
        :param utxo: <list[utxo]> list of utxo objects to insert
        """
        query = 'INSERT INTO utxo (address, tx_hash, tx_index, \
                                   tx_time, script, value) \
                 VALUES (%s, %s, %s, %s, %s, %s)'
        params = (
            utxo["address"], utxo["tx_hash"], utxo["tx_index"],
            utxo["tx_time"], utxo["script"], utxo["value"]
        )
        message = self.session.update_rows(query, params)
        print(message)

    def get_all_utxo_for_address(self, address):
        """Method for querying utxo from the DB given an address
        :param address: <str> encrypted address to query by
        """
        query = "SELECT * FROM utxo \
                 WHERE address = %s \
                 ORDER BY value"
        utxo = self.session.select_rows(query, [address])
        return utxo

    def spend_utxo(self, tx_hash, tx_index):
        """Method "spending" utxo

        This method actually deletes utxo from the DB, but in terms
        of business logic, a utxo is deleted when it is spent.
        :param tx_hash: <str> transaction identifier
        """
        query = "DELETE FROM utxo \
                 WHERE tx_hash = %s \
                 AND tx_index = %s"
        message = self.session.update_rows(query, [tx_hash, tx_index])
        print(message)
