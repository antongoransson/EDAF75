import sqlite3
import os.path
import sys
from data_classes import Customer, RawMaterial

class Database():
    def __init__(self, db_file):
        self.conn, self.c = None, None
        if(os.path.isfile(db_file)):
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
        return [Customer(c, a) for c,a in self.c.execute(query, {'value': "%" + customer + "%"})]

    def insert_customer(self, customer, name):
        query = '''INSERT
                   INTO customers
                   VALUES(?, ?)'''
        self.c.execute(query, (customer, name))
        self.conn.commit()

    def delete_customer(self, customer):
        query = '''DELETE FROM customers
                   WHERE name=:name'''
        self.c.execute(query, {"name": customer})
        self.conn.commit()

    def get_all_recipes(self):
        return [recipe[0] for recipe in self.c.execute('SELECT * FROM recipes')]

    def get_all_raw_materials(self):
        return [RawMaterial(rm, '-', amount) for rm, amount in self.c.execute('SELECT * FROM raw_materials')]

    def get_recipe_items(self, recipe):
        query = '''SELECT raw_material, ri.amount, rm.amount amount_left
                   FROM recipes
                   LEFT JOIN recipe_items AS ri
                   ON (recipes.name = ri.recipe)
                   LEFT JOIN raw_materials as rm
                   USING (raw_material)
                   WHERE name = :name'''
        return [RawMaterial(rm, amount, amount_left) for rm, amount, amount_left in self.c.execute(query, {'name': recipe})]

    def insert_raw_material(self, raw_material, amount):
        query = '''INSERT
                   INTO raw_materials
                   VALUES(?, ?)'''
        self.c.execute(query, (raw_material, amount))
        self.conn.commit()

    def delete_raw_material(self, raw_material):
        query = '''DELETE FROM raw_materials
                   WHERE raw_material=:raw_material'''
        self.c.execute(query, {"raw_material": raw_material})
        self.conn.commit()

    def update_raw_material(self, raw_material, amount):
        query = '''UPDATE raw_materials
                   SET amount =:amount
                   WHERE raw_material=:raw_material'''
        self.c.execute(query, {"raw_material": raw_material, "amount": amount})
        self.conn.commit()

    def get_raw_materials(self, raw_material, column='raw_material'):
        query = '''SELECT * FROM raw_materials
                    WHERE {column} like :value'''.format(column=column)
        return [RawMaterial(rm, amount, '-') for rm, amount in self.c.execute(query, {'value': "%" + raw_material + "%"})]
