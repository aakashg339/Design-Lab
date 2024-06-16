SELECT s.CompanyName
FROM Suppliers as s
WHERE (
    SELECT COUNT(DISTINCT p.Id)
    FROM Products as p
    WHERE p.SupplierId = s.Id
)>3;