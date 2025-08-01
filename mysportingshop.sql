/********************************************************
* This script creates the database named my_sporting_shop 
*********************************************************/
DROP DATABASE IF EXISTS my_sporting_shop;
CREATE DATABASE my_sporting_shop;
USE my_sporting_shop;

CREATE TABLE categories (
  category_id        INT PRIMARY KEY AUTO_INCREMENT,
  category_name      VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE products (
  product_id         INT PRIMARY KEY AUTO_INCREMENT,
  category_id        INT NOT NULL,
  product_code       VARCHAR(10) NOT NULL UNIQUE,
  product_name       VARCHAR(255) NOT NULL,
  description        TEXT default NULL,
  list_price         DECIMAL(10,2) NOT NULL,
  inventory          INT NOT NULL, 
  discount_percent   DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  date_added         DATETIME DEFAULT NULL,
  FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

CREATE TABLE vendors (
  vendor_id     INT PRIMARY KEY AUTO_INCREMENT,
  product_id    INT NOT NULL,
  vendor_name   VARCHAR(255) NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE TABLE customers (
  customer_id         INT PRIMARY KEY AUTO_INCREMENT,
  email_address       VARCHAR(255) NOT NULL UNIQUE,
  password            VARCHAR(60) NOT NULL,
  first_name          VARCHAR(60) NOT NULL,
  last_name           VARCHAR(60) NOT NULL,
  shipping_address_id INT DEFAULT NULL,
  billing_address_id  INT DEFAULT NULL
);

CREATE TABLE addresses (
  address_id     INT PRIMARY KEY AUTO_INCREMENT,
  customer_id    INT NOT NULL,
  line1          VARCHAR(60) NOT NULL,
  line2          VARCHAR(60) DEFAULT NULL,
  city           VARCHAR(40) NOT NULL,
  state          VARCHAR(2) NOT NULL,
  zip_code       VARCHAR(10) NOT NULL,
  phone          VARCHAR(12) NOT NULL,
  disabled       TINYINT(1) NOT NULL DEFAULT 0,
  FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE orders (
  order_id           INT PRIMARY KEY AUTO_INCREMENT,
  customer_id        INT NOT NULL,
  order_date         DATETIME NOT NULL,
  ship_amount        DECIMAL(10,2) NOT NULL,
  ship_date          DATETIME DEFAULT NULL,
  ship_address_id    INT NOT NULL,
  card_number        CHAR(16) NOT NULL,
  billing_address_id INT NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

CREATE TABLE order_items (
  item_id          INT PRIMARY KEY AUTO_INCREMENT,
  order_id         INT NOT NULL,
  product_id       INT NOT NULL,
  item_price       DECIMAL(10,2) NOT NULL,
  discount_amount  DECIMAL(10,2) NOT NULL,
  quantity         INT NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders (order_id),
  FOREIGN KEY (product_id) REFERENCES products (product_id)
);

CREATE TABLE administrators (
  admin_id       INT PRIMARY KEY AUTO_INCREMENT,
  email_address  VARCHAR(255) NOT NULL,
  password       VARCHAR(255) NOT NULL,
  first_name     VARCHAR(255) NOT NULL,
  last_name      VARCHAR(255) NOT NULL
);

CREATE TABLE cookies (
cookie_id int PRIMARY KEY AUTO_INCREMENT,
admin_id int NOT NULL,
cookie varchar(255) NOT null,
expire_at DATETIME not null,
foreign key (admin_id) references administrators (admin_id)
);

-- Insert data
INSERT INTO categories (category_name) VALUES
('Soccer'), ('Football'), ('Basketball'), ('Baseball'), ('Hockey');

INSERT INTO products (category_id, product_code, product_name, description, list_price, inventory, discount_percent, date_added) VALUES
(1, 'sb', 'Soccer ball', 'NEW SOCCER BALL', 25.00, 5, 0.00, '2025-07-17 09:32:40'),
(2, 'fb', 'Football', 'NEW FOOTBALL', 20.00, 5, 0.00, '2025-07-17 16:33:13'),
(3, 'bb', 'Basketball', 'NEW BASKETBALL', 25.00, 5, 5.00, '2025-07-17 11:04:31'),
(4, 'baseb', 'Baseball', 'NEW BASEBALL', 7.99, 5, 0.00, '2025-07-17 11:12:59'),
(5, 'hp', 'Hockey Puck', 'NEW HOCKEY PUCK', 10.00, 5, 0.00, '2025-07-17 13:58:35');

INSERT INTO customers (email_address, password, first_name, last_name, shipping_address_id, billing_address_id) VALUES
('allan.sherwood@yahoo.com', '1234', 'Allan', 'Sherwood', 1, 2),
('barryz@gmail.com', 'ABCD', 'Barry', 'Zimmer', 3, 3),
('christineb@solarone.com', 'ZYXW', 'Christine', 'Brown', 4, 4),
('david.goldstein@hotmail.com', '9876', 'David', 'Goldstein', 5, 6);

INSERT INTO addresses (customer_id, line1, line2, city, state, zip_code, phone, disabled) VALUES
(1, '100 East Ridgewood Ave.', '', 'Paramus', 'NJ', '07652', '201-653-4472', 0),
(1, '21 Rosewood Rd.', '', 'Woodcliff Lake', 'NJ', '07677', '201-653-4472', 0),
(2, '16285 Wendell St.', '', 'Omaha', 'NE', '68135', '402-896-2576', 0),
(3, '19270 NW Cornell Rd.', '', 'Beaverton', 'OR', '97006', '503-654-1291', 0),
(4, '186 Vermont St.', 'Apt. 2', 'San Francisco', 'CA', '94110', '415-292-6651', 0),
(4, '1374 46th Ave.', '', 'San Francisco', 'CA', '94129', '415-292-6651', 0);

INSERT INTO orders (customer_id, order_date, ship_amount, ship_date, ship_address_id, card_number, billing_address_id) VALUES
(1, '2018-03-28 09:40:28', 5.00, '2018-03-30 15:32:51', 1, '4111111111111111', 2),
(2, '2018-03-28 11:23:20', 5.00, '2018-03-29 12:52:14', 3, '4012888888881881', 3),
(1, '2018-03-29 09:44:58', 10.00, '2018-03-31 09:11:41', 1, '4111111111111111', 2),
(3, '2018-03-30 15:22:31', 5.00, '2018-04-03 16:32:21', 4, '378282246310005', 4),
(4, '2018-03-31 05:43:11', 5.00, '2018-04-02 14:21:12', 5, '4111111111111111', 6);

INSERT INTO order_items (order_id, product_id, item_price, discount_amount, quantity) VALUES
(1, 2, 1199.00, 359.70, 1),
(2, 4, 489.99, 186.20, 1),
(3, 3, 2517.00, 1308.84, 1),
(4, 2, 1199.00, 359.70, 2),
(5, 5, 299.00, 0.00, 1);

INSERT INTO administrators (email_address, password, first_name, last_name) VALUES
('admin@mysportingshop.com', '1234', 'Admin', 'User'),
('joel@murach.com', '12345', 'Joel', 'Murach'),
('mike@murach.com', '123456', 'Mike', 'Murach');

-- Manage user creation
DROP USER IF EXISTS 'mgs_user'@'localhost';
CREATE USER 'mgs_user'@'localhost' IDENTIFIED BY 'pa55word';
GRANT SELECT, INSERT, UPDATE, DELETE, DROP, CREATE VIEW, EXECUTE ON my_sporting_shop.* to mgs_user@localhost;
