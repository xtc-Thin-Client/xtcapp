#!/bin/bash
# configure system by file 
if (test -s /data/thinclient/connection.config)
then
  mv /data/thinclient/connection.config /data/thinclient/connection.conf
  chown thinclient:thinclient /data/thinclient/connection.conf  
fi
if (test -s /data/thinclient/thinclient.config)
then
  # run configuration app
  /opt/thinclient/script/system.sh /data/thinclient/thinclient.config
  mv /data/thinclient/thinclient.config /data/thinclient/thinclient.config.save
  # reboot system to complete configuration
  shutdown -r now
fi
exit 0
