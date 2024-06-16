-- METHOD 1
-- CREATE VIEW productQuantityMapping AS (
--     SELECT oi.ProductId as productId, SUM(oi.Quantity) as totalQuantity
--     FROM OrderItem as oi
--     GROUP BY productId
-- );

-- SELECT ProductName
-- FROM Products as p
-- WHERE p.Id IN (
--     SELECT pQM1.productId
--     FROM productQuantityMapping as pQM1
--     WHERE pQM1.totalQuantity = (
--         SELECT MAX(pQM2.totalQuantity)
--         FROM productQuantityMapping AS pQM2
--     )
-- );

-- -- Method 2
-- with productQuantityMapping AS (
--     SELECT oi.ProductId as productId, SUM(oi.Quantity) as totalQuantity
--     FROM OrderItem as oi
--     GROUP BY productId
-- );

-- SELECT ProductName
-- FROM Products as p
-- WHERE p.Id IN (
--     SELECT pQM1.productId
--     FROM productQuantityMapping as pQM1
--     WHERE pQM1.totalQuantity = (
--         SELECT MAX(pQM2.totalQuantity)
--         FROM productQuantityMapping AS pQM2
--     )
-- );

-- Method 3
SELECT p.ProductName, SUM(oi.Quantity) as totalQuantity
FROM OrderItem as oi JOIN Products as p ON oi.ProductId = p.Id
GROUP BY p.ProductName
ORDER BY totalQuantity DESC
LIMIT 1;