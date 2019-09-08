from datetime import datetime, timedelta
import time
import requests
import sys
import os

second = 1000
minute = second * 60
hour = minute * 60
day = hour * 24

endpoint  = "https://www.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1m&startTime={0}&endTime={1}&limit=2000"

# Thu Aug 03 2019 00:00:00 GMT+0530 (India Standard Time)
startDate = datetime(2019, 8, 3, 0, 0, 0, 0)
startTime = 1564770600000

print(startTime)

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
        # max number of records returned by the api is 1000 so we will have to request twice for each day
        
        print(pairs[i][2])
        url = endpoint.format(pairs[i][0], pairs[i][1]-int(day/2))
        
        print(url)

        if requestAndDump(url, os.path.join(dumpfolder, pairs[i][2] + ".1.json")) == True:
            url = endpoint.format(pairs[i][1]-int(day/2), pairs[i][1])
            print(url,"\n")

            if requestAndDump(url, os.path.join(dumpfolder, pairs[i][2] + ".2.json")) == False:
                print("Breaking on " + pairs[i][2])
                break  
        else:      
            print("Breaking on " + pairs[i][2])
            break

        time.sleep(3)

start = 0 if len(sys.argv) == 1 else int(sys.argv[1])
length = 1 if len(sys.argv) == 1 else int(sys.argv[2])

print("Start: {0}, End: {1} [start excluded]\n".format(getDayDiff(start), getDayDiff(start + length)))

dumpfolder = os.path.join(os.getcwd(), "dump")

if not os.path.isdir(dumpfolder):
    os.mkdir(dumpfolder)

scrape(start, length, dumpfolder)