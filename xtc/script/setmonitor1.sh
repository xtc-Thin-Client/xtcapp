#!/bin/bash

if (test -e /data/thinclient/config/multimonitor)
then
  if (test -e /data/thinclient/dispsetup.sh)
  then
    sh /data/thinclient/dispsetup.sh
  fi
  MONITOR1=$(/opt/thinclient/script/getmonitor.sh 1)
  MONITOR2=$(/opt/thinclient/script/getmonitor.sh 2)  
 echo $MONITOR1
echo $MONITOR2 
  if [ "$MONITOR2" = "" ]
  then
    exit 0
  fi
  
  ORIENTATION=$(grep "orientation=" /data/thinclient/config/multimonitor | cut -d= -f2)
  RESOLUTION=$(grep "resolution=" /data/thinclient/config/multimonitor | cut -d= -f2)
  
  # set resolution for monitor 2
  MODE=""
  if [ "$RESOLUTION" != "" ]
  then
    MODE="--output "$MONITOR2" --mode "${RESOLUTION}
  fi
  if [ "$RESOLUTION" = "auto" ]
  then
    MODE="--output "$MONITOR2" --auto"
  fi
 echo $MODE 
  case $ORIENTATION in 
  left)
      xrandr --output $MONITOR1 --left-of $MONITOR2 $MODE
      ;;
  right)
      xrandr --output $MONITOR1 --right-of $MONITOR2 $MODE
      ;;
  above)
      xrandr --output $MONITOR1 --above $MONITOR2 $MODE
      ;;
  below)
      xrandr --output $MONITOR1 --below $MONITOR2 $MODE
      ;;   
  esac
fi
exit 0
