-- Method 1
SELECT CONCAT(c.FirstName, c.LastName) as customerName, AVG(o.TotalAmount) as averageOrderValue
FROM Customers as c JOIN Orders as o ON c.Id=o.CustomerId
GROUP BY customerName;

-- Method 2
-- SELECT AVG(o.TotalAmount) as averageOrderValue
-- FROM Orders as o
-- GROUP BY o.CustomerId;