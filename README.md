# analyst-recommendation-performance
 
Knowing whether or not to heed the anvice of a stock analyst when they downgrade a stock you own from buy to sell can be quite difficult, the stock might move down the same day this recommendation is announced but knowing whether or not this analyst will be right in the long term is unclear. Many analyst issue many dozens of recommendations a year so tracking their historical performance may shed light on the importance of this recommendations. This library hopes to solve this problem by offering highly tunable functions that help measure performance analytically and visually.

## Ratings

The ratings are acquired by using the https://github.com/ranaroussi/yfinance library which scrapes ratings that appear on yahoo finance. 

I have found 49 different terminologies analysts use to represent their recommendation for a stock this library maps these terms to a smaller and more general set of terms Examples: {Strong Sell, Sell, Hold, Buy, Strong Buy}, {Sell, Hold, Buy}, this library allows for multiple mapping conventions that the user can choose from. 

## Schemes for Measuring Performance

The performance of a stock is measured by the percent change in a given metric, right now just price, from the start to the end of a given period. The start of the period is which the recommendation is given; the users has two options for when the end of the period should occur, 1. When a certain length of time is reached. 2. When a certian length of time is reach or when a new recommendation from the same analyst is given, which ever comes first. 

If the first option is choosen then the performance of all recommendations will be over a constant length of time this means its sensible to measure the total performance with either the mean of a the analysts recommendations or the geometic mean of a the analysts recommendations.

If the second option is choosen then the performance of an analysts recommendations will be over different lengths of time so its only sensible to measure the time weighted geometic mean.

Note: The second option seems to be the better choice as analysts typically issue changes to stock recommendations and the fairest way to measure performance is probably by acting accordingly to new recommendations.


Right now the library only looks at stock price to measure the performance however in the future I plan on implementing EPS and Peter Lynch's fair value metric.

