DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS alarm;
DROP TABLE IF EXISTS coordinate;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE alarm (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  armed INTEGER DEFAULT 0,
  alarm_triggered INTEGER DEFAULT 0
);

CREATE TABLE coordinate (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  acX INTEGER, -- Acceleration along X axis
  acY INTEGER, -- Acceleration along Y axis
  acZ INTEGER, -- Acceleration along Z axis
  gyX INTEGER, -- Rotation around X axis
  gyY INTEGER, -- Rotation around Y axis
  gyZ INTEGER, -- Rotation around Z axis
  tmp INTEGER, -- Temperature °C
  alarm_id INTEGER NOT NULL,
  FOREIGN KEY (alarm_id) REFERENCES alarm (id)
);