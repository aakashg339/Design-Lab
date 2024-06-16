create table Customers (
  Id int, 
  FirstName varchar(40) not null, 
  LastName varchar(40) not null, 
  City varchar(40), 
  Country varchar(40), 
  Phone varchar(20), 
  constraint PK_CUSTOMER primary key (Id)
);
create table Orders (
  Id int, 
  OrderDate datetime not null default (
    CURDATE()
  ), 
  OrderNumber varchar(10), 
  CustomerId int not null, 
  TotalAmount decimal(12, 2) default 0, 
  constraint PK_ORDER primary key (Id)
);
create table OrderItem (
  Id int, 
  OrderId int not null, 
  ProductId int not null, 
  UnitPrice decimal(12, 2) not null default 0, 
  Quantity int not null default 1, 
  constraint PK_ORDERITEM primary key (Id)
);
create table Products (
  Id int, 
  ProductName varchar(50) not null, 
  SupplierId int not null, 
  UnitPrice decimal(12, 2) default 0, 
  Package varchar(30), 
  IsDiscontinued bit not null default 0, 
  constraint PK_PRODUCT primary key (Id)
);
create table Suppliers (
  Id int, 
  CompanyName varchar(40) not null, 
  ContactName varchar(50), 
  ContactTitle varchar(40), 
  City varchar(40), 
  Country varchar(40), 
  Phone varchar(30), 
  Fax varchar(30), 
  constraint PK_SUPPLIER primary key (Id)
);
alter table 
  Orders 
add 
  constraint FK_ORDER_REFERENCE_CUSTOMER foreign key (CustomerId) references Customers (Id);
alter table 
  OrderItem 
add 
  constraint FK_ORDERITE_REFERENCE_ORDER foreign key (OrderId) references Orders (Id);
alter table 
  OrderItem 
add 
  constraint FK_ORDERITE_REFERENCE_PRODUCT foreign key (ProductId) references Products (Id);
alter table 
  Products 
add 
  constraint FK_PRODUCT_REFERENCE_SUPPLIER foreign key (SupplierId) references Suppliers (Id);
