#!/bin/bash
# Install xtc 
#
SOURCE=`dirname $0`
rm $SOURCE/install.err 2> /dev/null
DIR=/home/thinclient
DESTINATION=/opt/thinclient
VAR=/var/thinclient
DATA=/data
echo "* start installation"
MODEL=""
OS="U"
if (cat /etc/issue | grep -i "RASPBIAN")
then
  OS="R"
  # detect pi hardware 
  MODEL=$(cat /proc/cpuinfo |grep "Revision" | cut -d: -f2 | sed 's/^[ \t]*//')
  if [ "$MODEL" = "a22082" ] || [ "$MODEL" = "a220a0" ] || [ "$MODEL" = "a32082" ] || [ "$MODEL" = "a52082" ] || [ "$MODEL" = "a22083" ] || [ "$MODEL" = "a02100" ] || [ "$MODEL" = "a020d3" ] || [ "$MODEL" = "a2082" ] || [ "$MODEL" = "a20a0" ]
  then
    MODEL="PI3"
  else
    MODEL="PI4"
  fi
fi

echo "System:" $OS
echo "Model:" $MODEL

echo "1. install packages"
apt-get update > $SOURCE/install.out
echo "   - install ssh"
apt-get -y install ssh >> $SOURCE/install.out
echo "   - install sshpass"
apt-get -y install sshpass >> $SOURCE/install.out
echo "   - install nfs-client"
apt-get -y install nfs-client >> $SOURCE/install.out
echo "   - install fbi"
apt-get -y install fbi >> $SOURCE/install.out
if [ "$OS" = "R" ]
then
  echo "   - install xorg"
  apt-get -y install xorg >> $SOURCE/install.out
else
  echo "   - install xserver-xorg-core"
  apt-get -y install xserver-xorg-core >> $SOURCE/install.out
fi
echo "   - install x11vnc"
apt-get -y install x11vnc >> $SOURCE/install.out
echo "   - install openbox"
apt-get -y install openbox >> $SOURCE/install.out 
if [ "$OS" = "U" ]
then
  echo "   - install xinit"
  apt-get -y install xinit >> $SOURCE/install.out
fi
echo "   - install tint2"
apt-get -y install tint2 >> $SOURCE/install.out 
echo "   - install wmctrl"
apt-get -y install wmctrl >> $SOURCE/install.out 
echo "   - install qt5-default"
apt-get -y install qt5-default >> $SOURCE/install.out
echo "   - install python3-pyqt5"
apt-get -y install python3-pyqt5 >> $SOURCE/install.out 
echo "   - install xbase-clients"
apt-get -y install xbase-clients >> $SOURCE/install.out 
echo "   - install tightvncserver"
apt-get -y install tightvncserver >> $SOURCE/install.out 
#echo "   - install xtightvncviewer"
#apt-get -y install xtightvncviewer >> $SOURCE/install.out
echo "   - install tigervnc-viewer"
apt-get -y install tigervnc-viewer >> $SOURCE/install.out
echo "   - install freerdp2-x11"
apt-get -y install freerdp2-x11 >> $SOURCE/install.out
echo "   - install rdesktop"
apt-get -y install rdesktop >> $SOURCE/install.out
echo "   - install xserver-xephyr"
apt-get -y install xserver-xephyr >> $SOURCE/install.out
echo "   - install pyhoca-cli"
apt-get -y install pyhoca-cli >> $SOURCE/install.out
echo "   - install openvpn"
apt-get -y install openvpn >> $SOURCE/install.out
# used by usbmount
echo "   - install lockfile-progs"
apt-get -y install lockfile-progs >> $SOURCE/install.out
echo "   - install usbmount"
if [ "$OS" = "R" ]
then
  # original usbmount is defect
  dpkg -i $SOURCE/usbmount_0.0.24_all.deb
else
  apt-get -y install usbmount >> $SOURCE/install.out
fi
# delete pulseaudio while problems with also sound
apt-get -y remove pulseaudio

echo "2. start ssh"
systemctl disable ssh > /dev/null 2>&1

echo "3. add user"
adduser --disabled-password --gecos "" thinclient 2>> $SOURCE/install.err
echo thinclient:thinclient | chpasswd 2>> $SOURCE/install.err
usermod -a -G users thinclient 2>> $SOURCE/install.err
usermod -a -G video thinclient 2>> $SOURCE/install.err
rmdir /home/thinclient/Desktop
rmdir /home/thinclient/Documents
rmdir /home/thinclient/Downloads
rmdir /home/thinclient/Music
rmdir /home/thinclient/Pictures
rmdir /home/thinclient/Public
rmdir /home/thinclient/Templates
rmdir /home/thinclient/Videos
adduser --disabled-password --gecos "" system 2>> $SOURCE/install.err
echo system:system | chpasswd 2>> $SOURCE/install.err
usermod -a -G users system 2>> $SOURCE/install.err
usermod -a -G video system 2>> $SOURCE/install.err

