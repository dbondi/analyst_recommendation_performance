import pandas as pd
import io
import requests
import json


_EXCHANGE_LIST = ['nyse', 'nasdaq', 'amex']

_SECTORS_LIST = set(['Consumer Non-Durables', 'Capital Goods', 'Health Care',
       'Energy', 'Technology', 'Basic Industries', 'Finance',
       'Consumer Services', 'Public Utilities', 'Miscellaneous',
       'Consumer Durables', 'Transportation'])

_ANALYST_RATINGS_LIST = set(['Strong Buy','Hold','Buy','Sell','Strong Sell'])

_REGIONS_LIST = set(['AFRICA','EUROPE','ASIA','AUSTRALIA+AND+SOUTH+PACIFIC','CARIBBEAN','SOUTH+AMERICA','MIDDLE+EAST','NORTH+AMERICA'])

_COUNTRIES_LIST = set(['Argentina','Armenia','Australia','Austria','Belgium','Bermuda','Brazil','Canada','Cayman Islands','Chile','Colombia',
        'Costa Rica','Curacao','Cyprus','Denmark','Finland','France','Germany','Greece','Guernsey','Hong Kong','India','Indonesia','Ireland',
        'Isle of Man','Israel','Italy','Japan','Jersey','Luxembourg','Macau','Mexico','Monaco','Netherlands','Norway','Panama','Peru',
        'Philippines','Puerto Rico','Russia','Singapore','South Africa','South Korea','Spain','Sweden','Switzerland','Taiwan','Turkey',
        'United Kingdom','United States'])


# headers and params used to bypass NASDAQ's anti-scraping mechanism in function __exchange2df
headers = {
    'authority': 'nasdaq.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://github.com/shilewenuw/get_all_tickers/issues/2',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'AKA_A2=A; NSC_W.TJUFEFGFOEFS.OBTEBR.443=ffffffffc3a0f70e45525d5f4f58455e445a4a42378b',
}

def params(exchange='NYSE',regions=None,sectors=None,countries=None,analystRatings=None):
    params = (('exchange', exchange),('download', 'true'),('tableonly', 'true'))

    if regions is not None:
        if isinstance(regions, str):
            regions = [regions]
        if not _REGIONS_LIST.issuperset(set(regions)):
            raise ValueError('Some regions included are invalid')
        params = params + (('region','|'.join(regions)),)
    if sectors is not None:
        if isinstance(sectors, str):
            sectors = [sectors]
        if not _SECTORS_LIST.issuperset(set(sectors)):
            raise ValueError('Some sectors included are invalid')
        params = params + (('sector','|'.join(sectors)),)
    if countries is not None:
        if isinstance(countries, str):
            countries = [countries]
        if not _COUNTRIES_LIST.issuperset(set(countries)):
            raise ValueError('Some countries included are invalid')
        params = params + (('country','|'.join(countries)),)
    if analystRatings is not None:
        if isinstance(analystRatings, str):
            analystRatings = [analystRatings]
        if not _ANALYST_RATINGS_LIST.issuperset(set(analystRatings)):
            raise ValueError('Some ratings included are invalid')
        params = params + (('recommendation','|'.join(analystRatings)),)
    return params


# I know it's weird to have Sectors as constants, yet the Regions as enums, but
# it makes the most sense to me
class Region:
    AFRICA = 'AFRICA'
    EUROPE = 'EUROPE'
    ASIA = 'ASIA'
    AUSTRALIA_SOUTH_PACIFIC = 'AUSTRALIA+AND+SOUTH+PACIFIC'
    CARIBBEAN = 'CARIBBEAN'
    SOUTH_AMERICA = 'SOUTH+AMERICA'
    MIDDLE_EAST = 'MIDDLE+EAST'
    NORTH_AMERICA = 'NORTH+AMERICA'

class AnalystRating:
    STRONG_BUY = 'Strong Buy'
    HOLD = 'Hold'
    BUY = 'Buy'
    SELL = 'Sell'
    STRONG_SEll = 'Strong Sell'

