import yfinance as yf
from get_stock_data import get_historical_market_data
from get_recommendations import get_recommendations,get_convert_type_keys
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from get_tickers import get_tickers_filtered,SectorConstants
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
import matplotlib.ticker
from datetime import date,datetime
from dateutil.relativedelta import relativedelta

def get_recommendations_performance(tickers,start,end,performance_test_period,early_stop,data_type,convert_type,verbose):

    
    convert_type_list = get_convert_type_keys(convert_type=convert_type)

    df_firm_perf = pd.DataFrame(columns=convert_type_list)
    df_time_total = pd.DataFrame(columns=convert_type_list)

    if verbose:
        print('Total tickers: '+str(len(tickers)))

    for tick in tickers:
        if verbose:
            print("Geting data for ticker: " + tick + "...")
        
        #get historical data
        data = get_historical_market_data(ticker = tick,start=start,end=end,interval='1d',data_type=data_type)
        data['Date'] = data.index

        # make sure no nan or inf values exists, replace nan values will most recent value unless value is first is dataframe then replace with next value
        data = data.replace(np.inf, np.nan)
        data = data.fillna(method='ffill')
        data = data.fillna(method='bfill')

        #no data
        if len(data.index) == 0:
            continue

        #get recommendations
        recommendations_df = get_recommendations(ticker=tick,convert_type=convert_type)
        #no recommendations for stock
        if recommendations_df is None:
            continue
        recommendations_df['Date'] = recommendations_df.index

        #get list of firms
        yf_firms_set = set(recommendations_df['Firm'].values)
        firm_list = list(yf_firms_set)
        
        #add firms not already in datafram
        for firm in firm_list:
            if firm not in df_firm_perf.index:
                df_firm_perf = df_firm_perf.append(pd.Series(name=firm,dtype=np.dtype(float)))
                df_time_total = df_time_total.append(pd.Series(name=firm,dtype=np.dtype(float)))

        results = []
        
        if early_stop:

            #create dictionary which groups all firms recommendations together
            yf_recommendations_dict = {}
            for yf_firm in firm_list:
                yf_recommendations_dict[yf_firm] = recommendations_df.loc[recommendations_df['Firm'] == yf_firm]
            

            for firm in yf_recommendations_dict.keys():
                firm_recommendations = yf_recommendations_dict[firm]

                last_date_df = 0
                last_to_grade_df = 0
                wait_once = True
                for date_df, to_grade_df in zip(firm_recommendations['Date'],firm_recommendations['To Grade']):
                    
                    if wait_once:
                        last_date_df = date_df
                        last_to_grade_df = to_grade_df
                        wait_once = False
                        continue
                    else:
                        
                        result = calculate_performance(data=data,performance_test_period=performance_test_period,date=last_date_df, next_date=date_df, firm=firm, to_grade=last_to_grade_df)
                        
                        last_date_df = date_df
                        last_to_grade_df = to_grade_df
                        results.append(result)
                result = calculate_performance(data=data,performance_test_period=performance_test_period,date=last_date_df, next_date=None, firm=firm, to_grade=last_to_grade_df)
                results.append(result) 
        else:
            results = [calculate_performance(data=data,performance_test_period=performance_test_period,date=date_df, next_date=None, firm=firm_df, to_grade=to_grade_df) for date_df, firm_df, to_grade_df in zip(recommendations_df['Date'], recommendations_df['Firm'],recommendations_df['To Grade'])]
            
        for result in results:
                if result is not None:
                    performance = result[0]
                    firm = result[1]
                    grade = result[2]
                    time_dif = result[3]
                    
                    if grade is not 'Invalid' and grade is not 'Dont Include':
                        
                        if not isinstance(df_firm_perf.at[firm,grade],np.ndarray):
                            df_firm_perf.at[firm,grade] = np.array([performance])
                            df_time_total.at[firm,grade] = np.array([time_dif])
                        else:
                            temp_val_1 = df_firm_perf.at[firm,grade]
                            temp_val_2 = df_time_total.at[firm,grade]
                            df_firm_perf.at[firm,grade] = np.append(temp_val_1,performance)
                            df_time_total.at[firm,grade] = np.append(temp_val_2,time_dif)

    return df_firm_perf,df_time_total


