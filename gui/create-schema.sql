-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS raw_materials;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS recipe_items;
-- DROP TABLE IF EXISTS pallets;
-- DROP TABLE IF EXISTS shows;
-- DROP TABLE IF EXISTS reservations;
PRAGMA foreign_keys=ON;

-- Create the tables.
CREATE TABLE customers (
  name TEXT,
  address TEXT NOT NULL,
  PRIMARY KEY(name)
);

CREATE TABLE raw_materials (
  raw_material TEXT,
  amount INT not NULL,
  PRIMARY KEY(raw_material)
);

CREATE TABLE recipes (
  name TEXT,
  PRIMARY KEY(name)
);

CREATE TABLE recipe_items (
  id INTEGER,
  recipe TEXT NOT NULL,
  raw_material TEXT NOT NULL,
  amount INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(recipe) REFERENCES recipes(name),
  FOREIGN KEY(raw_material) REFERENCES raw_materials(raw_material),
  FOREIGN KEY(amount) REFERENCES raw_materials(amount)
);
