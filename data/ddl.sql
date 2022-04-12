/**
DDL for database tables using PostgreSQL.
*/

CREATE TABLE Store (
   StoreId  SERIAL,
   Address VARCHAR(50)         NOT NULL,
   PhoneNumber VARCHAR(15)     NOT NULL,
   Website VARCHAR(50),
   OpeningHours VARCHAR(20)    NOT NULL,
   PRIMARY KEY (StoreId)
);

CREATE TABLE Product (
   ProductId     CHAR(5)       NOT NULL,
   ProductName   VARCHAR(50),
   ListPrice     DECIMAL(9, 2),
   Category      VARCHAR(50),
   InStock       BOOLEAN       NOT NULL,
   PRIMARY KEY (ProductId)
);

CREATE TABLE Concern (
   SessionId   CHAR(10)          NOT NULL, 
   PhoneNumber CHAR(10)          NOT NULL, 
   Description VARCHAR(1000)     NOT NULL, 
   DateCreated TIMESTAMP         NOT NULL,
   Status CHAR(9)                NOT NULL CHECK (Status IN ('open', 'closed', 'cancelled')),
   PRIMARY KEY (SessionId)
);

CREATE TABLE Employee (
   EmployeeId    CHAR(5)    NOT NULL,
   EmployeeName  VARCHAR(50),
   Salary        DECIMAL(9,2),
   SupervisorId  CHAR(5),
   PRIMARY KEY (EmployeeId),
   FOREIGN KEY (SupervisorId) REFERENCES Employee (EmployeeId)
);

CREATE TABLE Customer (
   CustomerId    CHAR(5)    NOT NULL,
   CustomerName  VARCHAR(50),
   PRIMARY KEY (CustomerId)
);

CREATE TABLE Orders (
   OrderId       CHAR(5)    NOT NULL,
   OrderDate     TIMESTAMP,
   CustomerId    CHAR(5),
   EmployeeId    CHAR(5),
   Total         DECIMAL(9,2),
   PRIMARY KEY (OrderId),
   FOREIGN KEY (CustomerId) REFERENCES Customer (CustomerId) ON UPDATE CASCADE ON DELETE CASCADE,
   FOREIGN KEY (EmployeeId) REFERENCES Employee (EmployeeId) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE OrderedProduct (
   OrderId       CHAR(5)    NOT NULL,
   ProductId     CHAR(5) 	NOT NULL,
   Quantity      INTEGER,
   Price         DECIMAL(9,2),
   PRIMARY KEY (OrderId, ProductId),
   FOREIGN KEY (OrderId) REFERENCES Orders (OrderId) ON UPDATE CASCADE ON DELETE CASCADE,
   FOREIGN KEY (ProductId) REFERENCES Product (ProductId) ON UPDATE CASCADE ON DELETE SET NULL
);

COPY Customer FROM '/docker-entrypoint-initdb.d/samples/customer.csv' DELIMITER ',' CSV HEADER;
COPY Employee FROM '/docker-entrypoint-initdb.d/samples/employee.csv' DELIMITER ',' CSV HEADER;
COPY Orders FROM '/docker-entrypoint-initdb.d/samples/orders.csv' DELIMITER ',' CSV HEADER;
COPY Product FROM '/docker-entrypoint-initdb.d/samples/product.csv' DELIMITER ',' CSV HEADER;
COPY Store(Address, PhoneNumber, Website, OpeningHours) FROM '/docker-entrypoint-initdb.d/samples/store.csv' DELIMITER ',' CSV HEADER;
COPY OrderedProduct FROM '/docker-entrypoint-initdb.d/samples/orderedproduct.csv' DELIMITER ',' CSV HEADER;