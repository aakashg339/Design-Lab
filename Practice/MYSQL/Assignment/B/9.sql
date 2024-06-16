SELECT DISTINCT p1.ProductName
FROM Products AS p1 JOIN Products AS p2 ON p1.Id = p2.Id
WHERE p1.SupplierId <> p2.SupplierId;
