# Data Sources

## Amazon (`Amazon_raw_data.xlsx`)
Figures are Amazon.com Inc.'s consolidated, audited results in USD billions, taken from Amazon's
quarterly/full-year earnings releases and 10-K filings (SEC EDGAR / ir.aboutamazon.com):

- Total Revenue, Operating Income, Net Income, segment sales (North America, International, AWS) —
  Amazon Q4 earnings releases, FY2020–FY2024.
- Advertising Revenue — Amazon "Advertising services" revenue line, disclosed in quarterly/annual filings.
- CFO (Cash Flow from Operating Activities) and Capex (purchases of property & equipment) — Amazon
  consolidated statements of cash flows, FY2020–FY2024.

All figures are full fiscal (calendar) year results, in $ billions, rounded to 2 decimals.

## Indian market comparison (`indian_market_comparison.csv`)
Zomato (Eternal Ltd), Swiggy Ltd, and FSN E-Commerce Ventures Ltd (Nykaa) are publicly listed on the
NSE/BSE and file audited consolidated results. Revenue and net income figures (INR crore) are sourced
from consolidated financial statements as aggregated by stockanalysis.com, cross-checked against press
coverage of official results (e.g., Zomato FY24 net profit of ₹351 Cr, Swiggy FY24 net loss of ₹2,350 Cr).

Flipkart, Reliance Retail, and Tata Digital are **not included** — they don't file standalone public
financial statements (Flipkart is a private Singapore-domiciled entity with only partial regulatory
filings; Reliance Retail and Tata Digital report only as consolidated segments inside larger parent
company results), so comparable figures aren't independently verifiable. They remain a documented
future-work item rather than fabricated data points.

### Fiscal year alignment
Indian companies report on an **April–March** fiscal year; Amazon reports on a **calendar year**. Each
Indian FY is aligned to the Amazon calendar year with the greatest overlap (9 of 12 months), e.g. Indian
FY2024 (Apr 2023–Mar 2024) is aligned to Amazon CY2023. This is a standard approximation for cross-market
comparison, not a precise quarter-for-quarter match — see `Amazon_Aligned_Year` column.

### Currency conversion
Revenue/net income are converted to USD at approximate average annual RBI reference rates for each
fiscal year (₹74.5, ₹80.4, ₹82.8, ₹84.5 per USD for FY22–FY25 respectively). This is for illustrative,
order-of-magnitude comparison only — not a precise treasury-grade FX conversion.

Pulled: August 2026.
