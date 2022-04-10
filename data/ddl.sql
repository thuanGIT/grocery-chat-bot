/**
DDL for database tables using PostgreSQL.
*/

CREATE TABLE Store (
   StoreId  SERIAL,
   Name VARCHAR(50)            NOT NULL,
   Address VARCHAR(50)         NOT NULL,
   PhoneNumber VARCHAR(10)     NOT NULL,
   Website VARCHAR(50),
   OpeningHours VARCHAR(20)    NOT NULL,
   PriceRange VARCHAR(10),
   PRIMARY KEY (StoreId)
);

CREATE TABLE Product (
   ProductId     CHAR(5)       NOT NULL,
   ProductName   VARCHAR(50),
   Category      VARCHAR(50),
   ListPrice     DECIMAL(9, 2),
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

