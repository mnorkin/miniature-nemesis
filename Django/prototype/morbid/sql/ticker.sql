---
INSERT INTO morbid_ticker (name, long_name, last_stock_price, number_of_analytics, number_of_tp, consensus_min, consensus_avg, consensus_max, slug) VALUES 
  ('GOOG', 'Google Inc.',   '12.3', '11', '53', '54.3', '60.4', '82.3', 'google'),
  ('AAPL', 'Apple Inc.',    '13.3', '12', '23', '36.3', '44.4', '52.3', 'apple'),
  ('RIG', 'Transocean LTD', '15.3', '62', '17', '10.3', '34.4', '66.3', 'transocean'),
  ('HMIN', 'Home Inns & Hotels Management Inc. (ADR)', '15.3', '62', '17', '10.3', '34.4', '66.3', 'home-inns-hotels-management-inc'); -- initial data for the tickers

-- ALTER TABLE morbid_ticker ADD COLUMN name_tsv tsvector; -- text optimization for searching `name`
-- ALTER TABLE morbid_ticker ADD COLUMN long_name_tsv tsvector; -- text optimization for searching `long_name`

-- CREATE TRIGGER tsvector_update_name BEFORE INSERT OR UPDATE ON morbid_ticker
  -- FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(name_tsv, 'pg_catalog.english', name); -- Trigger for `name`

-- CREATE TRIGGER tsvector_update_long_name BEFORE INSERT OR UPDATE ON morbid_ticker
  -- FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(long_name_tsv, 'pg_catalog.english', long_name); -- Trigger for `long_name`

-- CREATE INDEX morbid_ticker_name_tsv ON morbid_ticker USING gin(name_tsv); -- GIN entry for `name`
-- CREATE INDEX morbid_ticker_name_idx ON morbid_ticker USING gin(lower(name) wildcard_ops); -- TODO !
-- CREATE INDEX morbid_ticker_long_name_tsv ON morbid_ticker USING gin(long_name_tsv); -- GIN entry for `long_name`
-- CREATE INDEX morbid_ticker_long_name_idx ON morbid_ticker USING gin(lower(long_name) wildcard_ops); -- TODO !

-- UPDATE morbid_ticker SET name_tsv=to_tsvector(name); -- update the database data
-- UPDATE morbid_ticker SET long_name_tsv=to_tsvector(long_name); --- update database data