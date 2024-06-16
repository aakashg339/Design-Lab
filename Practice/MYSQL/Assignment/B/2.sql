SELECT c.FIRSTNAME, c.LASTNAME
FROM Customers as c
WHERE c.Id NOT IN (
    SELECT o.CustomerId
    FROM Orders as o
    WHERE YEAR(o.OrderDate) = 2014
);