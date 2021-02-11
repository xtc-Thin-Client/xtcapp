#!/bin/bash
# set resolution
# $1 = resolution
sed -i "/^xrandr/d" /var/thinclient/home/thinclient/.config/openbox/autostart
if [ "$1" != "" ] && [ "$1" != "auto" ]
then
  sed -i "1 i\xrandr -s $1" /var/thinclient/home/thinclient/.config/openbox/autostart  
fi
exit 0
