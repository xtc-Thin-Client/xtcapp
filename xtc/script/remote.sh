#!/bin/bash
if (test -e /data/thinclient/config/remoteon)
then
    /usr/bin/x11vnc -auth guess -forever -loop -noxdamage -repeat -rfbauth /data/thinclient/config/remote.pass -rfbport 5900 -shared
fi
