ALTER TABLE temp_option_details
    ADD COLUMN option_contract_id INTEGER;

UPDATE temp_option_details AS temp
SET option_contract_id = optContract.id
FROM option_contracts AS optContract
WHERE temp."symbolId" = optContract.broker_id;

DROP TABLE IF EXISTS option_contract_prices_staging;

CREATE TABLE option_contract_prices_staging AS (
    SELECT 
        bid_price,
        bid_size,
        ask_price,
        ask_size,
        last_trade_price_tr_hrs,
        last_trade_price,
        last_trade_size,
        last_trade_tick,
        last_trade_time,
        volume,
        open_price,
        high_price,
        low_price,
        volatility,
        delta,
        gamma,
        theta,
        vega,
        rho,
        open_interest,
        delay,
        is_halted,
        vwap,
        option_contract_id
    FROM option_contract_prices WHERE 1 = 2
);


UPDATE option_contracts AS optContract
SET 
    updated_at = NOW(),
    bid_price = temp."bidPrice",
    bid_size = temp."bidSize",
    ask_price = temp."askSize",
    last_trade_price_tr_hrs = temp."lastTradePriceTrHrs",
    last_trade_price = temp."lastTradePrice",
    last_trade_size = temp."lastTradeSize",
    last_trade_tick = temp."lastTradeTick",
    last_trade_time = temp."lastTradeTime",
    volume = temp.volume,
    open_price = temp."openPrice",
    high_price = temp."highPrice",
    low_price = temp."lowPrice",
    volatility = temp.volatility,
    delta = temp.delta,
    gamma = temp.gamma,
    theta = temp.theta,
    vega = temp.vega,
    rho = temp.rho,
    open_interest = temp."openInterest",
    delay = temp.delay,
    is_halted = temp."isHalted",
    vwap = temp."VWAP"
FROM temp_option_details AS temp
WHERE optContract.id = temp.option_contract_id;

INSERT INTO option_contract_prices_staging
SELECT
    "bidPrice",
    "bidSize",
    "askPrice",
    "askSize",
    "lastTradePriceTrHrs",
    "lastTradePrice",
    "lastTradeSize",
    "lastTradeTick",
    "lastTradeTime",
    "volume",
    "openPrice",
    "highPrice",
    "lowPrice",
    "volatility",
    "delta",
    "gamma",
    "theta",
    "vega",
    "rho",
    "openInterest",
    "delay",
    "isHalted",
    "VWAP",
    "option_contract_id"
FROM temp_option_details AS temp
WHERE NOT EXISTS (
    SELECT * FROM option_contract_prices
    WHERE 
        option_contract_id = temp."option_contract_id"
    AND last_trade_time = temp."lastTradeTime");

INSERT INTO option_contract_prices (
    updated_at,
    created_at,
    bid_price,
    bid_size,
    ask_price,
    ask_size,
    last_trade_price_tr_hrs,
    last_trade_price,
    last_trade_size,
    last_trade_tick,
    last_trade_time,
    volume,
    open_price,
    high_price,
    low_price,
    volatility,
    delta,
    gamma,
    theta,
    vega,
    rho,
    open_interest,
    delay,
    is_halted,
    vwap,
    option_contract_id
)
SELECT now(), now(), * FROM option_contract_prices_staging;