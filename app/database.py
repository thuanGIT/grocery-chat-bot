
from __future__ import annotations
import os
import psycopg2 as pgsql
from app.error import SQLException
from app.utilities.logs import Log


# Get credentials for posgres
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME")

class Database: 
    """Wrapper class to connect to the database (POSTGRESQL).
    """

    # Static field to hold the singly-defined instance
    __cached = dict()

    # Log TAG
    __TAG = __name__

    @staticmethod
    def instance(session_id) -> Database:
        return Database.__cached.setdefault(session_id, Database(session_id=session_id))
        
    def __init__(self, session_id):
        self.session_id = session_id
        self.conn = None

    def connect(self):
        """Connect to the database.
        """
        # Get configurations
        config = self.get_config()
        # Connect
        self.conn = pgsql.connect(**config)
        Log.i(Database.__TAG, f"Connection #{self.session_id} initialized.")

    def close(self):
        """Close the connection to the database.
        """
        self.conn.close()
        self.conn = None
        Log.i(Database.__TAG, f"Connection #{self.session_id} closed.")
    
    def execute(self, sql_string):
        """Execute an SQL statement.

        Args:
            sql_string (str): SQL statement to execute

        Raises:
            SQLException: _description_

        Returns:
            Cursor: _description_
        """
        if self.conn:
            # Get a cursor
            cursor = self.conn.cursor()
            # Execute a query and converting to a set
            cursor.execute(sql_string)
            result = self.from_result_to_tuples(cursor=cursor)
            # Close the cursor
            cursor.close()
            Log.i(Database.__TAG, f"Query execution succeeded!")
            return result
        else:
            raise SQLException("Connection is not initalized!")
    
    def get_config(self) -> dict:
        """Get the configuratin for database connection.

        Returns:
            dict: The configurations in dictionary.
        """
        config = {
            "database": POSTGRES_DB, 
            "user": POSTGRES_USER, 
            "password": POSTGRES_PASSWORD, 
            "host": POSTGRES_HOSTNAME,
        }
        return config

    def from_result_to_tuples(self, cursor):
        """Get all result tuples from the cursor into a set.

        Args:
            cursor (cursor): The cursor executing the query.

        Returns:
            set: Set of all tuples
        """
        tuples_l = set()
        for row in cursor:
            tuples_l.add(row)
        return tuples_l