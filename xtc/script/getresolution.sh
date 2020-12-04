#!/bin/bash
# get resolution

OS="U"
if (cat /etc/issue | grep -i "RASPBIAN" > /dev/null)
then
  OS="R"
fi

if [ "$OS" = "R" ]
then
  grep "^hdmi_mode=" /boot/config.txt | cut -d"=" -f2
  
else
  xrandr --current | grep "*" | awk '{print $1}'
fi
exit 0
