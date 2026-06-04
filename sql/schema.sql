-- Bluestock MF Capstone Database Schema

CREATE TABLE 01_fund_master (
    amfi_code INTEGER,
    fund_name TEXT,
    category TEXT
);

CREATE TABLE 02_nav_history (
    date TEXT,
    amfi_code INTEGER,
    nav REAL
);

CREATE TABLE 03_aum_by_fund_house (
    month TEXT,
    fund_house TEXT,
    aum_crore REAL
);

CREATE TABLE 04_monthly_sip_inflows (
    month TEXT,
    sip_inflow_crore REAL
);

CREATE TABLE 05_category_inflows (
    month TEXT,
    category TEXT,
    net_inflow_crore REAL
);

CREATE TABLE 06_industry_folio_count (
    month TEXT,
    total_folios_crore REAL
);

CREATE TABLE 07_scheme_performance (
    amfi_code INTEGER,
    returns_1y REAL,
    returns_3y REAL,
    returns_5y REAL
);

CREATE TABLE 08_investor_transactions (
    investor_id TEXT,
    transaction_date TEXT,
    amount_inr REAL
);

CREATE TABLE 09_portfolio_holdings (
    amfi_code INTEGER,
    stock_symbol TEXT,
    weight_pct REAL
);

CREATE TABLE 10_benchmark_indices (
    date TEXT,
    index_name TEXT,
    close_value REAL
);