def calculate_performance(data,performance_test_period,date,next_date,firm,to_grade):

    start_date = date
    end_date = date + relativedelta(months=+performance_test_period)

    if next_date is not None:
        if next_date < end_date:
            end_date = next_date

    #test if recommendation is in test range
    if len(data.index) == 0:
        return None
    if start_date < data.iloc[0]['Date']:
        return None
    elif end_date > data.iloc[-1]['Date']:
        return None

    #get difference in seconds between start date and data dates
    data['dif_start_date'] = abs(data['Date'] - start_date)
    data['dif_end_date'] = abs(data['Date'] - end_date)

    start_index = data['dif_start_date'].idxmin()
    end_index = data['dif_end_date'].idxmin()

    start_value_df = data.loc[[start_index]]
    end_value_df = data.loc[[end_index]]

    start_value = start_value_df['Close'].values[0]
    end_value = end_value_df['Close'].values[0]

    performance = (end_value - start_value)/start_value
    #get time between start and end in seconds
    time_dif_sec = (end_date.value-start_date.value)/1000000000.0
    return [performance,firm,to_grade,time_dif_sec]
        

"""
    start:
        look at data past start date 'YYYY-MM-DD'
        
    end:
        look at data up until end date 'YYYY-MM-DD'

    performance_test_period:
        integer
            number of months until recommendation performance is tested
            
    early_stop:
        True: test every recommendation until end of performance_test_period or until new recommendation, whichever comes first

        False: test every recommendation until end of performance_test_period

    data_type
        price: return price

    metric
        mean: return mean rate of return of a firms stock picks, only use with normal convert_type

        geometric mean: return geometric average rate of return of a firms stock picks

    min_recommendations
        dictionary: min number of recommendations for each recommndation type respectively. Firms without min for any recommendation type will be removed. Example {Strong Buy:0,Buy:10,Hold:10,Sell:10,Strong Sell:0}
        int: min number of total recommendations for all types. Firms without min recommendations will be removed Example: 10

    convert_type 
        normal:  convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            includes all recommednation types
        simple:  convert recommendations to {Sell, Hold, Buy} 
            groups more confident recommedations together
        reduced: convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            same as normal but doesnt consider 'longer-term buy', 'specultive buy', 'specultive sell'

    save
        str: location to save dataframe as csv
        None: to not save

    verbose
        True: print number of tickers and when each ticker is gathering data
        False: dont print info
    
"""

def measure_firm_performance(tickers=[],start='2012-01-01',end='2020-01-01',data_type='price',performance_test_period=24,early_stop=True,metric='geometric mean',convert_type='simple',min_recommendations=21,save=None,verbose=False):
    convert_keys = get_convert_type_keys(convert_type=convert_type)
    if metric == 'mean' and early_stop:
        raise Warning('calculating average rate of return over variable period lengths will yield bad results')
    if isinstance(min_recommendations, dict):
        if convert_type == 'normal' and len(min_recommendations) != 5:
            raise ValueError('Normal recommendation convertion has 5 types need min recommendation dictionary to have 5 integer values')
        if convert_type == 'reduced' and len(min_recommendations) != 5:
            raise ValueError('Reduced recommendation convertion has 5 types need min recommendation dictionary to have 5 integer values')
        if convert_type == 'simple' and len(min_recommendations) != 3:
            raise ValueError('Simple recommendation convertion has 3 types need min recommendation dictionary to have 3 integer values')
        if set(min_recommendations.keys()) != set(convert_keys):
            raise ValueError('Invalid value for some min_recommendation key')
    if metric != 'mean' and metric != 'geometric mean':
        raise ValueError('Invalid metric')
    if (not isinstance(performance_test_period,int)) or performance_test_period <= 0:
        raise ValueError('Invalid performance_test_period')

    df_firm_perf,df_time_total = get_recommendations_performance(tickers=tickers,start=start,end=end,performance_test_period=performance_test_period,early_stop=early_stop,data_type=data_type,convert_type=convert_type,verbose=verbose)

    df_new_firm_perf = df_firm_perf.copy()
    for firm_name,firm_perf in df_firm_perf.iterrows():
        
        #count number of recommendations
        found = False
        if isinstance(min_recommendations, dict):
            for rec in min_recommendations:
                if not isinstance(firm_perf[rec],np.ndarray):
                    if min_recommendations[rec] > 0:
                        df_new_firm_perf.drop([firm_name],inplace=True)
                        found = True
                        break
                elif len(firm_perf[rec]) < min_recommendations[rec]:
                    df_new_firm_perf.drop([firm_name],inplace=True)
                    found = True
                    break
        if isinstance(min_recommendations, int):
            total_recommendations = 0
            for rec in convert_keys:
                if isinstance(firm_perf[rec],np.ndarray):
                    total_recommendations = total_recommendations + len(firm_perf[rec])
            if total_recommendations < min_recommendations:
                df_new_firm_perf.drop([firm_name],inplace=True)
                found = True

        if found:
            continue

        for rec in convert_keys:

            if isinstance(firm_perf[rec],np.ndarray):

                #array of performances based on recommendation
                perf_array = firm_perf[rec]

                #calculate average rate of return needs 
                if metric == 'mean':
                    arr = np.array([])
                    #get yearly rate of return 
                    for perf in perf_array:
                        ret = np.power(perf+1.0,12.0/performance_test_period)-1.0
                        arr = np.append(arr,ret)
                    me = np.mean(arr)
                    df_new_firm_perf.at[firm_name,rec] = me
                
                #calculate geometric average rate of return 
                elif metric == 'geometric mean':

                    arr = np.array([])
                    for perf in perf_array:
                        arr = np.append(arr,perf+1.0)

                    #first get log to prevent overflow
                    arr_log = np.log(arr)
                    sum_log = np.sum(arr_log)

                    #get total time in seconds 
                    time_of_investments = np.sum(df_time_total.at[firm_name,rec])
                    #get return per year
                    seconds_in_year = 31622400.0
                    geometric_avg_log = sum_log*seconds_in_year/time_of_investments
                    geometric_avg = np.exp(geometric_avg_log)

                    geometric_avg_return = geometric_avg-1.0

                    df_new_firm_perf.at[firm_name,rec] = geometric_avg_return

    if save is not None:
        df_new_firm_perf.to_csv(save)

    return df_new_firm_perf

