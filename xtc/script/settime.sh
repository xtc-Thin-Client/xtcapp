#!/bin/bash
# set time

CONFIG=/data/thinclient/config/time.conf

if (grep "save=no" $CONFIG)
then 
  exit 0
fi

TIME="20-01-01 00:00:00"

if (grep "automatic=yes" $CONFIG)
then
  NTP=$(grep "ntp=" $CONFIG | cut -d= -f2)
  if [ "$NTP" = "" ]
  then
    NTP="ptbtime1.ptb.de"
  fi
  TIMEZONE=$(grep "zone=" $CONFIG | cut -d= -f2)
  if [ "$TIMEZONE" == "" ]
  then
    TIMEZONE="UTC"
  fi    
  TIME=$(/opt/thinclient/bin/getntptime.py $NTP $TIMEZONE)
else
  RESULT=$(grep "time=" $CONFIG | cut -d= -f2)
  if [ "$RESULT" != "" ]  
  then
    TIME=$RESULT
  fi
fi

date -s "$TIME"
if (grep "automatic=yes" $CONFIG)
then
  /opt/thinclient/script/settimejob.sh $NTP $TIMEZONE &
fi
exit 0
