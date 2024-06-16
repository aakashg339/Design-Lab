SELECT c.FirstName, c.LastName
FROM Customers AS c
WHERE (
    SELECT COUNT(o1.Id)
    FROM Orders AS o1
    WHERE o1.CustomerId = c.Id
    AND YEAR(o1.OrderDate) = 2014
) > (
    SELECT COUNT(o2.Id)
    FROM Orders AS o2
    WHERE o2.CustomerId = c.Id
    AND YEAR(o2.OrderDate) = 2013
)
AND (
    SELECT COUNT(o3.Id)
    FROM Orders AS o3
    WHERE o3.CustomerId = c.Id
    AND YEAR(o3.OrderDate) = 2013
) > (
    SELECT COUNT(o4.Id)
    FROM Orders AS o4
    WHERE o4.CustomerId = c.Id
    AND YEAR(o4.OrderDate) = 2012
)