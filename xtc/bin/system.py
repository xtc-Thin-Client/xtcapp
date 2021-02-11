#!/usr/bin/python3
import sys
import os
import logging
import common
import vpn

def configSystem(systemfile):
    print("read file " + systemfile)
    values = readParameters(systemfile)
    
    networksave = True
    if "system_networksave" in values:
        if values["system_networksave"] == "no":
            networksave = False
    
    print("config network")
    if networksave:
        # write network
        if not "network_address" in values:
            values["network_address"] = ""
        if not "network_subnetmask" in values:
            values["network_subnetmask"] = ""
        if not "network_gateway" in values:
            values["network_gateway"] = ""
        if not "network_dns" in values:
            values["network_dns"] = ""
        if not "network_wlan_ssid" in values:
            values["network_wlan_ssid"] = ""
        if not "network_wlan_password" in values:
            values["network_wlan_password"] = ""
        
        networkvalues = {}
        networkvalues["connection"] = values["network_interface"]
        networkvalues["address"] = values["network_address"]
        networkvalues["subnetmask"] = values["network_subnetmask"]
        networkvalues["gateway"] = values["network_gateway"]
        networkvalues["dns"] = values["network_dns"]
        networkvalues["ssid"] = values["network_wlan_ssid"]
        networkvalues["password"] = values["network_wlan_password"]
        
        if values["network_typ"] == "dhcp":
            print(" set network")
            common.networkWriteDHCP(networkvalues)
        else:
            print(" set network")
            common.networkWriteStaticIP(networkvalues)
        print("OK")
    
    print("config vnc")
    if "system_vnc" in values:
        print(" set vnc")
        if values["system_vnc"] == "on": 
            if values["sytem_vnc_password"] != "":
                common.remoteVNC(True, values["system_vnc_password"])
            else:
                common.remoteVNC(False, None)
    else:
        values["system_vnc"] = "off"
    print("OK")
    
    print("config ssh")
    if "system_ssh" in values:
        print(" set ssh")
        if values["system_ssh"] == "on":
            if values["system_ssh_password"] != "":
                common.remoteSSH(True, values["system_ssh_password"])
        else:
            common.remoteSSH(False, None)
    else:
        values["system_ssh"] = "off"
    print("OK")
    
    # set up config scripts    
    # read system
    print("config system")
    systemValues = common.readSystem()
    if not "startAdmin" in systemValues:
        systemValues["startAdmin"] = "yes"
    if not "language" in systemValues:
        systemValues["language"] = "English"
    if not "keyboardLayout" in systemValues:
        systemValues["keyboardLayout"] = "gb"
    if  not "startminimized" in values:
        systemValues["startMinimized"] = "no"
    if  not "networkSave" in values:
        systemValues["networkSave"] = "yes"
    if  not "resolution" in values:
        systemValues["resolution"] = "auto"
    if  not "resolution2" in values:
        systemValues["resolution2"] = "auto"
        
    if "system_admin" in values:
        systemValues["startAdmin"] = values["system_admin"]
    if systemValues["startAdmin"] == "no":
        if "system_admin_password" in values:
            if values["sytem_admin_password"] != "":
                systemValues["adminPassword"] = common.convertPassword(values["system_admin_password"])
    if "system_language" in values:
        systemValues["language"] = values["system_language"]
    if "system_keyboard" in values:
        systemValues["keyboardLayout"] = values["system_keyboard"]
    if "system_startminimized" in values:
        systemValues["startMinimized"] = values["system_startminimized"]
    if "system_networkSave" in values:
        systemValues["networkSave"] = values["system_networksave"]
    if "monitor_resolution" in values:
        systemValues["resolution"] = values["monitor_resolution"]
        common.setResolution(values["monitor_resolution"])
    if "monitor_resolution2" in values:
        systemValues["resolution2"] = values["monitor_resolution2"]
        if "monitor_orientation" in values:
            common.setMultiMonitor(True, values["monitor_orientation"], values["monitor_resolution2"])
        
    if len(systemValues) > 0:
        print("set system")
        common.writeSystem(systemValues)
        
    if "system_keyboard" in values:
        print(" set keyboard")
        common.writeKeyboardLayout(values["system_keyboard"])
    if "monitor_screensaver" in values:
        print(" set screensaver")
        common.setScreensaver(values["monitor_screensaver"])
    if "monitor_standby" in values:
        print(" set monitor standby")
        common.setMonitorStandby(values["monitor_standby"])
    if "monitor_resolution" in values:
        print(" set resolution")
        common.setResolution(values["monitor_resolution"])
    if "system_usbautomount" in values:
        print(" set usb automount")
        common.setUSBAutomount(values["system_usbautomount"])
    if "system_oneninedesign" in values:
        print(" set case oneninedesign")
        common.setOneninedesign(values["system_oneninedesign"])
    if "system_argon1" in values:
        print(" set case argon1")
        common.setArgon1(values["system_argon1"])
    if "system_soundcard" in values:
        print(" set soundcard")
        common.setSoundCard(values["system_soundcard"])
    print("OK")
    
    print("config time")
    timeValues = common.readTime()
    if "time_save" in values:
        timeValues["save"] = values["time_save"]
    if "time_time" in values:
        timeValues["time"] = values["time_time"]
    timeValues["automatic"] = "no"
    if "time_automatic" in values:
        timeValues["automatic"] = values["time_automatic"]
    if "time_ntp" in values:
        timeValues["ntp"] = values["time_ntp"]
    if "time_timezone" in values:
        timeValues["timezone"] = values["time_timezone"]
    timeValues["execute"] = "no"
    if "time_execute" in values:
        timeValues["execute"] = values["time_execute"]
    timeValues["repeat"] = "no"
    if "time_repeat" in values:
        timeValues["repeat"] = values["time_repeat"]
    if "time_action" in values:
        timeValues["action"] = values["time_action"]
    if "time_at" in values:
        timeValues["at"] = values["time_at"]
    if "time_last" in values:
        timeValues["last"] = values["time_last"]
    if len(timeValues) > 0:
        print(" set time")
        common.writeTime(timeValues)

    timeValues = {}
    if "time_show" in values:
        timeValues["show"] = values["time_show"]
    if len(timeValues) > 0:
        common.writeTimeTemp(timeValues)
    print("OK")
    
    # write vpn
    print("config vpn")
    vpnvalues = {}
    if "ovpn" in values:
        vpnvalues["ovpn"] = values["vpn_ovpn"]
    if "vpn_parameter" in values:
        vpnvalues["parametervpn"] = values["vpn_parameter"]
    if "vpn_autostart" in values:
        vpnvalues["autostartvpn"] = values["vpn_autostart"]
    if "vpn_systemlogin" in values:
        vpnvalues["systemlogin"] = values["vpn_systemlogin"]
    if len(vpnvalues) > 0:
        print(" set vpn")
        vpn.writeVPN(vpnvalues)
    print("OK")
    
# read system paramater file
def readParameters(filename):
    logging.info("readParmaeters " + filename)
    values = {}
    filer = open(filename, "r")
    for line in filer:
        line = line.strip()
        if line != "":
            stringlist = line.split("=", 2)
            name = stringlist[0]
            name = name.strip()
            value = stringlist[1]
            value = value.strip()
            values[name] = value
    filer.close()
    return values

if __name__ == "__main__":
    configSystem(sys.argv[1])
    print("to complete configuration: reboot system\n")
