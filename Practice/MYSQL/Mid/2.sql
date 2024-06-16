SELECT MONTH(o.OrderDate) AS OrderMonth, SUM(o.TotalAmount) AS revenue
FROM Orders AS o
WHERE YEAR(o.OrderDate) = 2013
GROUP BY OrderMonth
ORDER BY OrderMonth;