"""
    data
        from measure_firm_performance
    recommendation
        (Strong Sell, Sell, Hold, Buy, Stong Buy)
    metric
        'max': best return for given key 
        'min': worst return for given key

"""
def rank_performance(df_firm_performance,recommendation,metric):
    
    if metric == 'max':
        df_ranked = df_firm_performance.sort_values(recommendation,ascending=False)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
            print(df_ranked)
        return df_ranked
    elif metric == 'min':
        df_ranked = df_firm_performance.sort_values(recommendation,ascending=True)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
            print(df_ranked)
        return df_ranked


"""
    graph_type:
        'histogram': plot histogram of recommendation performance for a firm (early_stop must be False)
        '1d': plot 1d eventplot graph of recommendation performance (early_stop must be False)
        '2d': plot 2d graph of time vs return recommendation performance (early_stop must be True)

    start:
        look at data past start date 'YYYY-MM-DD'
        
    end:
        look at data up until end date 'YYYY-MM-DD'

    performance_test_period:
        integer
            number of months until recommendation performance is tested
    
    early_stop:
        True: test every recommendation until end of performance_test_period or until new recommendation, whichever comes first

        False: test every recommendation until end of performance_test_period

    data_type
        price: return price

    min_recommendations
        dictionary: min number of recommendations for each recommndation type respectively. Firms without min for any recommendation type will be removed.      Example {Strong Buy:0,Buy:10,Hold:10,Sell:10,Strong Sell:0}
        int: min number of total recommendations for all types. Firms without min recommendations will be removed Example: 10

    convert_type 
        normal:  convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            includes all recommednation types
        simple:  convert recommendations to {Sell, Hold, Buy} 
            groups more confident recommedations together
        reduced: convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} 
            same as normal but doesnt consider 'longer-term buy', 'specultive buy', 'specultive sell'

    verbose
        True: print number of tickers and when each ticker is gathering data
        False: dont print info
    
"""

