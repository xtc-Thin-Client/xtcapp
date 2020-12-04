#!/bin/bash
# set state for oneninedesign power case
# $1 = on/off

FILE=/boot/config.txt
COMMAND1="dtoverlay=gpio-poweroff"
COMMAND2="dtoverlay=gpio-shutdown"
RESULT=$(grep "$COMMAND1" $FILE)
if (test -s $FILE)
then
  # delete shutdown command
  sed -i "/$COMMAND1/d" $FILE    
  sed -i "/$COMMAND2/d" $FILE    
  
  # insert shutdown command
  if [ "$1" = "on" ]
  then
      echo >> $FILE
      echo "dtoverlay=gpio-poweroff,gpiopin=18,active_low=0" >> $FILE
      echo "dtoverlay=gpio-shutdown,gpio_pin=17,active_low=1,gpio_pull=up" >> $FILE
      echo "" >> $FILE
    fi
  fi
fi
exit 0
