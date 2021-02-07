# exchange-scraper
CLI tool for scraping binance data

### Prereq

```
pip install argparse
```

### Run Scraper

#### Usage
```bash
>>> python .\scraper.py --date "20201228"

Scraping data with config: {'date': '20201228', 'offset': 0, 'length': 1, 'timeframe': '15m', 'symbol': 'BTCUSDT', 'delay': 3}

Start: 2020-12-28, End: 2020-12-27 [start excluded]

2020-12-27
https://www.binance.com/api/v1/klines?symbol=BTCUSDT&interval=15m&startTime=1609007400000&endTime=1609093800000&limit=2000
```

#### Options

```bash
>>> python .\scraper.py --help
usage: scraper.py [-h] --date "YYYYMMDD" [--offset integer] [--length integer]
                  [--timeframe string] [--symbol string] [--delay integer]

optional arguments:
  -h, --help          show this help message and exit
  --date "YYYYMMDD"   Scrape data to this date.
  --offset integer    Offset end date by number of days
  --length integer    Number of days to scrape to given date
  --timeframe string  Candle time frame
  --symbol string     Candle time frame
  --delay integer     Request delay in seconds
```

### Time gap analysis in scraped data

```bash
>>>python .\gapanalysis.py --path .\data\BINANCE_BTCUSDT_15m\ --time 15
Gap: lastTime: [1529977500000, '2018-06-26.json', 29]  Current:  [1530014400000, '2018-06-26.json', 30] Difference:  615.0
Gap: lastTime: [1530103500000, '2018-06-27.json', 73]  Current:  [1530110700000, '2018-06-27.json', 74] Difference:  120.0
Gap: lastTime: [1530663300000, '2018-07-04.json', 23]  Current:  [1530691200000, '2018-07-04.json', 24] Difference:  465.0
Gap: lastTime: [1539927900000, '2018-10-19.json', 45]  Current:  [1539941400000, '2018-10-19.json', 46] Difference:  225.0
Gap: lastTime: [1542159900000, '2018-11-14.json', 29]  Current:  [1542186000000, '2018-11-14.json', 30] Difference:  435.0
Gap: lastTime: [1552355100000, '2019-03-12.json', 29]  Current:  [1552377600000, '2019-03-12.json', 30] Difference:  375.0
Gap: lastTime: [1557888300000, '2019-05-15.json', 33]  Current:  [1557925200000, '2019-05-15.json', 34] Difference:  615.0
Gap: lastTime: [1559941200000, '2019-06-08.json', 10]  Current:  [1559945700000, '2019-06-08.json', 11] Difference:  75.0
Gap: lastTime: [1565833500000, '2019-08-15.json', 29]  Current:  [1565863200000, '2019-08-15.json', 30] Difference:  495.0
Gap: lastTime: [1573609500000, '2019-11-13.json', 29]  Current:  [1573618500000, '2019-11-13.json', 30] Difference:  150.0
Gap: lastTime: [1574646300000, '2019-11-25.json', 29]  Current:  [1574654400000, '2019-11-25.json', 30] Difference:  135.0
Gap: lastTime: [1581212700000, '2020-02-09.json', 29]  Current:  [1581217200000, '2020-02-09.json', 30] Difference:  75.0
Gap: lastTime: [1582111800000, '2020-02-19.json', 68]  Current:  [1582133400000, '2020-02-19.json', 69] Difference:  360.0
Gap: lastTime: [1583313300000, '2020-03-04.json', 59]  Current:  [1583321400000, '2020-03-04.json', 60] Difference:  135.0
Gap: lastTime: [1587779100000, '2020-04-25.json', 29]  Current:  [1587789000000, '2020-04-25.json', 30] Difference:  165.0
Gap: lastTime: [1593308700000, '2020-06-28.json', 29]  Current:  [1593322200000, '2020-06-28.json', 30] Difference:  225.0
Gap: lastTime: [1606715100000, '2020-11-30.json', 45]  Current:  [1606719600000, '2020-11-30.json', 46] Difference:  75.0
Gap: lastTime: [1608559200000, '2020-12-21.json', 78]  Current:  [1608573600000, '2020-12-21.json', 79] Difference:  240.0
Gap: lastTime: [1608860700000, '2020-12-25.json', 29]  Current:  [1608865200000, '2020-12-25.json', 30] Difference:  75.0
```


### Binance REST APIs

https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#klinecandlestick-data

#### Interpreting the response

```
[
  [
    1499040000000,      // Open time
    "0.01634790",       // Open
    "0.80000000",       // High
    "0.01575800",       // Low
    "0.01577100",       // Close
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
]
```
