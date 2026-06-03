CREATE DATABASE amazon_financial_intelligence;
USE amazon_financial_intelligence;
CREATE TABLE IF NOT EXISTS amazon_financials (
    Year INT PRIMARY KEY,
    Total_Revenue DECIMAL(10,2),
    Operating_Income DECIMAL(10,2),
    Net_Income DECIMAL(10,2),
    AWS_Revenue DECIMAL(10,2),
    North_America_Revenue DECIMAL(10,2),
    International_Revenue DECIMAL(10,2),
    Advertising_Revenue DECIMAL(10,2),
    CFO DECIMAL(10,2),
    Capex DECIMAL(10,2)
);
DROP TABLE `year,total_revenue,operating_income,net_income,aws_revenue,north_america_revenue,international_revenue,advertising_revenue,cfo,capex`;
CREATE TABLE amazon_financials (
    Year INT PRIMARY KEY,
    Total_Revenue DECIMAL(10,2),
    Operating_Income DECIMAL(10,2),
    Net_Income DECIMAL(10,2),
    AWS_Revenue DECIMAL(10,2),
    North_America_Revenue DECIMAL(10,2),
    International_Revenue DECIMAL(10,2),
    Advertising_Revenue DECIMAL(10,2),
    CFO DECIMAL(10,2),
    Capex DECIMAL(10,2)
);
INSERT INTO amazon_financials VALUES
(2020,386.06,22.90,21.33,45.37,236.28,104.41,21.45,66.06,40.14),
(2021,469.82,24.88,33.36,62.20,279.84,127.79,31.16,46.33,61.05),
(2022,513.98,12.25,-2.72,80.10,315.88,118.01,37.74,46.75,63.65),
(2023,574.78,36.85,30.43,90.76,352.83,131.20,46.91,84.95,52.86),
(2024,620.00,48.00,36.00,107.00,380.00,145.00,56.00,98.00,58.00);

SELECT * FROM amazon_financials;
DESCRIBE amazon_financials;

SELECT Year, Total_Revenue
FROM amazon_financials
ORDER BY Year;

SELECT Year, Net_Income
FROM amazon_financials
ORDER BY Year;

SELECT 
Year,
AWS_Revenue,
Total_Revenue,
ROUND((AWS_Revenue / Total_Revenue)*100,2) AS AWS_Contribution_Pct
FROM amazon_financials;

SELECT
    Year,
    Total_Revenue,
    LAG(Total_Revenue) OVER (ORDER BY Year) AS Prev_Revenue,
    ROUND(
        ((Total_Revenue - LAG(Total_Revenue) OVER (ORDER BY Year))
        / LAG(Total_Revenue) OVER (ORDER BY Year)) * 100,2
    ) AS YoY_Growth_Pct
FROM amazon_financials;

SELECT
    Year,
    ROUND((Operating_Income / Total_Revenue) * 100,2) AS Operating_Margin_Pct
FROM amazon_financials;

SELECT
    Year,
    Net_Income,
    RANK() OVER (ORDER BY Net_Income DESC) AS Profit_Rank
FROM amazon_financials;

SELECT
    Year,
    Total_Revenue,
    SUM(Total_Revenue) OVER (ORDER BY Year) AS Cumulative_Revenue
FROM amazon_financials;

SELECT
    Year,
    AWS_Revenue,
    North_America_Revenue,
    International_Revenue
FROM amazon_financials;

SELECT
    Year,
    AWS_Revenue,
    North_America_Revenue,
    International_Revenue
FROM amazon_financials;

SELECT
ROUND(
    (POWER(
        (SELECT Total_Revenue FROM amazon_financials WHERE Year = 2024) /
        (SELECT Total_Revenue FROM amazon_financials WHERE Year = 2020),
        1.0/4
    ) - 1) * 100,2
) AS Revenue_CAGR_Pct;