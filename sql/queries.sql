-- =====================================================
-- Bluestock Mutual Fund Capstone
-- SQL Analysis Queries
-- =====================================================

---------------------------------------------------------
-- 1. Total Mutual Fund Schemes
---------------------------------------------------------
SELECT COUNT(*) AS total_schemes
FROM fund_master;


---------------------------------------------------------
-- 2. List All Fund Categories
---------------------------------------------------------
SELECT DISTINCT category
FROM fund_master
ORDER BY category;


---------------------------------------------------------
-- 3. Average NAV of Each Fund
---------------------------------------------------------
SELECT
    amfi_code,
    AVG(nav) AS average_nav
FROM nav_history
GROUP BY amfi_code
ORDER BY average_nav DESC;


---------------------------------------------------------
-- 4. Total AUM by Fund House
---------------------------------------------------------
SELECT
    fund_house,
    SUM(aum_crore) AS total_aum
FROM aum_by_fund_house
GROUP BY fund_house
ORDER BY total_aum DESC;


---------------------------------------------------------
-- 5. Monthly SIP Inflows
---------------------------------------------------------
SELECT
    month,
    sip_inflow_crore
FROM monthly_sip_inflows
ORDER BY month;


---------------------------------------------------------
-- 6. Category-wise Net Inflows
---------------------------------------------------------
SELECT
    category,
    SUM(net_inflow_crore) AS total_net_inflow
FROM category_inflows
GROUP BY category
ORDER BY total_net_inflow DESC;


---------------------------------------------------------
-- 7. Industry Folio Trend
---------------------------------------------------------
SELECT
    month,
    total_folios_crore
FROM industry_folio_count
ORDER BY month;


---------------------------------------------------------
-- 8. Top Performing Funds (5-Year Return)
---------------------------------------------------------
SELECT
    amfi_code,
    returns_5y
FROM scheme_performance
ORDER BY returns_5y DESC
LIMIT 10;


---------------------------------------------------------
-- 9. Best Funds by 3-Year Return
---------------------------------------------------------
SELECT
    amfi_code,
    returns_3y
FROM scheme_performance
ORDER BY returns_3y DESC
LIMIT 10;


---------------------------------------------------------
-- 10. Investor Transaction Summary
---------------------------------------------------------
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount_inr) AS total_transaction_amount,
    AVG(amount_inr) AS average_transaction
FROM investor_transactions;


---------------------------------------------------------
-- 11. Top Portfolio Holdings
---------------------------------------------------------
SELECT
    stock_symbol,
    AVG(weight_pct) AS average_weight
FROM portfolio_holdings
GROUP BY stock_symbol
ORDER BY average_weight DESC
LIMIT 10;


---------------------------------------------------------
-- 12. Latest Benchmark Index Values
---------------------------------------------------------
SELECT
    index_name,
    MAX(close_value) AS latest_close
FROM benchmark_indices
GROUP BY index_name
ORDER BY latest_close DESC;