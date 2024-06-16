SELECT c.Country, COUNT(o.Id)
FROM Orders AS o INNER JOIN Customers as c ON o.CustomerId = c.Id
GROUP BY c.Country