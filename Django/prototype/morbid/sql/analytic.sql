--- Load module
-- CREATE EXTENSION pg_trgm;
-- CREATE EXTENSION btree_gin;
CREATE EXTENSION wildspeed;

---
INSERT INTO morbid_analytic (name, number_of_companies, number_of_tp, volatility, last_target_price, slug) VALUES 
  ('Barclay',         '9',  '12', '3',    '123.54', 'barclay'),
  ('Bernstein',       '15', '45', '-3',   '123.54', 'bernstein'),
  ('Citigroup',       '11', '33', '-12',  '123.54', 'citigroup'),
  ('Morgan Stanley',  '14', '23', '11',   '123.54', 'morgan-stanley'),
  ('JP Morgan',       '21', '18', '1',    '123.54', 'jp-morgan'); -- initial data for the tickers

-- ALTER TABLE morbid_analytic ADD COLUMN name_tsv tsvector; -- text optimization for searching `name`

-- CREATE TRIGGER tsvector_update_name BEFORE INSERT OR UPDATE ON morbid_analytic
  -- FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger(name_tsv, 'pg_catalog.english', name); -- Trigger for `name`

-- CREATE INDEX morbid_analytic_name_tsv ON morbid_analytic USING gin(name_tsv); -- GIN entry for `name`
CREATE INDEX morbid_analytic_name_idx ON morbid_analytic USING gin(lower(name) wildcard_ops);
-- CREATE INDEX wildspeed_btree_idx ON wildspeed_dict USING btree(lower(name) varchar_pattern_ops);

-- UPDATE morbid_analytic SET name_tsv=to_tsvector(name); -- update the database data