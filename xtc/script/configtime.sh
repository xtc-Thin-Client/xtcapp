#!/bin/bash
# run before shutdown. 
# started from savereboot.sh
# do: set date and time in panale, set time zone, set ntp on/off

CONFIGTMP=/data/thinclient/config/time
SHOW=$(grep "show=" $CONFIGTMP)
if [ "$SHOW" = "show=yes" ]
then
  sed "s/^panel_items =.*$/panel_items = LTSC/" -i /var/thinclient/home/thinclient/.config/tint2/tint2rc
else
  sed "s/^panel_items =.*$/panel_items = LTS/" -i /var/thinclient/home/thinclient/.config/tint2/tint2rc
fi

exit 0
