WITH CTE AS (
    SELECT *, 
           ROW_NUMBER() OVER (
               PARTITION BY time, city
               ORDER BY TempID
           ) AS rn
    FROM Meteo_Hourly
)
DELETE FROM CTE
WHERE rn > 1;