echo "4. create restore files"
mkdir /thinclient_restore 2>> $SOURCE/install.err
cp /etc/fstab /thinclient_restore 2>> $SOURCE/install.err
if [ "$OS" = "U" ]
then
  cp /etc/netplan/* /thinclient_restore 2>> $SOURCE/install.err
else
  cp /etc/dhcpcd.conf /thinclient_restore
  cp /etc/resolv.conf /thinclient_restore
  cp /etc/wpa_supplicant/wpa_supplicant.conf /thinclient_restore
fi
cp /lib/systemd/system/getty@.service /thinclient_restore 2>> $SOURCE/install.err
cp /etc/xdg/openbox/menu.xml /thinclient_restore 2>> $SOURCE/install.err
cp /etc/default/keyboard /thinclient_restore 2>> $SOURCE/install.err
cp $DIR/.bashrc /thinclient_restore 2>> $SOURCE/install.err
cp /etc/xdg/openbox/rc.xml /thinclient_restore 2>> $SOURCE/install.err
cp /etc/usbmount/usbmount.conf /thinclient_restore 2>> $SOURCE/install.err

echo "5. config sudo"
cat /etc/sudoers $SOURCE/sudoers.txt > /tmp/sudoers 2>> $SOURCE/install.err 
mv /tmp/sudoers /etc/sudoers 2>> $SOURCE/install.err

echo "6. autologin"
sed -e 's/^ExecStart=.*$/ExecStart=-\/sbin\/agetty --noclear --autologin thinclient %I $TERM/g' -i /lib/systemd/system/getty@.service 2>> $SOURCE/install.err

echo "7. config openbox"
cp $SOURCE/menu.xml /etc/xdg/openbox 2>> $SOURCE/install.err
mkdir $DIR/.config 2>> $SOURCE/install.err
mkdir $DIR/.config/openbox 2>> $SOURCE/install.err
cp $SOURCE/autostart $DIR/.config/openbox 2>> $SOURCE/install.err
cp $SOURCE/rc.xml /etc/xdg/openbox 2>> $SOURCE/install.err

echo "8. config tint2"
mkdir $DIR/.config/tint2 2>> $SOURCE/install.err
cp $SOURCE/tint2rc $DIR/.config/tint2 2>> $SOURCE/install.err
chown -R thinclient $DIR/.config 2>> $SOURCE/install.err
chgrp -R thinclient $DIR/.config 2>> $SOURCE/install.err

echo "9. config user thinclient"
cat $DIR/.bashrc $SOURCE/bashrc.txt > /tmp/bashrc 2>> $SOURCE/install.err 
mv /tmp/bashrc $DIR/.bashrc 2>> $SOURCE/install.err
chown thinclient $DIR/.bashrc
chgrp thinclient $DIR/.bashrc

echo "10. install thinclient"
mkdir $DESTINATION 2>> $SOURCE/install.err  
cp -a $SOURCE/bin $DESTINATION 2>> $SOURCE/install.err
cp -a $SOURCE/config $DESTINATION 2>> $SOURCE/install.err  
cp -a $SOURCE/script $DESTINATION 2>> $SOURCE/install.err
cp -a $SOURCE/desktop $DESTINATION 2>> $SOURCE/install.err
if [ "$OS" = "U" ]
then
  cp -a $SOURCE/script/ubuntu/tightvncpasswd $DESTINATION/script 2>> $SOURCE/install.err
else
  cp -a $SOURCE/script/raspbian/tightvncpasswd $DESTINATION/script 2>> $SOURCE/install.err
fi
ln -s $DESTINATION/script/thinclient.sh /usr/bin/thinclient 

echo "11. create var directory"
mkdir $VAR 2>> $SOURCE/install.err
mkdir $VAR/home 2>> $SOURCE/install.err

echo "12. save home directory"
cp -a /home/thinclient $VAR/home
chown -R thinclient $VAR 2>> $SOURCE/install.err
chgrp -R thinclient $VAR 2>> $SOURCE/install.err

echo "13. install start script"
cp $SOURCE/thinclient_start /etc/init.d 2>> $SOURCE/install.err
update-rc.d thinclient_start defaults

echo "14. install shutdown script"
cp $SOURCE/thinclient_shutdown /etc/init.d 2>> $SOURCE/install.err
update-rc.d thinclient_shutdown defaults

echo "15. install splashscreen"
cp $SOURCE/splashscreen.png $VAR
cp $SOURCE/splashscreen.service /etc/systemd/system
systemctl enable splashscreen

echo "16. create data directory"
mkdir $DATA 2>> /dev/null

echo "17. mount data directory"
if [ "$OS" = "R" ]
then
  cat /etc/fstab $SOURCE/fstab_data > /tmp/fstab
  mv /tmp/fstab /etc/fstab
  mount -a
fi

echo "18. config data directory"
chmod a=rwx $DATA 2>> /dev/null
mkdir $DATA/thinclient 2>> $SOURCE/install.err
chown thinclient $DATA/thinclient 2>> $SOURCE/install.err
chgrp thinclient $DATA/thinclient 2>> $SOURCE/install.err
mkdir $DATA/vpn 2>> $SOURCE/install.err
chown thinclient $DATA/vpn 2>> $SOURCE/install.err
chgrp thinclient $DATA/vpn 2>> $SOURCE/install.err
mkdir $DATA/usb 2>> $SOURCE/install.err
chown thinclient $DATA/usb 2>> $SOURCE/install.err
chgrp thinclient $DATA/usb 2>> $SOURCE/install.err

echo "19. config read only fs"
if [ "$OS" = "R" ]
then
  sed '/\/ /s/defaults/ro,defaults/g' -i /etc/fstab
  sed '/\/boot/s/defaults/ro,defaults/g' -i /etc/fstab
  cat /etc/fstab $SOURCE/fstab_ro > /tmp/fstab
  mv /tmp/fstab /etc/fstab
fi

echo "20. edit boot options (Rasberry Pi only)"
if [ "$OS" = "R" ]
then
  cp /boot/cmdline.txt /thinclient_restore 2>> $SOURCE/install.err
  # Use no swap, disable Raspberry pi logi, disable kernel output
  # Parameter net.ifnames=0 for /etc/network/interfaces with Raspbian Stretch
  sed 's/$/ noswap logo.nologo consoleblank=0 net.ifnames=0 loglevel=1 quiet/' -i /boot/cmdline.txt
fi

echo "21. config monitor and sound (Rasberry Pi only)"
if [ "$OS" = "R" ]
then
  cp /boot/config.txt /thinclient_restore 2>> $SOURCE/install.err
  sed 's/^#disable_overscan/disable_overscan/' -i /boot/config.txt
  # set Raspberry Pi to HDMI mode even if no HDMI monitor is detected
  sed 's/^#hdmi_force_hotplug=/hdmi_force_hotplug=/' -i /boot/config.txt
  # send sound to hdmi 
  sed 's/^#hdmi_drive=/hdmi_drive=/' -i /boot/config.txt
  # enable monitor stand by
  echo "hdmi_blanking=1" >> /boot/config.txt
  # disable Raspberry Pi color test
  echo "disable_splash=1" >> /boot/config.txt
fi

echo "22. delete user pi (Rasberry Pi only)"
if [ "$OS" = "R" ]
then
  deluser pi 2>> $SOURCE/install.err
  rm -rf /home/pi
fi

echo "23. install driver for pi desktop case (Raspbery Pi 3 only)"
if [ "$OS" = "R" ]
then
  dpkg -i /opt/thinclient/desktop/pidesktop-base.deb
  echo " " >> /boot/config.txt
  echo " " >> /boot/config.txt
  cp $SOURCE/desktop/pidesktop.sh $DESTINATION/desktop
  cp $SOURCE/desktop/pidesktop-powerkey.service /lib/systemd
  cp $SOURCE/desktop/pidesktop-reboot.service /lib/systemd
  cp $SOURCE/desktop/pidesktop-shutdown.service /lib/systemd
  cp $SOURCE/desktop/pidesktop-powerkey.service /etc/systemd/system
  cp $SOURCE/desktop/pidesktop-reboot.service //etc/systemd/system
  cp $SOURCE/desktop/pidesktop-shutdown.service /etc/systemd/system
  chown root:root $DESTINATION/desktop/pidesktop.sh
  chown root:root /lib/systemd/pidesktop-powerkey.service 
  chown root:root /lib/systemd/pidesktop-reboot.service
  chown root:root /lib/systemd/pidesktop-shutdown.service
  chown root:root /etc/systemd/system/pidesktop-powerkey.service 
  chown root:root /etc/systemd/system/pidesktop-reboot.service
  chown root:root /etc/systemd/system/pidesktop-shutdown.service
fi

echo "24. disable GL driver (Raspberry Pi 4 only)"
if [ "$OS" = "R" ] && [ "$MODEL" = "PI4" ]
then
  # Raspberry Pi 4: disable GL driver
  sed 's/^dtoverlay=/#dtoverlay=/' -i /boot/config.txt
fi

echo "25. install software for argon1 case (Raspberry Pi 4 only)"
if [ "$OS" = "R" ]
then
  $SOURCE/desktop/argon1.sh
  systemctl disable argononed
fi

echo "26. configure usb automount"
sed 's/^FS_MOUNTOPTIONS=/FS_MOUNTOPTIONS="-fstype=vfat,user=000,dmask=0000,fmask=0000,gid=thinclient,uid=thinclient"/' -i /etc/usbmount/usbmount.conf
# deactivate automount
mv /etc/usbmount/usbmount.conf /etc/usbmount/usbmount.conf.off

echo "* End installation"
if [ -s $SOURCE/install.err ]
then
  echo "*********************************************"
  echo "error installation (see $SOURCE/install.err):"
  cat $SOURCE/install.err
else
  echo 
  echo "** Reboot system now"
fi
