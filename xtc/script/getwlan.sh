#!/bin/bash
# get list from wlan connections
# run as root
#
# get network interfaces
FILE=/tmp/getwlan.txt
ls /sys/class/net > $FILE

while read LINE
do 
  iwlist $LINE scan 2> /dev/null | grep "ESSID:" | cut -d: -f2 | tr -d \" | sort -u 
done < $FILE
