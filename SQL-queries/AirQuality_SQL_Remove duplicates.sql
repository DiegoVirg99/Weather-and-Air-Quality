WITH CTE AS (
    SELECT *, 
           ROW_NUMBER() OVER (
               PARTITION BY time, city, aqi, co, no2, o3, so2, pm2_5, pm10, nh3
               ORDER BY TempID
           ) AS rn
    FROM AirQuality_Data
)
DELETE FROM CTE
WHERE rn > 1;