def graph_performance(graph_type='histogram',tickers=[],start='2012-01-01',end='2020-01-01',performance_test_period=24,data_type='price',early_stop=False,min_recommendations=21,convert_type='simple',verbose=False):
    if early_stop and graph_type !='2d':
        raise ValueError('Can only suppot graph type 2d when early stop is true')
    if graph_type !='1d' and graph_type !='histogram' and graph_type !='2d':
        raise ValueError('Invalid graph_type')
    convert_keys = get_convert_type_keys(convert_type=convert_type)
    if isinstance(min_recommendations, dict):
        if convert_type == 'normal' and len(min_recommendations) != 5:
            raise ValueError('Normal recommendation convertion has 5 types need min recommendation dictionary to have 5 integer values')
        if convert_type == 'reduced' and len(min_recommendations) != 5:
            raise ValueError('Reduced recommendation convertion has 5 types need min recommendation dictionary to have 5 integer values')
        if convert_type == 'simple' and len(min_recommendations) != 3:
            raise ValueError('Simple recommendation convertion has 3 types need min recommendation dictionary to have 3 integer values')
        if set(min_recommendations.keys()) != set(convert_keys):
            raise ValueError('Invalid value for some min_recommendation key')
    if (not isinstance(performance_test_period,int)) or performance_test_period <= 0:
        raise ValueError('Invalid performance_test_period')

    df_firm_perf,df_time_total = get_recommendations_performance(tickers=tickers,start=start,end=end,performance_test_period=performance_test_period,early_stop=early_stop,data_type=data_type,convert_type=convert_type,verbose=verbose)

    df_new_firm_perf = df_firm_perf.copy()
    if graph_type == 'histogram':
        plt.style.use('seaborn-deep')
    for firm_name,firm_perf in df_firm_perf.iterrows():
        
        #count number of recommendations
        found = False
        if isinstance(min_recommendations, dict):
            for rec in min_recommendations:
                if not isinstance(firm_perf[rec],np.ndarray):
                    if min_recommendations[rec] > 0:
                        df_new_firm_perf.drop([firm_name],inplace=True)
                        found = True
                        break
                elif len(firm_perf[rec]) < min_recommendations[rec]:
                    df_new_firm_perf.drop([firm_name],inplace=True)
                    found = True
                    break
        if isinstance(min_recommendations, int):
            total_recommendations = 0
            for rec in convert_keys:
                if isinstance(firm_perf[rec],np.ndarray):
                    total_recommendations = total_recommendations + len(firm_perf[rec])
            if total_recommendations < min_recommendations:
                df_new_firm_perf.drop([firm_name],inplace=True)
                found = True

        if found:
            continue
        
        if graph_type=='2d':
            plt.title(firm_name)
            colors = {}   
            if len(convert_keys) == 5:
                colors = {'Strong Sell':'darkred','Sell':'red','Hold':'gold','Buy':'lightgreen','Strong Buy':'green'}
            if len(convert_keys) == 3:
                colors = {'Sell':'red','Hold':'gold','Buy':'green'}
            inc = 0
            patches = []
            
            for rec in convert_keys:

                if isinstance(firm_perf[rec],np.ndarray):

                    price_sum_log_values = np.array([0.0])
                    time_sum_values = np.array([0.0])

                    #array of performances based on recommendation
                    perf_array = firm_perf[rec]
                    time_array = df_time_total.at[firm_name,rec]

                    
                    #get total time in seconds 
                    time_of_investments = np.sum(df_time_total.at[firm_name,rec])

                    for perf,time in zip(perf_array,time_array):
                        price_sum_log_values = np.append(price_sum_log_values,price_sum_log_values[-1]+np.log(perf+1))
                        time_sum_values = np.append(time_sum_values,time_sum_values[-1]+time/time_of_investments)

                    
                    
                    seconds_in_year = 31622400.0
                    price_geo_avg_log_values = price_sum_log_values*seconds_in_year/time_of_investments
                    price_geo_avg_values = np.exp(price_geo_avg_log_values)

                    #price_geo_avg_values = price_geo_avg_values-1.0

                    #plot data
                    patch = mpatches.Patch(color=colors[rec], label=rec)
                    patches.append(patch)
                    
                    plt.plot(time_sum_values,price_geo_avg_values,color=colors[rec])  # Draw a horizontal line
                    
                        
                    inc = inc + 1
            plt.yscale('log')
            plt.gca().yaxis.set_minor_formatter(matplotlib.ticker.ScalarFormatter())
            plt.legend(handles=patches)  
            plt.show()

        
        
        elif graph_type == '1d':
            plt.figure()
            plt.title(firm_name)
            colors = {}   
            if len(convert_keys) == 5:
                colors = {'Strong Sell':'darkred','Sell':'red','Hold':'gold','Buy':'lightgreen','Strong Buy':'green'}
            if len(convert_keys) == 3:
                colors = {'Sell':'red','Hold':'gold','Buy':'green'}
            inc = 0
            patches = []
            
            for rec in convert_keys:
                if isinstance(firm_perf[rec],np.ndarray):

                    #array of performances based on recommendation
                    perf_array = firm_perf[rec]

                    #calculate average rate of return needs 
                    arr = np.array([])
                    #get yearly rate of return 
                    for perf in perf_array:
                        ret = np.power(perf+1.0,12.0/performance_test_period)-1.0
                        arr = np.append(arr,ret)

                    patch = mpatches.Patch(color=colors[rec], label=rec)
                    patches.append(patch)
                    
                    plt.vlines(arr,0,5-inc,colors=colors[rec])  # Draw a horizontal line
                        
                    inc = inc + 1
                
            plt.legend(handles=patches)  
            plt.xlim(-1, 2)
            frame1 = plt.gca()
            frame1.axes.get_yaxis().set_visible(False)
            plt.show()

        elif graph_type == 'histogram':
            color_dict = {}  
            plots = None
            fig = None
            if len(convert_keys) == 5:
                color_dict = {'Strong Sell':'#8b0000','Sell':'#ff0000','Hold':'#daa520','Buy':'#90ee2c','Strong Buy':'#00ff00'}
                fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(25,7))
                plots = (ax1, ax2, ax3, ax4, ax5)
            elif len(convert_keys) == 3:
                color_dict = {'Sell':'#ff0000','Hold':'#daa520','Buy':'#00ff00'}
                fig, (ax1, ax2, ax3) = plt.subplots(1, 3 , figsize=(25,7))
                plots = (ax1, ax2, ax3)
            inc = 0
            patches = []
            rec_values = []
            weights = []
            
            
            fig.suptitle(firm_name)
            inc = 0
            for rec in convert_keys:
                if isinstance(firm_perf[rec],np.ndarray):

                    #array of performances based on recommendation
                    perf_array = firm_perf[rec]
                    
                    patch = mpatches.Patch(color=color_dict[rec], label=rec)
                    patches.append(patch)

                    #calculate average rate of return needs 
                    x = np.array([])
                    #get yearly rate of return 
                    for perf in perf_array:
                        ret = np.power(perf+1.0,12.0/performance_test_period)-1.0
                        x = np.append(x,ret)
                    #get weight 
                    x_w = np.empty(x.shape)
                    x_w.fill(1/x.shape[0])
                    #get mean
                    me = np.mean(x)

                    #set sub plot title
                    plots[inc].set(xlabel=rec+" Avg: "+ str(me))

                    #graph histogram
                    plots[inc].hist(x, 60, weights=x_w, color=color_dict[rec])
                    inc = inc + 1

            #plt.legend(handles=patches)  
            plt.show()
                



