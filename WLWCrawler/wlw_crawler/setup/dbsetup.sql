
CREATE DATABASE wlw WITH ENCODING 'UTF-8';

CREATE TABLE wlw (
    id serial PRIMARY KEY NOT NULL, 
    company TEXT, address TEXT, email TEXT, fax TEXT, phone TEXT, website TEXT
    );
  
CREATE TABLE suffix (
    id serial PRIMARY KEY NOT NULL,
    suffix INT,
    crawled BOOLEAN DEFAULT FALSE
    );