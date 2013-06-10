SELECT tc.ticker as ticker, an.name as analytic, tp.price0 as price0, tp.date as pub_date
FROM sink_targetprice as tp, sink_analytic as an, sink_ticker as tc
WHERE an.id= tp.analytic_id AND tc.id=tp.ticker_id AND tp.price0 != 0
ORDER BY tp.date DESC;