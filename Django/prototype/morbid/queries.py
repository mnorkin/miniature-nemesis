
front_page_query = " \
    SELECT  \
        DISTINCT \
        morbid_targetprice.date as date, \
        morbid_ticker.name as ticker_name, \
        morbid_ticker.long_name as ticker_long_name, \
        morbid_ticker.id as ticker_id, \
        morbid_analytic.name as analytic_name, \
        morbid_analytic.id as analytic_id, \
        morbid_targetprice.price as price, \
        morbid_analytic.slug as analytic_slug, \
        morbid_ticker.slug as ticker_slug, \
        morbid_ticker.last_stock_price as last_stock_price \
    FROM morbid_targetprice \
    RIGHT JOIN morbid_analytic ON ( \
        morbid_targetprice.analytic_id = morbid_analytic.id \
    ) \
    RIGHT JOIN morbid_ticker ON ( \
        morbid_targetprice.ticker_id = morbid_ticker.id \
    ) \
    WHERE \
        morbid_targetprice.date <= ( \
            SELECT DISTINCT morbid_targetprice.date \
            FROM morbid_targetprice \
            ORDER BY morbid_targetprice.date DESC LIMIT 1 \
            ) AND \
        morbid_targetprice.date > ( \
            SELECT DISTINCT morbid_targetprice.date \
            FROM morbid_targetprice \
            ORDER BY morbid_targetprice.date \
            DESC LIMIT 1 OFFSET 5 \
            ) AND\
        morbid_ticker.display = true \
    ORDER BY morbid_targetprice.date DESC \
    LIMIT %s OFFSET %s \
"

target_prices_for_ticker_query = "\
    SELECT \
        morbid_targetprice.date as date, \
        morbid_targetprice.price as price, \
        morbid_analytic.slug as analytic_slug, \
        morbid_analytic.name as analytic_name, \
        morbid_analytic.id as analytic_id, \
        morbid_ticker.slug as ticker_slug, \
        morbid_ticker.name as ticker_name, \
        morbid_ticker.id as ticker_id, \
        morbid_ticker.long_name as ticker_long_name, \
        morbid_ticker.last_stock_price as last_stock_price \
    FROM morbid_targetprice \
    RIGHT JOIN morbid_analytic ON ( \
        morbid_targetprice.analytic_id = morbid_analytic.id \
    ) \
    RIGHT JOIN morbid_ticker ON ( \
        morbid_targetprice.ticker_id = morbid_ticker.id \
    ) \
    WHERE \
        morbid_ticker.slug = E%s \
    ORDER BY morbid_targetprice.date DESC \
    LIMIT %s OFFSET %s \
"

target_prices_for_analytic_query = "\
    SELECT \
        morbid_targetprice.date as date, \
        morbid_targetprice.price as price, \
        morbid_analytic.slug as analytic_slug, \
        morbid_analytic.name as analytic_name, \
        morbid_analytic.id as analytic_id, \
        morbid_ticker.slug as ticker_slug, \
        morbid_ticker.name as ticker_name, \
        morbid_ticker.id as ticker_id, \
        morbid_ticker.long_name as ticker_long_name, \
        morbid_ticker.last_stock_price as last_stock_price \
    FROM morbid_targetprice \
    RIGHT JOIN morbid_analytic ON ( \
        morbid_targetprice.analytic_id = morbid_analytic.id \
    ) \
    RIGHT JOIN morbid_ticker ON ( \
        morbid_targetprice.ticker_id = morbid_ticker.id \
    ) \
    WHERE \
        morbid_analytic.slug = E%s \
    ORDER BY morbid_targetprice.date DESC \
    LIMIT %s OFFSET %s \
"

sort_by_features_query = "\
    SELECT \
        morbid_targetprice.id as target_id \
    FROM morbid_targetprice\
    RIGHT JOIN morbid_analytic ON ( \
        morbid_targetprice.analytic_id = morbid_analytic.id \
    ) \
    RIGHT JOIN morbid_featureanalyticticker ON ( \
        morbid_targetprice.analytic_id = morbid_featureanalyticticker.analytic_id AND \
        morbid_targetprice.ticker_id = morbid_featureanalyticticker.ticker_id \
    ) \
    RIGHT JOIN morbid_feature ON ( \
        morbid_featureanalyticticker.feature_id = morbid_feature.id\
    )\
    RIGHT JOIN morbid_ticker ON ( \
        morbid_targetprice.ticker_id = morbid_ticker.id \
    )\
    WHERE \
        morbid_targetprice.date <= ( \
            SELECT DISTINCT morbid_targetprice.date \
            FROM morbid_targetprice \
            ORDER BY morbid_targetprice.date DESC LIMIT 1 \
            ) AND \
        morbid_targetprice.date > ( \
            SELECT DISTINCT morbid_targetprice.date \
            FROM morbid_targetprice \
            ORDER BY morbid_targetprice.date \
            DESC LIMIT 1 OFFSET 5 \
            ) AND\
        morbid_ticker.display = true AND \
        morbid_feature.slug = '%(feature_slug)s' \
    ORDER BY morbid_featureanalyticticker.value %(sort_direction)s \
    LIMIT %(limit)s OFFSET %(offset)s \
"

target_prices_query = "\
    SELECT \
        morbid_targetprice.date as date, \
        morbid_ticker.name as ticker_name, \
        morbid_ticker.long_name as ticker_long_name, \
        morbid_ticker.id as ticker_id, \
        morbid_analytic.name as analytic_name, \
        morbid_analytic.id as analytic_id, \
        morbid_targetprice.price as price, \
        morbid_analytic.slug as analytic_slug, \
        morbid_ticker.slug as ticker_slug, \
        morbid_ticker.last_stock_price as last_stock_price \
    FROM morbid_targetprice \
    RIGHT JOIN morbid_analytic ON ( \
        morbid_targetprice.analytic_id = morbid_analytic.id \
    ) \
    RIGHT JOIN morbid_ticker ON ( \
        morbid_targetprice.ticker_id = morbid_ticker.id \
    )\
    WHERE \
        morbid_targetprice.id = %s \
"

features_query = "\
    SELECT \
        morbid_feature.name as name, \
        morbid_featureanalyticticker.value as value, \
        morbid_feature.slug as slug \
    FROM morbid_featureanalyticticker \
    RIGHT JOIN morbid_feature ON ( \
        morbid_featureanalyticticker.feature_id = morbid_feature.id \
    ) \
    WHERE \
        morbid_feature.display_in_frontpage = true AND\
        morbid_featureanalyticticker.ticker_id = %s AND \
        morbid_featureanalyticticker.analytic_id = %s \
    ORDER BY morbid_feature.name \
"
