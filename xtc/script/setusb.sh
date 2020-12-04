#!/bin/bash
# set usb automount state
# $1 = "on", "off"

if [ "$1" = "on" ]
then
  if (test -f /etc/usbmount/usbmount.conf.off)
  then
    mv /etc/usbmount/usbmount.conf.off /etc/usbmount/usbmount.conf
  fi   
else
  if (test -f /etc/usbmount/usbmount.conf)
  then
    mv /etc/usbmount/usbmount.conf /etc/usbmount/usbmount.conf.off
  fi  
fi

exit 0
