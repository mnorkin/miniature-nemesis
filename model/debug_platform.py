from database import database
from stock_quote import stock_quote
from features import Features

_ticker = 'AAPL'
_analytic = 'Sterne Agee'

database = database()
stock_quote = stock_quote()
target_data = database.return_targetprices(ticker=_ticker, analytic=_analytic)
stock_data = stock_quote.get_data(ticker=_ticker)
beta = stock_quote.get_beta(ticker=_ticker)

features = Features(
    target_data=target_data,
    stock_data=stock_data,
    beta=beta,
    calculate=True
)
