DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS utxo;

CREATE TABLE transactions (
  hash VARCHAR(64) PRIMARY KEY,
  confirmed BOOLEAN DEFAULT FALSE,
  received_time TIMESTAMPTZ NOT NULL,
  size INT,
  total_inputs SMALLINT,
  total_outputs SMALLINT,
  total_btc_output DECIMAL(20, 8),
  total_btc_input DECIMAL(20, 8),
  fees NUMERIC,
  transacted_value_usd DECIMAL(12, 2)
);

CREATE TABLE utxo (
  id SERIAL,
  address VARCHAR(64) NOT NULL,
  tx_hash VARCHAR(64) NOT NULL,
  tx_index SMALLINT,
  tx_time TIMESTAMPTZ NOT NULL,
  script VARCHAR(64) NOT NULL,
  value DECIMAL(20, 8)
);

CREATE INDEX utxo_address ON utxo (address);