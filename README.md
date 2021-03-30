# analyst-recommendation-performance

# Overview

Knowing whether or not to heed the advice of a stock analyst when they downgrade a stock you own from buy to sell can be quite difficult, the stock might move down the same day this recommendation is announced but knowing whether or not this analyst will be right in the long term is unclear. Many analysts issue dozens of recommendations a year so tracking their historical performance may shed light on the importance of these recommendations. This library hopes to solve this problem by offering highly tunable functions that help measure analyst performance analytically and visually.

The ratings and pricing data are acquired by using the https://github.com/ranaroussi/yfinance library which scrapes ratings that appear on yahoo finance.

## Methods and Classes

### measure_firm_performance
```
measure_firm_performance(tickers=[],start='2012-01-01',end='2020-01-01',data_type='price',performance_test_period=24,early_stop=True,metric='geometric mean',convert_type='simple',min_recommendations=21,save=None,verbose=False)
```
Returns a Pandas Dataframe containing analysts performance for each type of recommendation type. Performance of stocks are outputed as annualized returns<br/>

Examples:<br/>
```
measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=True,data_type='price',metric='geometric mean',min_recommendations={'Sell': 10,'Hold': 10,'Buy': 10},convert_type='simple',save=None,verbose=False)
```
| | Sell | Hold | Buy
| --- | --- | --- | --- |
Citigroup | 0.14204269121582458 | 0.1627528422825344 | 0.1719686059278489
Exane BNP Paribas | 0.11300793616919114 | 0.061475516840060696 | 0.15501559957925193
Morgan Stanley | 0.18573949998646522 | 0.15942064641583298 | 0.16579152921044082
Jefferies | 0.15652834063350274 | 0.14629528374389777 | 0.18744852892435349
Goldman Sachs | 0.16085049838551346 | 0.19718270892442535 | 0.1786451198461767
RBC Capital | 0.20671859255546443 | 0.15505565022400325 | 0.1560254934995522
HSBC | 0.06821985504601868 | 0.09450416071257983 | 0.1158054177218486
JP Morgan | 0.18197844352780956 | 0.154352767138628 | 0.12134505675443119
Barclays | 0.1614429975769771 | 0.17573689484076183 | 0.21838722145869593
Credit Suisse | 0.11240540278031697 | 0.16436763166842105 | 0.18076744041378823
Deutsche Bank | 0.15476809888062149 | 0.17169487743727685 | 0.18264527661881602
Berenberg | 0.18013773848320036 | 0.11080378609458075 | 0.10770237070686739
Nomura | 0.14059635418241312 | 0.17715279020081898 | 0.191814660721759
UBS | 0.13044422500948039 | 0.15036908929531778 | 0.18128971153033202
Societe Generale | 0.10870565918456854 | 0.10002269482831916 | 0.09082864636286736
Bank of America | 0.22500898520525747 | 0.14388660392217667 | 0.1538129439990148
BMO Capital | 0.12123144278100129 | 0.16530603205073602 | 0.18353669710332454
Atlantic Equities | 0.16545413799129727 | 0.17714232525330065 | 0.1807617548444147
ISI Group | 0.35238092906215335 | 0.17876675445110712 | 0.12865477390577507
Bernstein | 0.19418210153950688 | 0.14576118129495508 | 0.16846495316094345
Standpoint Research | 0.10851544963865933 | 0.16620013173090364 | 0.27239684450279
Cantor Fitzgerald | 0.3401267079507577 | 0.18702997592007442 | 0.2087820169647736
Pacific Crest | 0.29100878275515196 | 0.2194417183625763 | 0.27617568339748555
Wedbush | 0.3952764905316153 | 0.2581466844237046 | 0.21827112784477265
Macquarie | 0.2229338292648324 | 0.1768223184252471 | 0.15699016907313768
Keefe Bruyette & Woods | 0.13667645861095834 | 0.20706073546129256 | 0.11817065130614157

### graph_performance
```
graph_performance(graph_type='histogram',tickers=[],start='2012-01-01',end='2020-01-01',performance_test_period=24,data_type='price',early_stop=False,min_recommendations=21,convert_type='simple',verbose=False)
```
Outputs graph as either histogram or 2d plot, based on graph_type. Results are annualized<br/>

