import psycopg
from typing import Optional


class DB:
    def __init__(self):
        self.conn: Optional[psycopg.Connection] = None

    def new_connection(self, _connection_string: str) -> None:
        if not self.conn or self.conn.closed:
            self.conn = psycopg.connect(_connection_string)
            print("Database connection stabilished.")

    def disconnect(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("Database connection closed.")