if __name__ == '__main__':
    
    #Tests

    #get recommendations of firms for stocks with 50 billion market cap or more
    measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=True,data_type='price',metric='geometric mean',min_recommendations={'Sell': 10,'Hold': 10,'Buy': 10},convert_type='simple',save='analyst_recommendation_performance/TestResults/Test1.csv',verbose=True)

    #get recommendations of firms for stocks with 10 billion to 20 billion market cap
    measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=10e3,mktcap_max=20e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=True,data_type='price',metric='geometric mean',min_recommendations={'Sell': 10,'Hold': 10,'Buy': 10},convert_type='simple',save='analyst_recommendation_performance/TestResults/Test2.csv',verbose=True)
    
    #get recommendations of firms for stocks with 1 billion market cap or more, and in Basic Industries Sector
    measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=1e3,sectors=SectorConstants.BASICS),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=True,data_type='price',metric='geometric mean',min_recommendations={'Sell':10,'Hold':10,'Buy':10},convert_type='simple',save='analyst_recommendation_performance/TestResults/Test3.csv',verbose=True)
    
    #get recommendations of firms for stocks with 50 billion market cap or more, using a performance test period of 12
    measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3),start='2012-01-01',end='2020-01-01',performance_test_period=12,early_stop=True,data_type='price',metric='geometric mean',min_recommendations={'Sell':10,'Hold':10,'Buy':10},convert_type='simple',save='analyst_recommendation_performance/TestResults/Test4.csv',verbose=True)
    
    #get recommendations of firms for stocks with 50 billion market cap or more, using no early stop
    measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=False,data_type='price',metric='geometric mean',min_recommendations={'Sell':10,'Hold':10,'Buy':10},convert_type='simple',save='analyst_recommendation_performance/TestResults/Test5.csv',verbose=True)
    
    #get recommendations of firms for stocks with 50 billion market cap or more, using 'mean' metric
    measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=False,data_type='price',metric='mean',min_recommendations={'Sell':10,'Hold':10,'Buy':10},convert_type='simple',save='analyst_recommendation_performance/TestResults/Test6.csv',verbose=True)
    
    #get recommendations of firms for stocks with 50 billion market cap or more, using convert type 'normal'
    measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=True,data_type='price',metric='geometric mean',min_recommendations={'Strong Sell': 0,'Sell':10,'Hold':10,'Buy':10,'Strong Buy': 0},convert_type='normal',save='analyst_recommendation_performance/TestResults/Test7.csv',verbose=True)
    