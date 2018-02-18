import sqlite3
import os.path
import sys
from data_classes import Customer

class Database():
    def __init__(self, db_file):
        self.conn, self.c = None, None
        if(os.path.exists(db_file)):
            self.conn, self.c = self.connect(db_file)
        else:
            print('Database file does not exist')
            sys.exit(1)

    def connect(self, db_file):
        """ Make connection to an SQLite database file """
        if self.conn is None:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
            return conn, c
        else:
            return self.conn, self.c

    def close(self, conn):
        """ Commit changes and close connection to the database """
        # conn.commit()
        conn.close()

    def get_all_customers(self):
        return [Customer(c, a) for c, a in self.c.execute('SELECT * FROM customers')]

    def get_customers(self, customer, column):
        query = '''SELECT * FROM customers
                    WHERE {column} like :value'''.format(column=column)
        return [Customer(c, a) for c,a in self.c.execute(query, {'value': customer + "%"})]

    def insert_customer(self, customer, name):
        query = 'INSERT INTO customers VALUES(?, ?)'
        self.c.execute(query, (customer, name))
        self.conn.commit()

    def delete_customer(self, customer):
        query = '''DELETE FROM customers
                   WHERE name=:name'''
        self.c.execute(query, {"name": customer})
        self.conn.commit()
