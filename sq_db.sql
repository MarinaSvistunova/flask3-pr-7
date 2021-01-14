CREATE TABLE IF NOT EXISTS reviews (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL,
  email text NOT NULL,
  review text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id integer PRIMARY KEY AUTOINCREMENT,
  name text NOT NULL,
  email text NOT NULL,
  psw text NOT NULL,
  time integer NOT NULL
);
