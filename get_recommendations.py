import yfinance as yf

"""
    convertion type 
        normal:  convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            includes are recommednation types simplist convertion
        simple:  convert recommendations to {Sell, Hold, Buy} 
            groups more confident recommedations together
        reduced: convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            same as normal but doesnt consider longer-term buy, specultive buy, specultive sell
    
"""
def get_recommendations(ticker,convert_type='normal'):
    yf_ticker_df = yf.Ticker(ticker)
    #get recommendations
    yf_recommendations_df = yf_ticker_df.recommendations

    #no recommendations for stock
    if yf_recommendations_df is None:
        return None

    #normalize recommendations
    yf_recommendations_df['To Grade'] = yf_recommendations_df['To Grade'].apply(normalize_recommendations, args=(convert_type,))

    return yf_recommendations_df

"""
    many firms include different terms for stock recommendations, this function attempts to map these terms to a smaller set of generally understood terms

    convertion type 
        normal:  convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            includes are recommednation types simplist convertion
        simple:  convert recommendations to {Sell, Hold, Buy} 
            groups more confident recommedations together
        reduced: convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            same as normal but doesnt consider longer-term buy, specultive buy, specultive sell
"""

def get_convert_type_keys(convert_type='normal'):
    if convert_type == 'normal':
        return ['Strong Sell','Sell','Hold','Buy','Strong Buy']
    elif convert_type == 'simple':
        return ['Sell','Hold','Buy']
    elif convert_type == 'reduced':
        return ['Strong Sell','Sell','Hold','Buy','Strong Buy']
    else:
        raise ValueError('Invalid convert type')

def normalize_recommendations(rec,convert_type='normal'):
    #convert to lower case
    rec = rec.lower()

    if convert_type == 'normal':

        strong_sell_arr = ['strong sell','focus recdude']
        sell_arr = ['overweight','sell','negative','reduce','sector underperform','market underperform','underperform','peer underperform','cautious','below average','speculative sell','tender','underperformer']
        hold_arr = ['hold neutral','neutral','equal-weight','sector weight','market weight','peer weight','hold','sector perform','market perform','perform','in-line','peer perform','peer','fair','mixed','average']
        buy_arr = ['long-term buy','underweight','buy','positive','accumulate','sector outperform','market outperform','outperform','peer outperform','add','outperformer','above average','specultive buy']
        strong_buy_arr = ['strong buy','conviction buy','top pick','focus buy','action list buy']

        #Strong Sell
        if rec in strong_sell_arr:
            return 'Strong Sell'
        #Sell
        elif rec in sell_arr:
            return 'Sell'
        #Hold
        elif rec in hold_arr:
            return 'Hold'
        #Buy
        elif rec in buy_arr:
            return 'Buy'
        #Strong Buy
        elif rec in strong_buy_arr:
            return 'Strong Buy'

        else:
            return 'Invalid'

    elif convert_type == 'simple':

        sell_arr = ['strong sell','focus recdude','overweight','sell','negative','reduce','sector underperform','market underperform','underperform','peer underperform','cautious','below average','speculative sell','tender','underperformer']
        hold_arr = ['hold neutral','neutral','equal-weight','sector weight','market weight','peer weight','hold','sector perform','market perform','perform','in-line','peer perform','peer','fair','mixed','average']
        buy_arr = ['strong buy','conviction buy','top pick','focus buy','action list buy','long-term buy','underweight','buy','positive','accumulate','sector outperform','market outperform','outperform','peer outperform','add','outperformer','above average','specultive buy']

        #Sell
        if rec in sell_arr:
            return 'Sell'
        #Hold
        elif rec in hold_arr:
            return 'Hold'
        #Buy
        elif rec in buy_arr:
            return 'Buy'

        else:
            return 'Invalid'

    if convert_type == 'reduced':

        dont_include = ['long-term buy','specultive buy','specultive sell']
        strong_sell_arr = ['strong sell','focus recdude']
        sell_arr = ['overweight','sell','negative','reduce','sector underperform','market underperform','underperform','peer underperform','cautious','below average','tender','underperformer']
        hold_arr = ['hold neutral','neutral','equal-weight','sector weight','market weight','peer weight','hold','sector perform','market perform','perform','in-line','peer perform','peer','fair','mixed','average']
        buy_arr = ['underweight','buy','positive','accumulate','sector outperform','market outperform','outperform','peer outperform','add','outperformer','above average']
        strong_buy_arr = ['strong buy','conviction buy','top pick','focus buy','action list buy']

        #Strong Sell
        if rec in strong_sell_arr:
            return 'Strong Sell'
        #Sell
        elif rec in sell_arr:
            return 'Sell'
        #Hold
        elif rec in hold_arr:
            return 'Hold'
        #Buy
        elif rec in buy_arr:
            return 'Buy'
        #Strong Buy
        elif rec in strong_buy_arr:
            return 'Strong buy'
        #Dont include
        elif rec in dont_include:
            return 'Dont Include'
        else:
            return 'Invalid'


if __name__ == '__main__':
    get_recommendations('MSFT',convert_type='normal')