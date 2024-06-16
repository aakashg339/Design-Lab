-- SELECT s.CompanyName, AVG(p.UnitPrice)
-- FROM Suppliers as s JOIN Products as p ON s.Id = p.SupplierId
-- GROUP BY s.CompanyName


-- For one supplier
SELECT AVG(p.UnitPrice)
FROM Products as p
WHERE p.SupplierId = 11;