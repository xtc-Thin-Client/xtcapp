#!/bin/bash
# get wpa file
cp /etc/wpa_supplicant/wpa_supplicant.conf $1 2> /dev/null
chmod a=rw $1 2> /dev/null