class Country:
    ARGENTINA = 'Argentina'
    ARMENIA = 'Armenia'
    AUSTRALIA = 'Australia'
    AUSTRIA = 'Austria'
    BELGUIM = 'Belgium'
    BERMUDA = 'Bermuda'
    BRAZIL = 'Brazil'
    CANADA = 'Canada'
    CAYMAN_ISLANDS = 'Cayman Islands'
    CHILE = 'Chile'
    COLOMBIA = 'Colombia'
    COSTA_RICA = 'Costa Rica'
    CURACAO = 'Curacao'
    CYCRUS = 'Cyprus'
    DENMARK = 'Denmark'
    FINLAND = 'Finland'
    FRANCE = 'France'
    GERMANY = 'Germany'
    GREECE = 'Greece'
    GUERNESY = 'Guernsey'
    HONG_KONG = 'Hong Kong'
    INDIA = 'India'
    INDONESIA = 'Indonesia'
    IRELAND = 'Ireland'
    ISLE_OF_MAN = 'Isle of Man'
    ISRAEL = 'Israel'
    ITALY = 'Italy'
    JAPAN = 'Japan'
    JERSEY = 'Jersey'
    LUXEMBOURG = 'Luxembourg'
    MACAU = 'Macau'
    MEXICO = 'Mexico'
    MONACO = 'Monaco'
    NETHERLANDS = 'Netherlands'
    NORWAY = 'Norway'
    PANAMA = 'Panama'
    PERU = 'Peru'
    PHILIPPINES = 'Philippines'
    PEURTO_RICO = 'Puerto Rico'
    RUSSIA = 'Russia'
    SINGAPORE = 'Singapore'
    SOUTH_AFRICA = 'South Africa'
    SOUTH_KOREA = 'South Korea'
    SPAIN = 'Spain'
    SWEDEN = 'Sweden'
    SWITZERLAND = 'Switzerland'
    TAIWAN = 'Taiwan'
    TURKEY = 'Turkey'
    UNITED_KINGDOM = 'United Kingdom'
    UNITED_STATES = 'United States'


class SectorConstants:
    NON_DURABLE_GOODS = 'Consumer Non-Durables'
    CAPITAL_GOODS = 'Capital Goods'
    HEALTH_CARE = 'Health Care'
    ENERGY = 'Energy'
    TECH = 'Technology'
    BASICS = 'Basic Industries'
    FINANCE = 'Finance'
    SERVICES = 'Consumer Services'
    UTILITIES = 'Public Utilities'
    DURABLE_GOODS = 'Consumer Durables'
    TRANSPORT = 'Transportation'

def get_tickers(NYSE=True, NASDAQ=True, AMEX=True):
    tickers_list = []
    if NYSE:
        tickers_list.extend(__exchange2list(exchange='NYSE'))
    if NASDAQ:
        tickers_list.extend(__exchange2list(exchange='NASDAQ'))
    if AMEX:
        tickers_list.extend(__exchange2list(exchange='AMEX'))
    return tickers_list


def get_tickers_filtered(NYSE=True, NASDAQ=True, AMEX=True,mktcap_min=None, mktcap_max=None, sectors=None, regions=None, countries=None, analystRatings=None):
    tickers_list = []
    if NYSE:
        tickers_list.extend(__exchange2list(exchange='NYSE', mktcap_min=mktcap_min, mktcap_max=mktcap_max, sectors=sectors, regions=regions, countries=countries, analystRatings=analystRatings))
    if NASDAQ:
        tickers_list.extend(__exchange2list(exchange='NASDAQ', mktcap_min=mktcap_min, mktcap_max=mktcap_max, sectors=sectors, regions=regions, countries=countries, analystRatings=analystRatings))
    if AMEX:
        tickers_list.extend(__exchange2list(exchange='AMEX', mktcap_min=mktcap_min, mktcap_max=mktcap_max, sectors=sectors, regions=regions, countries=countries, analystRatings=analystRatings))
    return tickers_list


def get_biggest_n_tickers(top_n, NYSE=True, NASDAQ=True, AMEX=True,mktcap_min=None, mktcap_max=None, sectors=None, regions=None, countries=None, analystRatings=None):
    df = pd.DataFrame()
    if NYSE:
        temp = __exchange2df(exchange='NYSE',regions=regions,sectors=sectors,countries=countries,analystRatings=analystRatings,mktcap_min=mktcap_min,mktcap_max=mktcap_max)
        df = pd.concat([df, temp])
    if NASDAQ:
        temp = __exchange2df(exchange='NASDAQ',regions=regions,sectors=sectors,countries=countries,analystRatings=analystRatings,mktcap_min=mktcap_min,mktcap_max=mktcap_max)
        df = pd.concat([df, temp])
    if AMEX:
        temp = __exchange2df(exchange='AMEX',regions=regions,sectors=sectors,countries=countries,analystRatings=analystRatings,mktcap_min=mktcap_min,mktcap_max=mktcap_max)
        df = pd.concat([df, temp])
    
    if df.empty:
        return []
        
    df = df.sort_values('marketCap', ascending=False)
    if top_n > len(df):
        raise ValueError('Not enough companies, please specify a smaller top_n')

    return df.iloc[:top_n]['symbol'].tolist()


