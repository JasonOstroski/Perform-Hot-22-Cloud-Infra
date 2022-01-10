#Parms
#python3 ingest_business_shop_revenue_drop_agent.py <start_time> <duration>
#<start_time> business metric will start dropping daily at start-time for <duration> minutes
import requests, time, sched, random, datetime, sys
from datetime import datetime

#Configure if you want to use the public Rest endpoint for metric ingest
#YOUR_DT_API_URL = 'https://<tenant-URL>'
#YOUR_DT_API_TOKEN = '<API_TOKEN>'

# datetime object containing current date and time
now = datetime.now()
timenow = int(now.strftime("%H%M"))

if (len(sys.argv) > 1):
    droptime = int(sys.argv[1])
    duration = int(sys.argv[2])
else:
    droptime = 0
    duration = 10

print("Current time: " + str(timenow))
print("Start simulation at: " + str(droptime) + " for " + str(duration) + " minutes")

METRICS_DROP = [
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Charlotte', 'store' : 'shop1'}, 'min' : 100000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Jacksonville', 'store' : 'shop2'}, 'min' : 50000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Indianapolis', 'store' : 'shop3'}, 'min' : 10000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Columbus', 'store' : 'shop4'}, 'min' : 20000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'NewYork', 'store' : 'shop5'}, 'min' : 40000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'SanFrancisco', 'store' : 'shop6'}, 'min' : 80000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'Seatle', 'store' : 'shop7'}, 'min' : 70000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'SanDiego', 'store' : 'shop8'}, 'min' : 90000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'Portland', 'store' : 'shop9'}, 'min' : 70000, 'max' : 100000 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'Anaheim', 'store' : 'shop10'}, 'min' : 90000, 'max' : 100000 }
    ]

METRICS = [
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Charlotte', 'store' : 'shop1'}, 'min' : 10, 'max' : 800 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Jacksonville', 'store' : 'shop2'}, 'min' : 5, 'max' : 900 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Indianapolis', 'store' : 'shop3'}, 'min' : 15, 'max' : 940 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'Columbus', 'store' : 'shop4'}, 'min' : 20, 'max' : 700 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'useast', 'city' : 'NewYork', 'store' : 'shop5'}, 'min' : 40, 'max' : 900 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'SanFrancisco', 'store' : 'shop6'}, 'min' : 80, 'max' : 1200 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'Seatle', 'store' : 'shop7'}, 'min' : 70, 'max' : 1300 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'SanDiego', 'store' : 'shop8'}, 'min' : 90, 'max' : 1400 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'Portland', 'store' : 'shop9'}, 'min' : 77, 'max' : 1500 },
        {'id' : 'retail.shop.responsetime', 'dims' : {'country' : 'us', 'region' : 'uswest', 'city' : 'Anaheim', 'store' : 'shop10'}, 'min' : 95, 'max' : 1100 }
    ]
scheduler = sched.scheduler(time.time, time.sleep)

def genSeries():
    mStr = ""
    now = datetime.now()
    timenow = int(now.strftime("%H%M"))
    if (timenow > int(droptime)) and (timenow < (int(droptime) + duration)):
        CURR_METRICS=METRICS_DROP
        print("Simulating response time increase...")
    else:
        CURR_METRICS=METRICS  
    for metric in CURR_METRICS:
        dimStr = ""
        for dK in metric['dims']:
            dimStr += "," + dK + "=" + metric['dims'][dK]
        mStr += metric['id'] + dimStr + " " + str(random.randint(metric['min'], metric['max'])) + "\n"
    return mStr


def doit():
    scheduler.enter(60, 1, doit)
    payload = genSeries()
    print(payload)
    #Ingest via localhost and OneAgent channel
    r = requests.post('http://localhost:14499/metrics/ingest', headers={'Content-Type': 'text/plain; charset=utf-8'}, data=payload)
    #Ingest via Public API endpoint
    #r = requests.post(YOUR_DT_API_URL + '/api/v2/metrics/ingest', headers={'Content-Type': 'text/plain', 'Authorization' : 'Api-Token ' + YOUR_DT_API_TOKEN}, data=payload)
    print(r)
    print(r.text)

print("START")
scheduler.enter(1, 1, doit)
scheduler.run()
