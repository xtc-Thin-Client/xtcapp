#!/bin/bash
# get usb automount state
# return 0 = on, 1 = off

FILEIN=/etc/usbmount/usbmount.conf
if (test -s $FILEIN)
then 
  FILEOUT=/tmp/getusb.txt
  ls $FILEIN > $FILEOUT

  if (test -s $FILEOUT)  
  then
    exit 0
  fi
fi

exit 1
