SELECT p1.Id, p1.ProductName, p2.Id, p2.ProductName, COUNT(oi1.Id) AS freq
FROM Products AS p1, Products AS p2, OrderItem AS oi1, OrderItem AS oi2
WHERE p1.Id = oi1.ProductId
AND p2.Id = oi2.ProductId
AND oi1.OrderId = oi2.OrderId
AND p1.Id > p2.Id
GROUP BY p1.Id, p1.ProductName, p2.Id, p2.ProductName
ORDER BY freq DESC LIMIT 5;