CREATE DATABASE IF NOT EXISTS course_storage;
USE course_storage;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

INSERT INTO customers (customer_id, name)
SELECT 1, 'Ada'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = 1);

INSERT INTO customers (customer_id, name)
SELECT 2, 'Sam'
WHERE NOT EXISTS (SELECT 1 FROM customers WHERE customer_id = 2);

SELECT customer_id, name FROM customers ORDER BY customer_id;
