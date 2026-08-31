CREATE DATABASE expense_tracker;

USE expense_tracker;

CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE expenses(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    amount DECIMAL(10,2),
    category VARCHAR(100),
    expense_date DATE,
    notes TEXT
);

CREATE TABLE budgets(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    month VARCHAR(20),
    budget_amount DECIMAL(10,2)
);

USE expense_tracker;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);