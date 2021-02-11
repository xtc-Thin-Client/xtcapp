#!/bin/bash
# set password for ssh user
# 
PASSWD=$(cat /data/thinclient/config/sshpass)
echo thinclientssh:$PASSWD | chpasswd 2>> /dev/null
rm /data/thinclient/config/sshpass
