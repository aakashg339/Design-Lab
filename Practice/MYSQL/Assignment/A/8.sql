-- -- Method 1
-- SELECT DISTINCT c.FirstName, c.LastName
-- FROM Customers as c
-- WHERE c.Id IN (SELECT CustomerId FROM Orders);

-- -- Method 2
-- SELECT DISTINCT c.FirstName, c.LastName
-- FROM Customers as c JOIN Orders as o on c.Id = o.CustomerId

-- Method 3
SELECT DISTINCT c.FirstName, c.LastName
FROM Customers as c
WHERE EXISTS (
    SELECT *
    FROM Orders as o
    WHERE o.CustomerId = c.Id
)