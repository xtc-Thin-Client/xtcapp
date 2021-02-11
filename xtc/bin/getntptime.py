#!/usr/bin/python3
import ntplib
import datetime
import sys
import pytz
from time import ctime

def getNTPTime(server, timezone):
    try:
        # get 
        client = ntplib.NTPClient()
        response = client.request(server, version=3)
        ntpTimeText = ctime(response.tx_time)
        ntpTime = datetime.datetime.strptime(ntpTimeText, "%a %b %d %H:%M:%S %Y")
        
        ctimezone = pytz.timezone(timezone)
        time = ntpTime.astimezone(ctimezone).strftime("%Y-%m-%d %H:%M:%S")
        print(time)
    except Exception as e:
        print (e)
    
if __name__ == "__main__":
    if len(sys.argv) > 2:
        #print("ntp: " + sys.argv[1])
        #print("time zone: " + sys.argv[2])
        getNTPTime(sys.argv[1], sys.argv[2])
    else:
        print("parameter required: ntp-server timezone")
        sys.exit(1)
    sys.exit(0)
