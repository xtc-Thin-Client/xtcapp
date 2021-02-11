#!/bin/bash
# if date and time is displayed?
# result:
# 0 = yes
# 1 = no

if (grep "^panel_items = LTSC" /home/thinclient/.config/tint2/tint2rc > /dev/null)
then
  exit 0
fi
exit 1
