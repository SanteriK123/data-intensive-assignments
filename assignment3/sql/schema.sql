DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS classroom;
DROP TABLE IF EXISTS book;

CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE course (
    id INTEGER PRIMARY KEY,
    name TEXT,
    credits INTEGER
);

CREATE TABLE professor (
    id INTEGER PRIMARY_KEY,
    name TEXT,
    department TEXT
);

CREATE TABLE classroom (
    id INTEGER PRIMARY KEY,
    building TEXT,
    room TEXT
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT
);
