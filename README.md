# analyst-recommendation-performance

# Overview

Knowing whether or not to heed the advice of a stock analyst when they downgrade a stock you own from buy to sell can be quite difficult, the stock might move down the same day this recommendation is announced but knowing whether or not this analyst will be right in the long term is unclear. Many analysts issue dozens of recommendations a year so tracking their historical performance may shed light on the importance of these recommendations. This library hopes to solve this problem by offering highly tunable functions that help measure analyst performance analytically and visually.

The ratings and pricing data are acquired by using the https://github.com/ranaroussi/yfinance library which scrapes ratings that appear on yahoo finance.

## Methods and Classes

### measure_firm_performance
```
measure_firm_performance(tickers=[],start='2012-01-01',end='2020-01-01',data_type='price',performance_test_period=24,early_stop=True,metric='geometric mean',convert_type='simple',min_recommendations=21,save=None,get_upgrade_downgrade=False,verbose=False)
```
Returns a Pandas Dataframe containing analysts performance for each type of recommendation type. Performance of stocks are outputed as annualized returns<br/>

Examples:<br/>
```
measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=50e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,early_stop=True,data_type='price',metric='geometric mean',min_recommendations={'Sell': 10,'Hold': 10,'Buy': 10},convert_type='simple',save=None,get_upgrade_downgrade=False,verbose=False)
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

```
measure_firm_performance(tickers=get_tickers_filtered(mktcap_min=20e3),start='2012-01-01',end='2020-01-01',performance_test_period=12,early_stop=False,data_type='price',metric='geometric mean',min_recommendations={'Sell': 30,'Hold': 30,'Buy': 30},convert_type='simple',save='analyst_recommendation_performance/TestResults/Test8.csv',get_upgrade_downgrade=True,verbose=True)
```
| | Sell | Hold | Buy | Hold->Sell | Hold->Buy | Buy->Hold | Sell->Hold | Sell->Buy | Buy->Sell
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Barclays | 0.1260078377645648 | 0.1494940902798929 | 0.168217547525783 | 0.23267765835160734 | 0.5272752219863128 | 0.464442908147265 | 0.2849725347860505 | 0.0003694849757559037 | 0.41419745484352327
Goldman Sachs | 0.16557655867333043 | 0.17417795021143556 | 0.18194731275056086 | -0.2809262461635094 | -0.09254716654998557 | 0.1787391957395673 | 0.5495495392292364 | 0.05429457515975649 | 0.0
Deutsche Bank | 0.20047941382062318 | 0.1429075993945692 | 0.15320976088248695 | 0.2964788131111358 | 0.20148645158952008 | -0.31004919827262334 | 0.5028666967700792 | 0.0 | -0.03243363215047216
Jefferies | 0.21143178759058068 | 0.14438471182255053 | 0.1708756606586963 | 0.2416457723621814 | 0.051571592879336686 | -0.06926389674636374 | 0.13228771623776375 | -0.043175598443716615 | 0.0
Bank of America | 0.19578635158254754 | 0.13505808351945814 | 0.13299104128333017 | 0.11290366214838006 | 0.36049378948447147 | 0.007084989135835188 | 0.49831160337329533 | 0.6468544955531657 | 0.3009621988685336
KeyBanc | 0.1599163305794935 | 0.15173009159248263 | 0.15298305631053166 | -0.3001296403633887 | -0.2853029990867131 | 0.001196134206122592 | 0.5799840282471589 | 0.0 | 0.0
Credit Suisse | 0.18591775598653704 | 0.16636707509680182 | 0.1436736722569394 | 0.3465328736193766 | 0.464442908147265 | -0.07512083654101444 | -0.09253627411379678 | 0.36965439052284343 | -0.434950673422577
Morgan Stanley | 0.12939123444070266 | 0.11843035803006807 | 0.1510072579799817 | 0.3260645593766388 | 0.3927521177269992 | 0.4356471189347443 | 0.2014550571877913 | -0.0005181880628928266 | -0.1349811425464924
UBS | 0.17934665164004437 | 0.1573234953586724 | 0.1888359696526294 | 0.0914395862471426 | 0.053231718410226794 | 0.18634619113037265 | 0.1995780775058912 | -0.2632286692950752 | 0.8139737250877088
JP Morgan | 0.12663225132798694 | 0.14558329188771335 | 0.13623499105494807 | 0.4882479062093058 | 0.9814482034489252 | 0.13968005366004266 | 0.439676486411518 | -0.16020464817685529 | -0.0017116320109910059
Citigroup | 0.14113826398471652 | 0.14246237353775926 | 0.12371564203248697 | 0.5274327469288537 | -0.12953106493098104 | 0.3802817752734498 | 0.4470087781108582 | -0.14954558409667026 | 0.8897157342000527
Societe Generale | 0.1132147015870606 | 0.11732541454859491 | 0.12380980622020554 | 0.1536051289780185 | 0.025136719617822892 | 0.01172010256809176 | 0.15761694217522826 | 0.06347038460530752 | -0.08772337953553724
Nomura | 0.17116083077360789 | 0.19239886106811643 | 0.16656645629979172 | 0.19760437480544082 | 0.06705941860081255 | 0.2612367759594828 | 0.7356475134062344 | 1.2583629260845397 | 1.1933721226289213
HSBC | 0.05179528033168079 | 0.09528655785403517 | 0.049796249935006864 | 0.6024489110829879 | 0.10544610077759582 | 0.2104661137146924 | -0.05145485366467471 | 0.12260171738207024 | 0.18580203698203218
Bernstein | 0.18641645674608043 | 0.15016853563595745 | 0.15303035400505127 | 0.5509176362800722 | 0.602785769430048 | 0.45909360095400215 | 0.11495400696839454 | -0.047437769960126594 | 0.0
BMO Capital | 0.12205297846642504 | 0.16879081193379508 | 0.19321585936198082 | 0.07496061421387443 | 0.27448659949233734 | 0.02906141672706251 | -0.08900703189407551 | 1.0529676860616024 | 0.0
Cantor Fitzgerald | 0.22548294361445853 | 0.18817130194456522 | 0.20749018922779605 | -0.3406982703832159 | 0.4955216281525279 | 0.7098216681713222 | 0.2564102185533623 | 0.0 | 0.22456412203669315
Pacific Crest | 0.16801828570646604 | 0.21948116923423844 | 0.2002381500548136 | -0.034145074994767294 | -0.07374182021134253 | -0.21190033913925863 | 1.07174090121519 | 0.029173890085070885 | 0.0
Macquarie | 0.10943040570136198 | 0.11680777972949574 | 0.12556051918816524 | 0.12527910227431682 | -0.26378692343496823 | -0.4271656688639499 | 0.5267604887158392 | 0.46792451506112603 | 0.0

### graph_performance
```
graph_performance(graph_type='histogram',tickers=[],start='2012-01-01',end='2020-01-01',performance_test_period=24,data_type='price',early_stop=False,min_recommendations=21,convert_type='simple',verbose=False)
```
Outputs graph as either histogram or 2d plot, based on graph_type. Results are annualized<br/>

Examples:<br/>

CDF Graph<br/>
```
graph_performance(graph_type='cdf',tickers=get_tickers_filtered(mktcap_min=30e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,data_type='price',early_stop=True,min_recommendations={'Sell': 10,'Hold': 10,'Buy': 10},convert_type='simple',verbose=False)
```
![Citigroup CDF](https://user-images.githubusercontent.com/30188191/112922221-1dabca00-90da-11eb-96da-44cc543a89f2.PNG)<br/>

Histogram Graph:
```
graph_performance(graph_type='histogram',tickers=get_tickers_filtered(mktcap_min=30e3),start='2012-01-01',end='2020-01-01',performance_test_period=24,data_type='price',early_stop=False,min_recommendations={'Sell': 25,'Hold': 25,'Buy': 25},convert_type='simple',verbose=False)
```
![histogram](https://user-images.githubusercontent.com/30188191/112783478-6c475e80-901d-11eb-8f2c-62934c78ba5f.PNG)

## Params

Since there are many parameters I will go into detail about each one below.

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

### get_upgrade_downgrade
This is only used by **measure_firm_performance**<br/>
True: Output additional columns that indicate the rate of return when a recommendation type changes, for example one column might be Hold->Sell, which indicates the rate of return after a firm downgrades a stock from hold to sell. Note: this is only measured once, if the next recommendation is the same it wont be factored into the rate of return<br/>
False: Dont output additional columns
```
measure_firm_performance(get_upgrade_downgrade=True)
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
'histogram': plot analyst recommendation performance anualized on histogram graph  (***early_stop*** must be False)<br/>
'1d': plot 1d eventplot graph of recommendation performance anualized (***early_stop*** must be False)
