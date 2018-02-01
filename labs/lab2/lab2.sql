-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS shows;
DROP TABLE IF EXISTS reservations;
PRAGMA foreign_keys=ON;

-- Create the tables.
CREATE TABLE users (
  username TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  address TEXT,
  phone_number TEXT
);

CREATE TABLE theaters (
  theater_name TEXT PRIMARY KEY,
  seats INT
);

CREATE TABLE movies (
  movie_name TEXT PRIMARY KEY
);

CREATE TABLE shows (
  movie_name TEXT,
  theater_name TEXT,
  show_date DATE,
  PRIMARY KEY(movie_name, show_date),
  FOREIGN KEY(movie_name) REFERENCES movies(movie_name),
  FOREIGN KEY(theater_name) REFERENCES theaters(theater_name)
);

CREATE TABLE reservations (
  res_nbr INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  movie_name TEXT,
  theater_name TEXT,
  show_date DATE,
  FOREIGN KEY(username) REFERENCES users(username),
  FOREIGN KEY(movie_name, show_date) REFERENCES shows(movie_name, show_date)
  FOREIGN KEY(movie_name) REFERENCES movies(movie_name),
  FOREIGN KEY(theater_name) REFERENCES theaters(theater_name)
);


-- Insert data into the tables.
INSERT
INTO    users (username, name, address, phone_number)
VALUES  ("Emma", "Emma EMma", "Malmö", "0202194213" ),
        ("An2n", "ANton anton", "BorrbyTown", "090124213"),
        ("Nooriz", "Nora TOra", "STUREP", "06212194213"),
        ("Hanna", "Hanna panna", "STUREP2", "75912194212");


INSERT
INTO    movies (movie_name)
VALUES  ("Dokumentär om Borrby"), ("Rädda valarna"), ("Vi räddade valarna"),
        ("Valarna har nu tagit över"),  ("Hoppla pålle"),
        ("HOPPLA SNABBARE HÄSTJÄVEL"), ("Folk spenderar för mycket tid på youtube");

INSERT
INTO    theaters (theater_name, seats)
VALUES  ("BorrbyBion", 5), ("Royal Malmö", 7), ("IMAX Ystad", 3),
        ("HemmaBio StureP", 2);

INSERT
INTO    shows (movie_name, theater_name, show_date)
VALUES  ("Rädda valarna", "BorrbyBion", "2017-01-28"),
        ("Rädda valarna", "Royal Malmö", "2017-01-29"),
        ("Rädda valarna", "IMAX Ystad", "2017-01-30"),
        ("Rädda valarna", "BorrbyBion", "2017-01-31"),
        ("Rädda valarna", "HemmaBio StureP", "2017-01-26"),
        ("Hoppla pålle", "Royal Malmö", "2017-01-26"),
        ("Hoppla pålle", "IMAX Ystad", "2017-01-27"),
        ("Hoppla pålle", "Royal Malmö", "2017-01-28"),
        ("Hoppla pålle", "IMAX Ystad", "2017-01-29"),
        ("Hoppla pålle", "Royal Malmö", "2017-02-02"),
        ("Hoppla pålle", "IMAX Ystad", "2017-01-30"),
        ("Vi räddade valarna", "HemmaBio StureP", "2017-01-26"),
        ("Vi räddade valarna", "Royal Malmö", "2017-01-28"),
        ("Vi räddade valarna", "IMAX Ystad", "2017-01-30"),
        ("Vi räddade valarna", "Royal Malmö", "2017-03-27"),
        ("Vi räddade valarna", "IMAX Ystad", "2017-01-27"),
        ("HOPPLA SNABBARE HÄSTJÄVEL", "Royal Malmö", "2017-01-28"),
        ("HOPPLA SNABBARE HÄSTJÄVEL", "IMAX Ystad", "2017-01-30"),
        ("HOPPLA SNABBARE HÄSTJÄVEL", "Royal Malmö", "2017-03-27"),
        ("HOPPLA SNABBARE HÄSTJÄVEL", "IMAX Ystad", "2017-01-27"),
        ("Dokumentär om Borrby", "BorrbyBion", "2017-01-28"),
        ("Dokumentär om Borrby", "Royal Malmö", "2017-01-26"),
        ("Dokumentär om Borrby", "IMAX Ystad", "2017-01-30"),
        ("Dokumentär om Borrby", "BorrbyBion", "2017-01-31"),
        ("Dokumentär om Borrby", "HemmaBio StureP", "2017-02-26");

INSERT
INTO    reservations (username, theater_name, movie_name, show_date)
VALUES  ("Emma", "HemmaBio StureP", "Rädda valarna", "2017-01-26"),
        ("An2n", "Royal Malmö", "Dokumentär om Borrby", "2017-01-26"),
        ("An2n", "Royal Malmö", "Dokumentär om Borrby", "2017-01-26"),
        ("An2n", "Royal Malmö", "Dokumentär om Borrby", "2017-01-26"),
        ("An2n", "Royal Malmö", "Dokumentär om Borrby", "2017-01-26");
