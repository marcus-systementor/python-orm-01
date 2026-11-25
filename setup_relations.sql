-- A separate, small relation lab. Existing course_storage is not changed.
CREATE DATABASE IF NOT EXISTS orm_relations_lab
    CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE orm_relations_lab;
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    description VARCHAR(100) NOT NULL,
    CONSTRAINT fk_orm_orders_customer FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
) ENGINE=InnoDB;
INSERT INTO customers SELECT 1, 'Ada' WHERE NOT EXISTS
    (SELECT 1 FROM customers WHERE customer_id = 1);
INSERT INTO customers SELECT 2, 'Sam' WHERE NOT EXISTS
    (SELECT 1 FROM customers WHERE customer_id = 2);
INSERT INTO customers SELECT 3, 'Liv' WHERE NOT EXISTS
    (SELECT 1 FROM customers WHERE customer_id = 3);
INSERT INTO orders SELECT 11, 1, 'Tangentbord' WHERE NOT EXISTS
    (SELECT 1 FROM orders WHERE order_id = 11);
INSERT INTO orders SELECT 12, 1, 'Mus' WHERE NOT EXISTS
    (SELECT 1 FROM orders WHERE order_id = 12);
INSERT INTO orders SELECT 13, 2, 'Skärm' WHERE NOT EXISTS
    (SELECT 1 FROM orders WHERE order_id = 13);
SELECT customer_id, name FROM customers ORDER BY customer_id;
SELECT order_id, customer_id, description FROM orders ORDER BY order_id;
