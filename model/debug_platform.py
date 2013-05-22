from database import database
from stock_quote import stock_quote
from features import Features

ticker = 'AAPL'
analytic = 'Bernstein'

database = database()
stock_quote = stock_quote()
target_data = database.return_targetprices(analytic, ticker)
stock_data = stock_quote.get_data(ticker)
beta = stock_quote.get_beta(ticker)

features = Features(
    target_data=target_data,
    stock_data=stock_data,
    beta=beta,
    plot=False,
    calculate=True
)
