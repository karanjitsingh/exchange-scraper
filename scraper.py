from datetime import datetime, timedelta
import time
import requests
import sys
import os
import argparse


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument("--date", metavar="\"YYYYMMDD\"", type=str, help="Scrape data to this date.", required=True)
parser.add_argument("--offset", metavar="integer", type=int, help="Offset end date by number of days", default=0)
parser.add_argument("--length", metavar="integer", type=int, help="Number of days to scrape to given date", default=1)
parser.add_argument("--timeframe", metavar="string", type=str, help="Candle time frame", default="1m")
parser.add_argument("--symbol", metavar="string", type=str, help="Candle time frame", default="BTCUSDT")
parser.add_argument("--delay", metavar="integer", type=str, help="Request delay in seconds", default=3)

args = vars(parser.parse_args())

print("Scraping data with config: " + str(args) + "\n")

second = 1000
minute = second * 60
hour = minute * 60
day = hour * 24

endpoint  = "https://www.binance.com/api/v1/klines?symbol={symbol}&interval={timeframe}&startTime={start}&endTime={end}&limit=2000"

date = args['date']
start = args['offset']
length = args['length']
symbol = args['symbol']
timeframe = args['timeframe']
delay = args['delay']

# Thu Aug 03 2019 00:00:00 GMT+0530 (India Standard Time)
startDate = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), 0, 0, 0, 0)
startTime = int(startDate.timestamp()*1000) 


def getDayDiff(d):
    return (startDate - timedelta(days=d)).strftime("%Y-%m-%d")
    

def getDayPairs(start, length):
    endTick = startTime - day * start
    startTick = startTime - day * start

    pairs = []

    for i in range(length):
        endTick = startTick
        startTick = startTick - day
        pairs.append([startTick, endTick, getDayDiff(i + start + 1)])

    return pairs

def requestAndDump(url, filename):
    success = True

    request = requests.get(url)
    data = request.content

    if request.status_code is 200:
        with open(filename, "w") as file:
            file.write(data.__str__()[2:-1])                
    else:
        print("Non 200 status code")
        print("Status Code:", request.status_code)
        print(request.headers)
        print(request.content)
        success = False

    return success

def scrape(start, length, dumpfolder):
    pairs = getDayPairs(start, length)
    
    for i in range(len(pairs)):
        if timeframe == "1m":
            # max number of records returned by the api is 1000 so we will have to request twice for each day
            
            print(pairs[i][2])
            url = endpoint.format(start=pairs[i][0], end=pairs[i][1]-int(day/2), timeframe=timeframe, symbol=symbol)
            
            print(url)


            if requestAndDump(url, os.path.join(dumpfolder, pairs[i][2] + ".1.json")) == True:
                url = endpoint.format(start=pairs[i][1]-int(day/2), end=pairs[i][1], timeframe=timeframe, symbol=symbol)
                print(url,"\n")

                if requestAndDump(url, os.path.join(dumpfolder, pairs[i][2] + ".2.json")) == False:
                    print("Breaking on " + pairs[i][2])
                    break  
            else:      
                print("Breaking on " + pairs[i][2])
                break

        else:
            print(pairs[i][2])
            url = endpoint.format(start=pairs[i][0], end=pairs[i][1], timeframe=timeframe, symbol=symbol)
            
            print(url)

            if requestAndDump(url, os.path.join(dumpfolder, pairs[i][2] + ".json")) == False:
                print("Breaking on " + pairs[i][2])
                break

        
        time.sleep(delay)


print("Start: {0}, End: {1} [start excluded]\n".format(getDayDiff(start), getDayDiff(start + length)))

dumpfolder = os.path.join(os.getcwd(), "dump")

if not os.path.isdir(dumpfolder):
    os.mkdir(dumpfolder)

scrape(start, length, dumpfolder)