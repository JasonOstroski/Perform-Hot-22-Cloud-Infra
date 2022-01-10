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
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'east-us', 'team' : 'teamA'}, 'min' : 1000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'east-us-2', 'team' : 'teamB'}, 'min' : 2000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'central-us', 'team' : 'teamD'}, 'min' : 1000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'west-central-us', 'team' : 'teamE'}, 'min' : 2000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'west-us', 'team' : 'teamF'}, 'min' : 2000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-east-2', 'team' : 'teamA'}, 'min' : 1000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-east-1', 'team' : 'teamA'}, 'min' : 2000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-west-1', 'team' : 'teamB'}, 'min' : 1000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-west-2', 'team' : 'teamB'}, 'min' : 2000, 'max' : 5000 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'af-south-1', 'team' : 'teamC'}, 'min' : 1000, 'max' : 5000 }
    ]

METRICS = [
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'east-us', 'team' : 'teamA'}, 'min' : 80, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'east-us-2', 'team' : 'teamB'}, 'min' : 70, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'central-us', 'team' : 'teamD'}, 'min' : 90, 'max' : 100},
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'west-central-us', 'team' : 'teamE'}, 'min' : 90, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'Azure', 'region' : 'west-us', 'team' : 'teamF'}, 'min' : 40, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-east-2', 'team' : 'teamA'}, 'min' : 10, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-east-1', 'team' : 'teamA'}, 'min' : 50, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-west-1', 'team' : 'teamB'}, 'min' : 10, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'us-west-2', 'team' : 'teamB'}, 'min' : 70, 'max' : 100 },
        {'id' : 'cloud.costestimate', 'dims' : {'provider' : 'AWS', 'region' : 'af-south-1', 'team' : 'teamC'}, 'min' : 20, 'max' : 100 }
    ]
scheduler = sched.scheduler(time.time, time.sleep)

def genSeries():
    mStr = ""
    now = datetime.now()
    timenow = int(now.strftime("%H%M"))
    if (timenow > int(droptime)) and (timenow < (int(droptime) + duration)):
        CURR_METRICS=METRICS_DROP
        print("Simulating cost increase...")
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
