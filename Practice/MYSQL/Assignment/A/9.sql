SELECT CONCAT(c.FirstName, " ", c.LASTNAME) as customerName, COUNT(o.Id) as TotalOrders
FROM Customers as c JOIN Orders as o ON c.Id=o.CustomerId
GROUP BY customerName