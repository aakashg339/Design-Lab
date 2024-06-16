CREATE VIEW productAndQuantity AS (
    SELECT p.Id, p.ProductName, SUM(oi.Quantity) as totalQuantity
    FROM Products AS p INNER JOIN OrderItem AS oi ON p.Id = oi.ProductId
    GROUP BY p.Id, p.ProductName
);

SELECT pq1.Id, pq1.ProductName
FROM productAndQuantity AS pq1
WHERE pq1.totalQuantity = (
    SELECT MAX(pq2.totalQuantity)
    FROM productAndQuantity AS pq2
    WHERE pq2.totalQuantity < (
        SELECT MAX(pq3.totalQuantity)
        FROM productAndQuantity AS pq3
    )
);