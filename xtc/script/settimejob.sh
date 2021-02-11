#!/bin/bash
# get ntp time and set periodic
# $1 = ntp server
# $2 = time zone

while true;
do
  TIME=$(/opt/thinclient/bin/getntptime.py $1 $2)
  date -s "$TIME"
  sleep 3600
done
