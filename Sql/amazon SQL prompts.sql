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

-- ============================================================
-- Anomaly detection: flag years where a metric deviates more
-- than 1.5 standard deviations from the 5-year mean (z-score),
-- computed entirely in SQL with window aggregates.
-- ============================================================
SELECT
    Year,
    Net_Income,
    ROUND(
        (Net_Income - AVG(Net_Income) OVER ()) / STDDEV(Net_Income) OVER (),
    2) AS Net_Income_Zscore,
    CASE
        WHEN ABS((Net_Income - AVG(Net_Income) OVER ()) / STDDEV(Net_Income) OVER ()) > 1.5
        THEN 'ANOMALY' ELSE 'NORMAL'
    END AS Net_Income_Flag
FROM amazon_financials;

SELECT
    Year,
    ROUND((Operating_Income / Total_Revenue) * 100,2) AS Operating_Margin_Pct,
    ROUND(
        (
            (Operating_Income / Total_Revenue * 100)
            - AVG(Operating_Income / Total_Revenue * 100) OVER ()
        ) / STDDEV(Operating_Income / Total_Revenue * 100) OVER (),
    2) AS Operating_Margin_Zscore
FROM amazon_financials;

-- ============================================================
-- Indian market comparison: Zomato (Eternal), Swiggy, and Nykaa
-- — the three companies from the Indian Market Expansion module
-- that publish standalone audited financials. Flipkart, Reliance
-- Retail, and Tata Digital are excluded (no comparable public
-- financials); see data/SOURCES.md.
-- ============================================================
CREATE TABLE IF NOT EXISTS indian_companies (
    Company VARCHAR(20),
    Fiscal_Year VARCHAR(10),
    Amazon_Aligned_Year INT,
    Revenue_INR_Cr DECIMAL(12,2),
    Net_Income_INR_Cr DECIMAL(12,2),
    FX_Rate_INR_per_USD DECIMAL(6,2),
    Revenue_USD_B DECIMAL(10,4),
    Net_Income_USD_B DECIMAL(10,4)
);

INSERT INTO indian_companies VALUES
('Nykaa','FY2022',2021,3773.90,41.075,74.5,0.5066,0.0055),
('Nykaa','FY2023',2022,5143.80,19.262,80.4,0.6398,0.0024),
('Nykaa','FY2024',2023,6385.60,32.260,82.8,0.7712,0.0039),
('Nykaa','FY2025',2024,7949.80,66.080,84.5,0.9407,0.0078),
('Zomato','FY2022',2021,4192.40,-1208.700,74.5,0.5627,-0.1622),
('Zomato','FY2023',2022,7079.00,-971.000,80.4,0.8804,-0.1208),
('Zomato','FY2024',2023,12114.00,351.000,82.8,1.4630,0.0424),
('Zomato','FY2025',2024,20243.00,527.000,84.5,2.3956,0.0624),
('Swiggy','FY2022',2021,5704.90,-3628.900,74.5,0.7658,-0.4871),
('Swiggy','FY2023',2022,8264.60,-4179.300,80.4,1.0279,-0.5198),
('Swiggy','FY2024',2023,11247.40,-2350.200,82.8,1.3581,-0.2838),
('Swiggy','FY2025',2024,15227.00,-3117.000,84.5,1.8014,-0.3689);

-- Amazon vs. each Indian peer in the latest aligned year: scale gap and margin gap
SELECT
    ic.Company,
    ic.Fiscal_Year,
    ic.Revenue_USD_B AS Company_Revenue_USD_B,
    af.Total_Revenue AS Amazon_Revenue_USD_B,
    ROUND(af.Total_Revenue / ic.Revenue_USD_B, 1) AS Amazon_Scale_Multiple,
    ROUND((ic.Net_Income_USD_B / ic.Revenue_USD_B) * 100, 2) AS Company_Net_Margin_Pct,
    ROUND((af.Net_Income / af.Total_Revenue) * 100, 2) AS Amazon_Net_Margin_Pct
FROM indian_companies ic
JOIN amazon_financials af ON af.Year = ic.Amazon_Aligned_Year
WHERE ic.Amazon_Aligned_Year = (SELECT MAX(Amazon_Aligned_Year) FROM indian_companies)
ORDER BY ic.Company;

-- Revenue CAGR per Indian company across the 4-year window (window-function based)
SELECT
    Company,
    ROUND(
        (POWER(
            MAX(Revenue_USD_B) / MIN(Revenue_USD_B),
            1.0 / (MAX(Amazon_Aligned_Year) - MIN(Amazon_Aligned_Year))
        ) - 1) * 100, 2
    ) AS Revenue_CAGR_Pct
FROM indian_companies
GROUP BY Company;