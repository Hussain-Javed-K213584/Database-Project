-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2023-11-30 03:51:20.749

-- tables
-- Table: Accessories
CREATE TABLE Accessories (
    A_id integer NOT NULL CONSTRAINT Accessories_pk PRIMARY KEY,
    Name varchar(100) NOT NULL,
    price integer NOT NULL,
    Qty integer NOT NULL,
    Type varchar(100) NOT NULL,
    Product_table_P_id integer NOT NULL,
    CONSTRAINT Accessories_Product_table FOREIGN KEY (Product_table_P_id)
    REFERENCES Product_table (P_id)
);

-- Table: Admin
CREATE TABLE Admin (
    Password varchar(100) NOT NULL,
    username varchar(100) NOT NULL,
    A_id integer NOT NULL CONSTRAINT Admin_pk PRIMARY KEY,
    name varchar(100) NOT NULL
);

-- Table: Jeans
CREATE TABLE Jeans (
    Gender character(1) NOT NULL,
    Type varchar(50) NOT NULL,
    name varchar(100) NOT NULL,
    price integer NOT NULL,
    J_id integer NOT NULL CONSTRAINT Jeans_pk PRIMARY KEY,
    Qty integer NOT NULL,
    Product_table_P_id integer NOT NULL,
    CONSTRAINT Jeans_Product_table FOREIGN KEY (Product_table_P_id)
    REFERENCES Product_table (P_id)
);

-- Table: Orders
CREATE TABLE Orders (
    O_id integer NOT NULL CONSTRAINT Orders_pk PRIMARY KEY,
    Total_price integer NOT NULL,
    name varchar(100) NOT NULL,
    timestamp datetime NOT NULL,
    Users_U_id integer NOT NULL,
    CONSTRAINT Orders_Users FOREIGN KEY (Users_U_id)
    REFERENCES Users (U_id)
);

-- Table: Product_table
CREATE TABLE Product_table (
    P_id integer NOT NULL CONSTRAINT P_id PRIMARY KEY,
    name varchar(100) NOT NULL,
    price integer NOT NULL
);

-- Table: Shoes
CREATE TABLE Shoes (
    S_id integer NOT NULL CONSTRAINT Shoes_pk PRIMARY KEY,
    name varchar(100) NOT NULL,
    type character(1) NOT NULL,
    Qty integer NOT NULL,
    Price integer NOT NULL,
    Product_table_P_id integer NOT NULL,
    CONSTRAINT Shoes_Product_table FOREIGN KEY (Product_table_P_id)
    REFERENCES Product_table (P_id)
);

-- Table: Tshirts
CREATE TABLE Tshirts (
    T_id integer NOT NULL CONSTRAINT Tshirts_pk PRIMARY KEY,
    name varchar(100) NOT NULL,
    Price integer NOT NULL,
    Gender character(1) NOT NULL,
    Product_table_P_id integer NOT NULL,
    CONSTRAINT Tshirts_Product_table FOREIGN KEY (Product_table_P_id)
    REFERENCES Product_table (P_id)
);

-- Table: Users
CREATE TABLE Users (
    U_id integer NOT NULL CONSTRAINT Users_pk PRIMARY KEY,
    email varchar(100) NOT NULL,
    Phone_no integer NOT NULL,
    Nmae varchar(100) NOT NULL,
    location varchar(100) NOT NULL,
    password varchar(50) NOT NULL
);

-- Table: order_details
CREATE TABLE order_details (
    OD_id integer NOT NULL CONSTRAINT order_details_pk PRIMARY KEY,
    Qty integer NOT NULL,
    Name varchar(100) NOT NULL,
    Total_p integer NOT NULL,
    Orders_O_id integer NOT NULL,
    Product_table_P_id integer NOT NULL,
    CONSTRAINT order_details_Orders FOREIGN KEY (Orders_O_id)
    REFERENCES Orders (O_id),
    CONSTRAINT order_details_Product_table FOREIGN KEY (Product_table_P_id)
    REFERENCES Product_table (P_id)
);

-- End of file.

