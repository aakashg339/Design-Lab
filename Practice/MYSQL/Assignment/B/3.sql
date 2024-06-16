SELECT SUM(o.TotalAmount)
FROM Orders as o
WHERE MONTH(o.OrderDate) = 10;