import sqlite3

class DBConnectionService:

    def __init__(self):
        self.conn = sqlite3.connect("analyzer.db")

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnectionService, cls).__new__(cls)
        return cls.instance

    @property
    def connection(self):
        return self.conn

    @connection.setter
    def connection(self, conn):
        self.conn = conn

    @connection.deleter
    def connection(self):
        print("CLOSE DATABASE CONNECTION")
        self.conn.close()




