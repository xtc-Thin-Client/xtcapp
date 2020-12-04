#!/bin/bash
# $1 = ovpn file
# $2 = output
# $3 = parameter/user
# $4 = user/password
# $5 = password
#
PARAM=""
USERNAME=""
PASSWORD=""

if (($# == 2))
then
  OVPN=$1
  OUT=$2
fi

if (($# == 3))
then 
  OVPN=$1
  OUT=$2
  if [ "$PARAM" != "" ]
  then
    PARAM="--config "$3
  fi
fi

if (($# == 4))
then 
  OVPN=$1
  OUT=$2
  USERNAME=$3
  PASSWORD=$4
fi

if (($# == 5))
then 
  OVPN=$1
  OUT=$2
  if [ "$PARAM" != "" ]
  then
    PARAM="--config "$3
  fi
  USERNAME=$4
  PASSWORD=$5
fi

USERFILE=""
FILE=/tmp/openvpn.user
if [ "$USERNAME" != "" ]
then
  echo $USERNAME > $FILE
  echo $PASSWORD >> $FILE
  USERFILE="--auth-user-pass "$FILE
fi

cd /data/vpn
openvpn --config $OVPN $PARAM $USERFILE >$OUT 2>&1
rm $FILE
