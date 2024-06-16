SELECT c.FirstName, c.LastName
FROM Customers AS c
WHERE (
    SELECT SUM(o.TotalAmount)
    FROM Orders as o
    WHERE o.CustomerId = c.Id
) > 100000;