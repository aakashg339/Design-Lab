SELECT COUNT(Id)
FROM Orders
WHERE MONTH(OrderDate) = 12;