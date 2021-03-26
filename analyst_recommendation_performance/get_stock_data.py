import yfinance as yf

"""
    data_type
        price: return price

        plynch: return peter lynch fair value

        eps: return earnings per share

"""
def get_historical_market_data(ticker,start,end,interval,data_type):
    yf_ticker = yf.Ticker(ticker)
    if data_type == 'price':
        hist = yf_ticker.history(ticker=ticker,start=start,end=end,interval=interval)
        return hist
    if data_type == 'plynch':
        #TODO
        return None
    