def __exchange2df(exchange,regions=None,sectors=None,countries=None,mktcap_min=None,mktcap_max=None,analystRatings=None):
    response = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params(exchange=exchange,regions=regions,sectors=sectors,countries=countries,analystRatings=analystRatings))
    
    text_data= response.text
    json_dict= json.loads(text_data)
    if json_dict['data']['headers'] is None:
        return pd.DataFrame()
    columns = list(json_dict['data']['headers'].keys())
    df = pd.DataFrame(json_dict['data']['rows'], columns=columns)
    def cust_filter(mkt_cap):
        if not mkt_cap:
            return float(0.0)
        return float(mkt_cap) / 1e6
    df['marketCap'] = df['marketCap'].apply(cust_filter)
    if mktcap_min is not None:
        df = df[df['marketCap'] > mktcap_min]
    if mktcap_max is not None:
        df = df[df['marketCap'] < mktcap_max]
    return df

def __exchange2list(exchange,regions=None,sectors=None,countries=None,analystRatings=None,mktcap_min=None,mktcap_max=None):
    df = __exchange2df(exchange=exchange,regions=regions,sectors=sectors,countries=countries,analystRatings=analystRatings,mktcap_min=mktcap_min,mktcap_max=mktcap_max)
    # removes weird tickers
    #df_filtered = df[~df['symbol'].str.contains("\.|\^")]
    if df.empty:
        return []
    return df['symbol'].tolist()


# save the tickers to a CSV
def save_tickers(NYSE=True, NASDAQ=True, AMEX=True, filename='tickers.csv'):
    tickers2save = get_tickers(NYSE, NASDAQ, AMEX)
    df = pd.DataFrame(tickers2save)
    df.to_csv(filename, header=False, index=False)

def save_tickers_filtered(NYSE=True, NASDAQ=True, AMEX=True,mktcap_min=None, mktcap_max=None, sectors=None, regions=None, countries=None, analystRatings=None, filename='tickers_by_region.csv'):
    tickers2save = get_tickers_filtered(NYSE=True, NASDAQ=True, AMEX=True,mktcap_min=None, mktcap_max=None, sectors=None, regions=None, countries=None, analystRatings=None)
    df = pd.DataFrame(tickers2save)
    df.to_csv(filename, header=False, index=False)


if __name__ == '__main__':


    # tickers of all exchanges
    tickers = get_tickers()
    print(tickers[:5])

    # tickers from NYSE and NASDAQ only
    tickers = get_tickers(AMEX=False)

    # default filename is tickers.csv, to specify, add argument filename='yourfilename.csv'
    save_tickers()

    # save tickers from NYSE and AMEX only
    save_tickers(NASDAQ=False)

    # get tickers filtered by market cap (in millions)
    filtered_tickers = get_tickers_filtered(mktcap_min=500, mktcap_max=2000)
    print(filtered_tickers[:5])

    # not setting max will get stocks with $2000 million market cap and up.
    filtered_tickers = get_tickers_filtered(mktcap_min=2000)
    print(filtered_tickers[:5])

    # get tickers filtered by multiple params, None should exist
    filtered_by_sector = get_tickers_filtered(mktcap_min=200e3, sectors=[SectorConstants.FINANCE,SectorConstants.BASICS,SectorConstants.CAPITAL_GOODS],analystRatings=[AnalystRating.SELL,AnalystRating.BUY],countries=[Country.ARGENTINA])
    print(filtered_by_sector)

    # get tickers filtered by multiple params
    filtered_by_sector = get_tickers_filtered(mktcap_min=200e3, sectors=[SectorConstants.FINANCE,SectorConstants.BASICS,SectorConstants.CAPITAL_GOODS],analystRatings=[AnalystRating.SELL,AnalystRating.BUY],countries=[Country.UNITED_STATES])
    print(filtered_by_sector[:5])

    # get tickers of 5 largest companies by market cap (specify sectors=SECTOR)
    top_5 = get_biggest_n_tickers(5)
    print(top_5)