Examples:<br/>
CDF Graph:
```
graph_performance(graph_type='cdf',tickers=get_tickers_filtered(mktcap_min=30e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,data_type='price',early_stop=True,min_recommendations={'Sell': 10,'Hold': 10,'Buy': 10},convert_type='simple',verbose=False)
```
![Citigroup CDF](https://user-images.githubusercontent.com/30188191/112922221-1dabca00-90da-11eb-96da-44cc543a89f2.PNG)
Histogram Graph:
```
graph_performance(graph_type='histogram',tickers=get_tickers_filtered(mktcap_min=30e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,data_type='price',early_stop=False,min_recommendations={'Sell': 25,'Hold': 25,'Buy': 25},convert_type='simple',verbose=False)
```
![histogram](https://user-images.githubusercontent.com/30188191/112783478-6c475e80-901d-11eb-8f2c-62934c78ba5f.PNG)

## Params

Since there are many non-intuitive parameters I will go into detail about each one below.

### tickers
In order to get recommendations, one must specify which tickers they want the recommendation to come from. A larger set is preferable to get a large sample size of recommendations. I have included the library https://github.com/dbondi/get_all_tickers to make it easy to search for a large number of tickers based on various filters.
```
measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3))
```
### start and end
Only recommendations that fall between these dates will be analyzed.
```
measure_firm_performance(start='2012-01-01',end='2020-01-01')
```
### data_type
'price': The performance of a stock is measured by the percent change in the price.
```
measure_firm_performance(data_type='price')
```
### performance_test_period
Integer type representing number of months after a recommendation is announced when performance is measured
```
measure_firm_performance(performance_test_period=12)
```
### early_stop
True: Test every recommendation until the end of ***performance_test_period*** or until a new recommendation by the same analyst is announced, whichever comes first.<br/>
False: Test every recommendation until end of ***performance_test_period***.<br/>

```
measure_firm_performance(early_stop=True)
```

### metric
'mean': returns mean rate of return of an analyst's stock picks, only should be used when 'early_stop' is False as one should measure performance over a constant length of time to get valid results.<br/>
'geometric mean': returns geometric average rate of return.
```
measure_firm_performance(metric='geometric mean')
```

### convert_type
I have found 49 different terms analysts use to represent their recommendation for a stock, this library maps these terms to a smaller and more general set of terms. These are the various mapping conventions that the user can choose from. <br/>

normal:  convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} includes all recommendation types<br/>
simple:  convert recommendations to {Sell, Hold, Buy} groups more confident recommendations together<br/>
reduced: convert recommendations to {Strong sell, Sell, Hold, Buy, Strong Buy} same as normal but doesn't consider 'longer-term buy', 'speculative buy', 'speculative sell'<br/>
```
measure_firm_performance(convert_type='simple')
```
### min_recommendations
dictionary: min number of recommendations for each recommendation type respectively. Firms without min for any recommendation type will be removed.<br/>
int: min number of total recommendations for all types. Firms without min recommendations will be removed<br/>
```
measure_firm_performance(min_recommendations={Strong Buy:0,Buy:10,Hold:10,Sell:10,Strong Sell:0})
```
```
measure_firm_performance(min_recommendations=21)
```

### save
This is only used by **measure_firm_performance**<br/>
str: location to save dataframe as csv<br/>
None: to not save<br/>
```
measure_firm_performance(save='analyst_recommendation_performance/TestResults/Test1.csv')
```

### verbose
True: print number of tickers and when each ticker is gathering data<br/>
False: don't print info
```
measure_firm_performance(verbose=True)
```

### graph_type
This is only used by **graph_performance**<br/>
'cdf': cdf plot of anualized rate of return<br/>
'2d': plot 2d graph of time vs return recommendation performance annualized. <br/>
'histogram': plot analyst recommendation performance on histogram graph  (***early_stop*** must be False)<br/>
'1d': plot 1d eventplot graph of recommendation performance (***early_stop*** must be False)
