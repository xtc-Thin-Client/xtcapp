#!/bin/bash
# get usb automount state
# return 0 = on, 1 = off

FILE=/tmp/getusb.txt
ls /etc/usbmount/usbmount.conf > $FILE

if (test -s $FILE)  
then
  exit 0
fi

exit 1
