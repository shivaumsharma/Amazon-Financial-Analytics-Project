# Indian Market Expansion Module

**Status: partially implemented.** The comparative-analytics module described below now exists and
runs live in the Streamlit dashboard (`Python/indian_comparison.py`, data in
`data/indian_market_comparison.csv`) — see the "Indian Market Comparison" section of the main
[README](../README.md).

## What's built
Amazon is benchmarked against the three companies from the original wishlist that are publicly
listed and file audited financials:
- **Zomato (Eternal Ltd)**
- **Swiggy Ltd**
- **Nykaa (FSN E-Commerce Ventures Ltd)**

Using real revenue and net income figures (see `data/SOURCES.md`), the dashboard computes and
visualizes:
- Indexed revenue growth (each company rebased to 100 in its first aligned year)
- Revenue CAGR per company vs. Amazon's
- Net margin comparison (profitability maturity gap)
- Amazon's scale multiple over each peer, per year

## What's not built (and why)
- **Flipkart, Reliance Retail, Tata Digital** are not included. Flipkart is a private,
  Singapore-domiciled entity; Reliance Retail and Tata Digital report only as segments inside a
  larger parent company's consolidated results. None publish standalone audited financials, so
  there's no verifiable public figure to plot — including them would mean fabricating numbers.
  If/when reliable estimates become available (e.g. from a data vendor with modeled private-company
  financials), this would be the place to add them, clearly labeled as estimates.

## Possible next steps
- Extend to global peers (Walmart, Alibaba, JD.com) for a broader benchmarking view
- Add quarterly granularity for the three companies already covered
- Revisit Flipkart/Reliance Retail/Tata Digital if a licensed data source becomes available
