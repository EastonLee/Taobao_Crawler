CREATE SCHEMA `scrapy` ;

DROP TABLE IF EXISTS website;
CREATE TABLE website (
  guid CHAR(32) PRIMARY KEY,
  name TEXT,
  description TEXT,
  url TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS brands;
CREATE TABLE brands (
  guid CHAR(32) PRIMARY KEY,
  name TEXT,
  url TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS models;
CREATE TABLE models (
  guid CHAR(32) PRIMARY KEY,
  brand TEXT,
  model TEXT,
  no_of_seller INTEGER ,
  price FLOAT ,
  power TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;

