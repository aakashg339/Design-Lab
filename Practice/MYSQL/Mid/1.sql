SELECT s.CompanyName, SUM(oi.UnitPrice * oi.Quantity) AS totalRevenue
FROM (Suppliers AS s INNER JOIN Products as p ON s.Id = p.SupplierId)
    INNER JOIN OrderItem AS oi ON p.Id = oi.ProductId
GROUP BY s.CompanyName
ORDER BY totalRevenue DESC;