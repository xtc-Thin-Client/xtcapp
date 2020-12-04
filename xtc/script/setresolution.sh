#!/bin/bash
# set resolution
# $1 = resolution

OS="U"
if (cat /etc/issue | grep -i "RASPBIAN" > /dev/null)
then 
  OS="R"
fi

if [ "$OS" = "R" ]
then
  sed -i "/^hdmi_group=/d" /boot/config.txt
  sed -i "/^hdmi_mode=/d" /boot/config.txt
  
  if [ "$1" != "" ]
  then
    echo "hdmi_group=2" >> /boot/config.txt
    echo "hdmi_mode="$1 >> /boot/config.txt
  fi   
else
  sed -i "/^xrandr/d" /var/thinclient/home/thinclient/.config/openbox/autostart
  if [ "$1" != "" ]
  then
    sed -i "1 i\xrandr -s $1" /var/thinclient/home/thinclient/.config/openbox/autostart  
  fi
fi
exit 0
