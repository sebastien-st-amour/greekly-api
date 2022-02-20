DROP TABLE IF EXISTS option_contracts_staging;

CREATE TABLE option_contracts_staging AS (
    SELECT type, broker_id, expiration_date, strike_price, stock_id FROM option_contracts WHERE 1 = 2
);

INSERT INTO option_contracts_staging
SELECT
    CAST("type" AS optiontypes),
    "brokerId",
    "expiryDate",
    "strikePrice",
    "greeklyStockId"
FROM temp_table AS temp
WHERE NOT EXISTS (
    SELECT * FROM option_contracts WHERE broker_id = temp."brokerId");

INSERT INTO option_contracts (
    updated_at,
    created_at,
    type,
    broker_id,
    expiration_date,
    strike_price,
    stock_id
)
SELECT now(), now(), * FROM option_contracts_staging;