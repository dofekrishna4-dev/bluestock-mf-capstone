-- Bluestock MF Capstone Database Schema

CREATE TABLE fund_master (
    amfi_code INTEGER,
    fund_name TEXT,
    category TEXT
);

CREATE TABLE nav_history (
    date TEXT,
    amfi_code INTEGER,
    nav REAL
);

CREATE TABLE aum_by_fund_house (
    month TEXT,
    fund_house TEXT,
    aum_crore REAL
);

CREATE TABLE monthly_sip_inflows (
    month TEXT,
    sip_inflow_crore REAL
);

CREATE TABLE category_inflows (
    month TEXT,
    category TEXT,
    net_inflow_crore REAL
);

CREATE TABLE industry_folio_count (
    month TEXT,
    total_folios_crore REAL
);

CREATE TABLE scheme_performance (
    amfi_code INTEGER,
    returns_1y REAL,
    returns_3y REAL,
    returns_5y REAL
);

CREATE TABLE investor_transactions (
    investor_id TEXT,
    transaction_date TEXT,
    amount_inr REAL
);

CREATE TABLE portfolio_holdings (
    amfi_code INTEGER,
    stock_symbol TEXT,
    weight_pct REAL
);

CREATE TABLE benchmark_indices (
    date TEXT,
    index_name TEXT,
    close_value REAL
);