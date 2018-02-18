import sqlite3
from data_classes import Customer
# conn = sqlite3.connect('movies.db')
# c = conn.cursor()
# c.execute('SELECT * FROM movies')
# print (c.fetchone()[0])
# for row in c.execute('SELECT * FROM shows'):
#         print(row)
class Database():
    def __init__(self):
        self.conn, self.c = None, None
        self.conn, self.c = self.connect()

    def connect(self):
        """ Make connection to an SQLite database file """
        if self.conn is None:
            conn = sqlite3.connect('db.db')
            c = conn.cursor()
            return conn, c
        else:
            return self.conn, self.c

    def close(self, conn):
        """ Commit changes and close connection to the database """
        # conn.commit()
        conn.close()

    def get_movies(self):
        return [row[0] for row in self.c.execute('SELECT * FROM movies')]

    def get_movie(self, movie):
        query = 'SELECT * FROM movies WHERE movie_name =:name'
        return [row[0] for row in self.c.execute(query, {"name": movie})]

    def get_customers(self):
        return [Customer(c, a) for c, a in self.c.execute('SELECT * FROM customers')]

    def get_customer(self, customer):
        query = 'SELECT * FROM customers WHERE name =:name'
        return [Customer(c, a) for c,a in self.c.execute(query, {"name": customer})]

    def insert_customer(self, customer, name):
        query = 'INSERT INTO customers VALUES(?, ?)'
        self.c.execute(query, (customer, name))
        self.conn.commit()

    # get_movies()
    # print(get_movie('Dokumentär om Borrby'))
