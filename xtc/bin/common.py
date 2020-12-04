from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import hashlib
import locale
import logging
import os.path
import lsb_release
import shutil
import socket
import struct
import subprocess
from subprocess import PIPE
from subprocess import Popen
import sys

ressourcefile = ""
SystemFile = ""
Language = ""


def loggingStart(loggingfilename, debugOn):
    if debugOn is True:
        try:
            filew = open(loggingfilename, "a")
            filew.write("======================================================\n")
            filew.close()
        except OSError as error:
            errorDialog(error)

    logginglevel = logging.CRITICAL
    if debugOn is True:
        logginglevel = logging.DEBUG
    logging.basicConfig(filename=loggingfilename,
                        level=logginglevel,
                        style="{",
                        format="{asctime} [{levelname:8}] [{funcName:25}] {message}")


# network
# -------
def isHostAlive(address):
    logging.info(address)
    result = os.system("ping -c 1 " + address + " > /dev/null")
    logging.info(result)
    if result == 0:
        return True
    return False
    
def isNetworkAddress(address):
    logging.info(address)
    stringlist = address.split(".")
    if len(stringlist) < 4:
        messageDialog("networkAddressError")
        return False
    for value in stringlist:
        value = str(value)
        if value.isdigit() is False:
            logging.info("isdigit " + value)
            messageDialog("networkAddressError")
            return False
        number = int(value)
        if number < 0 or number > 255:
            messageDialog("networkAddressError")
            return False
    return True


def readConnectionInterfaces():
    logging.info("readConnectionInterfaces")    
    niclist = os.listdir("/sys/class/net/")
    connections = []
    
    for line in niclist:        
        logging.info(line)    
        if not "lo" in line:
            logging.info(line)    
            connections.append(line)

    return connections


def isNetworkInterfaceUp(interface):
    result = False
    logging.info(interface)
    interface = "/sys/class/net/" + interface + "/operstate"
    
    try:
        filer = open(interface, "r")
        up = filer.read()
        filer.close()
        if "up" in up:
            result = True
    except OSError as error:
        logging.error(error)
        
    logging.info(result)
    return result
    
def getSystem():
    system = lsb_release.get_distro_information()
    if "Ubuntu" in system:
        return "UBUNTU"
    return "RASPBERRY"

def isNetworkInterfaces():
    logging.info("isNetworkInterfaces")
    system = lsb_release.get_distro_information()
    logging.info(system)
    return False


def netmaskToCidr(netmask):
    logging.info(netmask)
    cidr = str(sum([bin(int(x)).count('1') for x in netmask.split('.')]))
    logging.info(cidr)
    return cidr


def cidrToNetmask(cidr):
    logging.info(cidr)
    host_bits = 32 - int(cidr)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    logging.info(netmask)
    return netmask


def readNetwork(self):
    logging.info("readConnection")
    if getSystem() == "UBUNTU":
        path = getRessource("networkNetplan")
        files = os.listdir(path)
        for file in files:
            connectionfile = path + "/" + file
    else:
        connectionfile = getRessource("networkDhcpcd")
    logging.info(connectionfile)
    
    if os.path.isfile(connectionfile):
        if getSystem() == "UBUNTU":
            values = readConnectionNetplan(connectionfile)
        else:
            values = readConnectionDhcpcd(connectionfile)
    return values


def readConnectionNetplan(connectionfile):
    logging.info("readConnectionNetplan")
    logging.info(connectionfile)
    value = {}
    filer = open(connectionfile, "r")
    nameserver = False
    
    for line in filer:
        if "dhcp4:" in line:
            stringlist = line.split(":", 2)            
            stringvalue = stringlist[1]
            stringvalue = stringvalue.strip()
            if stringvalue == "false":
                value["dhcp"] = False
            else:
                value["dhcp"] = True
                
        if "addresses:" in line and not nameserver:
            stringlist = line.split("[", 2)
            stringvalue = stringlist[1]
            stringlist = stringvalue.split("/", 2)
            stringvalue = stringlist[0]
            stringvalue = stringvalue.strip()
            value["address"] = stringvalue
            stringvalue = stringlist[1]
            stringlist = stringvalue.split("]", 2)
            stringvalue = stringlist[0]
            stringvalue = stringvalue.strip()            
            value["netmask"] = cidrToNetmask(stringvalue)
        
        if "addresses:" in line and nameserver:
            stringlist = line.split("[", 2)
            stringvalue = stringlist[1]
            stringlist = stringvalue.split("]", 2)
            stringvalue = stringlist[0]
            stringvalue = stringvalue.strip()
            value["dns"] = stringvalue
            
        if "gateway4:" in line:
            stringlist = line.split(":", 2)
            stringvalue = stringlist[1]
            stringvalue = stringvalue.strip()
            value["gateway"] = stringvalue
            
        if "nameservers:" in line:
            nameserver = True
            
    filer.close()
    return value

def readConnectionDhcpcd(connectionfile):
    logging.info("readConnectionDhcpcd")
    logging.info(connectionfile)
    value = {}
    filer = open(connectionfile, "r")
    nameserver = False
    value["dhcp"] = True
    
    for line in filer:
        if not line.startswith("#"):
            if "static ip_address=" in line:
                stringlist = line.split("=", 2)
                stringvalue = stringlist[1]
                stringlist = stringvalue.split("/", 2)
                stringvalue = stringlist[0]
                stringvalue = stringvalue.strip()
                value["address"] = stringvalue
                stringvalue = stringlist[1]
                stringvalue = stringvalue.strip()
                value["netmask"] = cidrToNetmask(stringvalue)
                value["dhcp"] = False
            
            if "static routers=" in line:
                stringlist = line.split("=", 2)
                stringvalue = stringlist[1]
                stringvalue = stringvalue.strip()
                value["gateway"] = stringvalue
            
            if "static domain_name_servers=" in line:
                stringlist = line.split("=", 2)
                stringvalue = stringlist[1]
                stringvalue = stringvalue.strip()
                value["dns"] = stringvalue
    filer.close()
    
    logging.info("readConnectionWlan")
    command = getRessource("commandGetWPA") + " " + getRessource("tmpFile")
    logging.info(command)
    runProgram(command)
    
    connectionfile = getRessource("tmpFile")
    logging.info(connectionfile)
    filer = open(connectionfile, "r")
    for line in filer:
        if not line.startswith("#"):
            if "ssid=" in line:
                stringlist = line.split("=", 2)
                stringvalue = stringlist[1]
                stringvalue = stringvalue.strip()
                stringvalue = stringvalue.strip('"')
                value["ssid"] = stringvalue
            if "psk=" in line:
                stringlist = line.split("=", 2)
                stringvalue = stringlist[1]
                stringvalue = stringvalue.strip()
                stringvalue = stringvalue.strip('"')
                value["password"] = stringvalue
    filer.close()
    return value

    
def readConnectionInterface(connectionfile):
    logging.info("readConnectionInterface")
    logging.info(connectionfile)
    value = {}
    filer = open(connectionfile, "r")
    
    for line in filer:
        line = line.strip()        
        if "iface" in line:
            if "dhcp" in line:
                value["dhcp"] = True
            else:
                value["dhcp"] = False                
                
        if "address" in line:            
            stringlist = line.split(" ", 2)
            value["address"] = stringlist[1]
            
        if "netmask" in line:
            stringlist = line.split(" ", 2)
            value["netmask"] = stringlist[1]
            
        if "gateway" in line:
            stringlist = line.split(" ", 2)
            value["gateway"] = stringlist[1]
            
        if "dns-nameservers" in line:
            stringlist = line.split(" ", 2)
            value["dns"] = stringlist[1]
            
        if "wpa-ssid" in line:
            stringlist = line.split(" ", 2)
            value["ssid"] = stringlist[1]
        
        if "wpa-psk" in line:
            stringlist = line.split(" ", 2)
            value["password"] = stringlist[1]
    filer.close()
    return value
    
def networkWriteWLAN(ssid, password):
    wlanfilename = None 
    system = getSystem()
    if system == "RASPBERRY":
        wlanfile = getRessource("dhcpcdWlanTemplate")
        wlanfilename = getRessource("tmpFile2")
        filer = open(wlanfile, "r")
        filew = open(wlanfilename, "w")
        writeline = True
        for line in filer:
            if ssid != "":
                line = line.replace("{ssid}", ssid)
            if password != "":
                line = line.replace("{password}", password)
            if "network" in line and (ssid == "" or password == ""):
                writeline = False
            if writeline:
                filew.write(line)
        filew.close()
        filer.close()
            
    return wlanfilename
    
def networkWriteDHCP(self):
    logging.info("networkWriteDHCP")
    if getSystem() == "UBUNTU":
        connectionfile = getRessource("netplanDHCPTemplate")
    else:
        connectionfile = getRessource("dhcpcdDHCPTemplate")
    
    logging.info(connectionfile)
    connection = str(self.networkInputInterface.currentText())
    ssid = self.networkInputWlanSSID.text()
    password = self.networkInputWlanPassword.text()
    if ssid != "":
        typ = "wifis"
    else:
        typ = "ethernets"

    filename = getRessource("tmpFile")
    
    if os.path.isfile(connectionfile):
        filer = open(connectionfile, "r")
        filew = open(filename, "w")
        
        for line in filer:
            line = line.replace("{type}", typ)
            line = line.replace("{connection}", connection)
            
            if ssid != "":
                line = line.replace("{ssid}", ssid)
            else:
                if "{ssid}" in line:
                    line = ""
                if "access-points:" in line:
                    line = ""
                        
            if password != "":
                line = line.replace("{password}", password)
            else:
                if "{password}" in line:
                    line = ""
                            
            filew.write(line)
        filew.close()
        filer.close()
       
        wlanfilename = networkWriteWLAN(ssid, password)
        networkRestart(self, filename, wlanfilename)


def networkWriteStaticIP(self):    
    logging.info("networkWriteStaticIP")    
    
    connection = str(self.networkInputInterface.currentText())
    address = str(self.networkInputAddress.text())
    result = isNetworkAddress(address)
    
    if result:
        gateway = str(self.networkInputGateway.text())
        if gateway != "":
            result = isNetworkAddress(gateway)

    if result:
        netmask = str(self.networkInputSubnetmask.text())
        result = isNetworkAddress(netmask)

    if result:
        dns = str(self.networkInputDNS.text())
        if dns != "":
            result = isNetworkAddress(dns)
            
    if result:    
        ssid = self.networkInputWlanSSID.text()
        password = self.networkInputWlanPassword.text()
        netmask = netmaskToCidr(netmask)
        
        system = getSystem()
        if system == "UBUNTU":
            connectionfile = getRessource("netplanTemplate")
        else:
            connectionfile = getRessource("dhcpcdTemplate")
            
        if ssid != "":
            typ = "wifis"
        else:
            typ = "ethernets"

        filename = getRessource("tmpFile")

        if os.path.isfile(connectionfile):
            try:
                filer = open(connectionfile, "r")
                filew = open(filename, "w")
        
                for line in filer:
                    line = line.replace("{connection}", connection)
                    line = line.replace("{address}", address)                
                    line = line.replace("{netmask}", netmask)
                    line = line.replace("{type}", typ)
                        
                    if gateway != "":
                        line = line.replace("{gateway}", gateway)
                    else:
                        if "{gateway}" in line:
                            line = ""
                        
                    if dns != "":
                        line = line.replace("{nameserver}", dns)
                    else:
                        if "{nameserver}" in line:
                            line = ""
                        if "nameservers:" in line:
                            line = ""
            
                    if ssid != "":
                        line = line.replace("{ssid}", ssid)
                    else:
                        if "{ssid}" in line:
                            line = ""
                        if "access-points:" in line:
                            line = ""
                    
                    if password != "":
                        line = line.replace("{password}", password)
                    else:
                        if "{password}" in line:
                            line = ""
                    
                    filew.write(line)
                filew.close()
                filer.close()
            except OSError as error:
                logging.error(error)
                errorDialog(error)
                
            wlanfilename = networkWriteWLAN(ssid, password)
            networkRestart(self, filename, wlanfilename)


def networkRestart(self, filename, wlanfilename):
    logging.info("networkRestart")    
    logging.info(filename)        
    if getSystem() == "UBUNTU":
        command = getRessource("commandNetplan") + " " + filename
    else:
        command = getRessource("commandDhcpcd") + " " + filename
    logging.info(command)
    runProgram(command)
    
    if wlanfilename is not None:
        command = getRessource("commandWlanDhcpcd") + " " + wlanfilename
        logging.info(command)    
        runProgram(command)
    systemRebootAssume(self)

# system
# ------
def isRemoteVNC():
    filename = getRessource("remoteVNCSwitch")
    if os.path.isfile(filename):
        return True
    return False

def isRemoteSSH():
    filename = getRessource("remoteSSHSwitch")
    if os.path.isfile(filename):
        return True
    return False

def remoteVNC(switch, self):
    logging.info(switch)    
    filename = getRessource("remoteVNCSwitch")
    
    try:
        if switch == True:
            passfile = getRessource("remoteVNCPasswordFile")
            command = getRessource("commandVNCPasswd")
            password = self.systemInputRemotePassword.text()
            runProgram("echo '" + password + "' | " + command + " " + passfile)
            filew = open(filename, "w")
            filew.write("1")
            filew.close()
        else:
            if os.path.isfile(filename):
                os.remove(filename)
    except OSError as error:
        logging.error(error)
        errorDialog(error)

def remoteSSH(switch):
    logging.info(switch)    
    filename = getRessource("remoteSSHSwitch")
    
    try:
        if switch == True:
            filew = open(filename, "w")
            filew.write("1")
            filew.close()
        else:
            if os.path.isfile(filename):
                os.remove(filename)
    except OSError as error:
        logging.error(error)
        errorDialog(error)

def systemTerminal():
    logging.info("systemTerminal")
    runProgram(getRessource("commandTerminal"))


def systemRebootMessage(parent):
    logging.info("systemReboot")
    result = confirmDialog(parent,
                           getRessource("systemRebootTitle"),
                           getRessource("systemAssumeMessage"))
    return result

def systemReboot(parent):
    logging.info("systemReboot")
    result = confirmDialog(parent,
                           getRessource("systemRebootTitle"),
                           getRessource("systemRebootMessage"))
    if result:
        logging.shutdown()
        runProgram(getRessource("commandVPNKill"), False)
        runProgram(getRessource("commandReboot"))


def systemRebootAssume(parent):
    logging.info("systemReboot")
    result = confirmDialog(parent,
                           getRessource("systemRebootTitle"),
                           getRessource("systemAssumeMessage"))
    if result:
        logging.shutdown()
        runProgram(getRessource("commandReboot"))


def systemShutdown(parent):
    logging.info("systemShutdown")
    result = confirmDialog(parent,
                           getRessource("systemShutdownTitle"),
                           getRessource("systemShutdownMessage"))
    if result:
        logging.shutdown()
        runProgram(getRessource("commandVPNKill"), False)
        runProgram(getRessource("commandShutdown"))

def isScreensaver():
    logging.info("isScreensaver")
    result = runProgramResult(getRessource("commandisScreensaver"))       
    logging.info("isScreensaver result " + str(result))
    if result == 0:
        return True
    return False

def isMonitorStandby():
    logging.info("isMonitorStandby")
    result = runProgramResult(getRessource("commandisMonitorStandby"))    
    logging.info("isMonitorStandby result " + str(result))
    if result == 0:
        return True
    return False
    
def isOneninedesign():
    logging.info("isOneninedesign")
    result = runProgramResult(getRessource("commandisOneninedesign"))
    logging.info("isOneninedesign result " + str(result))
    if result == 0:
        return True
    return False
    
def isArgon1():
    logging.info("isArgon1")
    result = runProgramResult(getRessource("commandisArgon1"))
    logging.info("isArgon1 result " + str(result))
    if result == 0:
        return True
    return False

def setArgon1(switch):
    logging.info(switch)        
    # delete all files
    filename = getRessource("argon1FileStart")
    if os.path.isfile(filename):
        os.remove(filename)        
    filename = getRessource("argon1FileStop")
    if os.path.isfile(filename):
        os.remove(filename)        
            
    if switch == "on":        
        filename = getRessource("argon1FileStart")
    else:
        filename = getRessource("argon1FileStop")
    
    try:
        filew = open(filename, "w")
        filew.write("1")
        filew.close()
    except OSError as error:
        logging.error(error)
        errorDialog(error)

def setScreensaver(value):
    logging.info("setScreensaver: " + value)
    writeConfigScript(getRessource("commandSetScreensaver") + " " + value)
    
def setMonitorStandby(value):
    logging.info("setMonitorStandby: " + value)
    writeConfigScript(getRessource("commandSetMonitorStandby") + " " + value)
       
def setOneninedesign(value):
    logging.info("setOneninedesign: " + value)
    writeConfigScript(getRessource("commandSetOneninedesign") + " " + value)
       
def setResolution(value):
    logging.info("setResolution: " + value)
    writeConfigScript(getRessource("commandSetResolution") + " " + value)
        
def writeConfigScript(value):        
    logging.info("writeConfigScript: " + value)
    configfile = getRessource("configScript")
    filew = open(configfile, "a")
    filew.write(value + "\n")
    filew.close

def deleteConfigScript():
    logging.info("deleteConfigScript")
    filename = getRessource("configScript")     
    if os.path.isfile(filename):
        try:
            os.remove(filename)
        except OSError as error:
            logging.error(error)
            errorDialog(error)

def getResolution():
    logging.info("getResolution")
    filename = getRessource("tmpFile")        
    runProgram(getRessource("commandGetResolution") + " > " + filename)    
    filer = open(filename, "r")
    result = ""
    for line in filer:
        result = line
        result = result.strip();
    filer.close()        
    return result

def isUSBAutomount():
    logging.info("isUSBAutomount")
    result = runProgramResult(getRessource("commandGetUSBAutomount"))
    logging.info("isUSBAutomount result " + str(result))
    if result == 0:
        return True
    return False

def setUSBAutomount(switch):
    logging.info("setUSBAutomount " + str(switch))
    
    # delete all files
    filename = getRessource("usbAutomountOn")
    if os.path.isfile(filename):
        os.remove(filename)        
    filename = getRessource("usbAutomountOff")
    if os.path.isfile(filename):
        os.remove(filename)        
            
    if switch == "on":        
        filename = getRessource("usbAutomountOn")
    else:
        filename = getRessource("usbAutomountOff")
    
    try:
        filew = open(filename, "w")
        filew.write("1")
        filew.close()
    except OSError as error:
        logging.error(error)
        errorDialog(error)        
    
# Connection
# ----------
def readAllConnections():
    logging.info("readAll")
    connectionfile = getRessource("connectionFile")
    connection = {}
    if os.path.isfile(connectionfile):
        filer = open(connectionfile, "r")
        index = 0
        for line in filer:
            line = line.rstrip()
            if "[connection" in line:
                name = line.split(" ", 2)
                name = name[1].split("]", 1)
                connection[index] = name[0]
                index = index + 1
        filer.close()
    return connection


def existingConnection(connectionname):
    logging.info("existingConnection")
    result = False
    connectionfile = getRessource("connectionFile")
    if os.path.isfile(connectionfile):
        filer = open(connectionfile, "r")
        for line in filer:
            line = line.strip()
            if "[connection" in line:
                name = line.split(" ", 2)
                name = name[1].split("]", 1)
                if name == connectionname:
                    result = True
                    break
        filer.close()
    return result


def isRepeat(connectionname):
    logging.info(connectionname)
    result = False
    connectionfile = getRessource("connectionFile")
    if os.path.isfile(connectionfile):
        filer = open(connectionfile, "r")
        nameresult = False
        for line in filer:
            line = line.strip()
            if "[connection" in line:
                value = line.split(" ", 2)
                name = value[1].split("]", 1)
                name = name[0]
                if name == connectionname:
                    nameresult = True
                else:
                    nameresult = False
            if nameresult is True:
                if "repeat=" in line:
                    value = line.split("=", 2)
                    result = False
                    if value[1] == "yes":
                        result = True
                    break
        filer.close()
    return result


def readConnection(connectionname):
    logging.info("readConnection")
    logging.info(connectionname)
    connectionfile = getRessource("connectionFile")
    connection = {}
    # default values for further request
    connection["systemlogin"] = "no"
    connection["login"] = ""
    connection["password"] = ""
    
    if os.path.isfile(connectionfile):
        filer = open(connectionfile, "r")
        for line in filer:
            line = line.rstrip()
            if "[connection" in line:
                name = line.split(" ", 2)
                name = name[1].split("]", 1)
                fileconnectionname = name[0]
            if fileconnectionname == connectionname:
                if "[connection" in line:
                    name = line.split(" ", 2)
                    name = name[1].split("]", 1)
                    connection["name"] = name[0]
                if "typ=" in line:
                    name = line.split("=", 2)
                    connection["typ"] = name[1]
                if "address=" in line:
                    name = line.split("=", 2)
                    connection["address"] = name[1]
                if "port=" in line:
                    name = line.split("=", 2)
                    connection["port"] = name[1]
                if "password=" in line:
                    name = line.split("=", 2)
                    connection["password"] = name[1]
                if "resolution=" in line:
                    name = line.split("=", 2)
                    connection["resolution"] = name[1]
                if "color=" in line:
                    name = line.split("=", 2)
                    connection["color"] = name[1]
                if "autostart=" in line:
                    name = line.split("=", 2)
                    connection["autostart"] = name[1]
                if "command=" in line:
                    name = line.split("=", 1)
                    connection["command"] = name[1]
                if "application=" in line:
                    name = line.split("=", 2)
                    connection["application"] = name[1]
                if "port=" in line:
                    name = line.split("=", 2)
                    connection["port"] = name[1]
                if "login=" in line:
                    name = line.split("=", 2)
                    connection["login"] = name[1]
                if "user=" in line:
                    name = line.split("=", 2)
                    connection["user"] = name[1]
                if "desktop=" in line:
                    name = line.split("=", 2)
                    connection["desktop"] = name[1]
                if "keyboard=" in line:
                    name = line.split("=", 2)
                    connection["keyboard"] = name[1]
                if "parameter=" in line:
                    name = line.split("=", 2)
                    connection["parameter"] = name[1]
                if "repeat=" in line:
                    name = line.split("=", 2)
                    connection["repeat"] = name[1]
                if "systemlogin=" in line:
                    name = line.split("=", 2)
                    connection["systemlogin"] = name[1]
                if "alternative=" in line:
                    name = line.split("=", 2)
                    connection["alternative"] = name[1]
        filer.close()
    return connection


def deletePasswordFile(connectionname):
    logging.info("deletePasswordFile")
    filename = getRessource("passwordFile") + "." + connectionname
    if os.path.isfile(filename):
        try:
            os.remove(filename)
        except OSError as error:
            logging.error(error)
            errorDialog(error)


def getPasswordFile(connectionname):
    logging.info("getPasswordFile")
    filename = getRessource("passwordFile") + "." + connectionname
    return filename


def newConnection(values, command, connectionname):
    logging.info("newConnection")
    connectionfile = getRessource("connectionFile")
    filew = open(connectionfile, "a")
    filew.write("[connection " + connectionname + "]\n")
    filew.write("typ=" + values["typ"] + "\n")
    filew.write("address=" + values["address"] + "\n")
    if "port" in values:
        filew.write("port=" + values["port"] + "\n")
    if "resolution" in values:
        filew.write("resolution=" + values["resolution"] + "\n")
    if "color" in values:
        filew.write("color=" + values["color"] + "\n")
    if "application" in values:
        filew.write("application=" + values["application"] + "\n")
    if "desktop" in values:
        filew.write("desktop=" + values["desktop"] + "\n")
    if "keyboard" in values:
        filew.write("keyboard=" + values["keyboard"] + "\n")
    if "login" in values:
        filew.write("login=" + values["login"] + "\n")
    if "user" in values:
        filew.write("user=" + values["user"] + "\n")
    if "password" in values:
        filew.write("password=" + values["password"] + "\n")
    if "systemlogin" in values:
        filew.write("systemlogin=" + values["systemlogin"] + "\n")        
    if "parameter" in values:
        filew.write("parameter=" + values["parameter"] + "\n")        
    if "alternative" in values:
        filew.write("alternative=" + values["alternative"] + "\n")        
    filew.write("autostart=" + values["autostart"] + "\n")
    filew.write("repeat=" + values["repeat"] + "\n")
    filew.write("command=" + command + "\n\n")
    filew.close()
    # write conection to system
    command = getRessource("commandConnectionFile")
    command = command + " " + connectionfile
    runProgram(command)


def deleteConnection(connectionname):
    logging.info("deleteConnetion")
    connectionfile = getRessource("connectionFile")
    if os.path.isfile(connectionfile):
        filer = open(connectionfile, "r")
        tmpfile = getRessource("tmpFile")
        filew = open(tmpfile, "w")
        result = False
        for line in filer:
            line = line.rstrip()
            if "[connection" in line:
                result = False
                nameline = line.split(" ", 2)
                nameline = nameline[1].split("]", 1)
                name = nameline[0]
                name = name.strip()
                if name == connectionname:
                    result = True
            if result is False:
                filew.write(line + "\n")
        filew.close()
        filer.close()
        try:
            oldfile = connectionfile + ".old"
            shutil.copyfile(connectionfile, oldfile)
            shutil.copyfile(tmpfile, connectionfile)
        except (IOError, os.error) as error:
            logging.error(error)
            errorDialog(error)

# miscellaneous
# -------------
def setRessourceFile(filename):
    global ressourcefile
    ressourcefile = filename


def getRessourceByName(filename, name):
    ressource = ""
    if os.path.isfile(filename):
        filep = open(filename)
        for line in filep:
            line = line.rstrip()
            if line.startswith("#") is False:
                if name in line:
                    stringlist = line.split("=", 1)
                    ressource = stringlist[1]
        filep.close()
        return ressource


def getSystemFile(filename):
    logging.info("getSystemFile")
    systemfile = getRessourceByName(filename, "systemFile")
    global SystemFile
    SystemFile = systemfile
    return systemfile


def readSystem():
    logging.info("readSystem")
    values = {}
    global SystemFile
    if os.path.isfile(SystemFile):
        try:
            filer = open(SystemFile, "r")
            for line in filer:
                line = line.strip()
                name = line.split("=", 2)
                values[name[0]] = name[1]
            filer.close()
        except IOError as error:
            logging.error(error)
            errorDialog(error)
    return values


def writeSystem(values):
    logging.info("writeSystem")
    global SystemFile
    logging.info(SystemFile)
    try:
        tmpfile = getRessource("tmpFile")
        filew = open(tmpfile, "w")
        line = "startAdmin=" + values["startAdmin"] + "\n"
        filew.write(line)
        if "adminPassword" in values:
            line = "adminPassword=" + values["adminPassword"] + "\n"
            filew.write(line)
        line = "language=" + values["language"] + "\n"
        filew.write(line)
        line = "keyboardLayout=" + values["keyboardLayout"] + "\n"
        filew.write(line)
        filew.close()
    except OSError as error:
        logging.error(error)
        errorDialog(error)
    try:
        if os.path.isfile(SystemFile):
            oldfile = SystemFile + ".old"
            shutil.copyfile(SystemFile, oldfile)
        #shutil.copyfile(tmpfile, SystemFile)
        # write file to system
        command = getRessource("commandSystemFile")
        command = command + " " + tmpfile
        runProgram(command)
    except OSError as error:
        logging.error(error)
        errorDialog(error)

    
def fillListWidgets(self, connectedThreads):
    logging.info("fillListWidgets")
    self.connectList.clear()
    self.configList.clear()
    connections = readAllConnections()
    for index in range(len(connections)):
        name = connections[index]
        item = QListWidgetItem(name)
        item.setIcon(QIcon(getRessource("disconnectIcon")))

        if name in connectedThreads:
            item.setIcon(QIcon(getRessource("connectIcon")))
        self.connectList.addItem(item)

        item = QListWidgetItem(name)
        item.setIcon(QIcon(getRessource("disconnectIcon")))
        if name in connectedThreads:
            item.setIcon(QIcon(getRessource("connectIcon")))
        self.configList.addItem(item)
    self.connectList.sortItems()
    self.configList.sortItems()
    

def getLanguage():
    logging.info("getLanguage")
    language = "DE"
    values = readSystem()
    if "language" in values:
        if values["language"] == "English":
            language = "EN"
    else:
        locales = locale.getlocale()
        if locales[0].find("de_") == -1:
            language = "EN"
    global Language
    Language = language
    logging.info(language)
    return language


def getRessource(ressource):
    result = None
    if os.path.isfile(ressourcefile):
        filep = open(ressourcefile)
        for line in filep:
            line = line.rstrip()
            if line.startswith("#") is False:
                stringlist = line.split("=", 1)
                findressource = ressource
                global Language
                if Language == "DE":
                    findressource = ressource + "_D"
                if findressource == stringlist[0]:
                    stringlist = line.split("=", 1)
                    result = stringlist[1]
                    result = result.rstrip()
                    break
                findressource = ressource
                if findressource == stringlist[0]:
                    stringlist = line.split("=", 1)
                    result = stringlist[1]
                    result = result.rstrip()
                    break
        filep.close()

    if result is None:
        logging.info("Ressource " + ressource + " not found")
        print("Ressource " + ressource + " not found")
        sys.exit()
    #result = result.decode("utf-8")
    return result


def convertPassword(password):
    logging.info("convertPassword")
    result = hashlib.md5(bytes(password, "utf-8"))
    result = result.hexdigest()
    return result


def confirmDialog(parent, title, message):
    result = QMessageBox.question(parent, title, message,
                                  QMessageBox.Yes | QMessageBox.No)
    if result == QMessageBox.Yes:
        return True
    return False


def getCurrentKeyboardLayout():
    logging.info("getKeyboardLayout")
    tmpfile = getRessource("tmpFile")
    command = getRessource("commandCurrentKeyboardLayout")
    command = command + " > " + tmpfile
    runProgram(command)
    layout = ""
    if os.path.isfile(tmpfile):
        filer = open(tmpfile)
        for line in filer:
            line = line.strip()
            stringlist = line.split(":", 1)
            layout = stringlist[1]
            layout = layout.strip()
        filer.close()
    return layout


def getKeyboardLayouts():
    logging.info("getKeyboardLayouts")
    filename = getRessource("tmpFile")
    command = getRessource("commandKeyboardLayouts")
    command = command + " > " + filename
    runProgram(command)
    layout = ""
    if os.path.isfile(filename):
        filer = open(filename)
        for line in filer:
            line = line.strip()
            layout = layout + "," + line
        filer.close()
    return layout


def writeKeyboardLayout(layout):
    logging.info("editKeyboardLayout")
    filename = getRessource("keyboardLayoutFile")
    if os.path.isfile(filename):
        try:
            filer = open(filename, "r")
            tmpfile = getRessource("tmpFile")
            filew = open(tmpfile, "w")
            for line in filer:
                if "XKBLAYOUT" in line:
                    line = 'XKBLAYOUT="' + layout + '"\n'
                filew.write(line)
            filew.close()
            filer.close()
            # copy keyboard to keyboard file
            command = getRessource("commandKeyboardLayout") + " " + tmpfile
            runProgram(command)
        except OSError as error:
            errorDialog(error)
    else:
        error = getRessource("fileNotFoundError") + ": " + filename
        logging.error(error)
        errorDialog(error)


def fillComboBoxConnections(self, component):
    logging.info("fillComboBoxConnections")
    connections = readAllConnections()
    component.addItem("")
    for index in range(len(connections)):
        name = connections[index]
        component.addItem(name)

    
def fillComboBoxList(self, values, component):
    logging.info("fillComboBoxFileList")
    results = values.split(",")
    for value in results:
        component.addItem(value)


def fillComboBox(self, ressource, component):
    logging.info("fillComboBox")
    result = getRessource(ressource)
    results = result.split(",")
    for value in results:
        value = value.strip()
        component.addItem(value)


def getDesktop():
    desktop = "openbox"
    try:
        command = Popen(["wmctrl", "-m"], stdout=PIPE)
        commandout, commanderr = command.communicate()
        logging.info(commandout)
        logging.info(commanderr)
        desktop = "openbox"
        if "Lightdm" in str(commandout):
            desktop = "lightdm"
        logging.info(desktop)
    except OSError:
        None
    return desktop


def getVNCViewer():
    logging.info("getVNCViewer")
    result = "realvnc"
    filename = os.path.realpath(getRessource("pathToVNCViewer"))
    if "tigervnc" in filename:
        result = "tigervnc"
    if "tightvnc" in filename:
        result = "tightvnc"
    logging.info(result)
    return result


def enableTabs(self, enable):
    self.thinClientTab.setTabEnabled(2, enable)
    self.thinClientTab.setTabEnabled(3, enable)
    self.thinClientTab.setTabEnabled(4, enable)
    self.thinClientTab.setTabEnabled(5, enable)


def runProgram(command, message=True):
    logging.info("runProgram")
    logging.info(command)
    result = True
    try:        
        resultrun = runProgramResult(command)
        if resultrun != 0 and message:
            errorDialog(getRessource("systemErrorMessage"))
            result = False
    except OSError as error:
        logging.error(error)
        errorDialog(error)
        result = False
    return result

def getSystem():
    command = getRessource("commandGetSystem")
    logging.info("getSystem")
    logging.info(command)
    result = subprocess.run([command], stdout=subprocess.PIPE).stdout.decode('utf-8')
    result = result.strip()
    if result == "PI3" or result == "PI4":
        result = "RASPBERRY"
    else:
        result = "UBUNTU"
    logging.info(result)
    return result
    
def runProgramResult(command):
    logging.info("runProgramResult")
    logging.info(command)
    return os.system(command)


def errorDialog(message):
    logging.info("errorDialog")
    logging.info(message)
    messageDialogExec(str(message), getRessource("messageTitle"),
                      QMessageBox.Critical)


def messageDialog(message):
    logging.info("messageDialog")
    messageDialogExec(getRessource(message), getRessource("messageTitle"),
                      QMessageBox.Information)


def messageDialogExec(message, title, typ, text=None):
    msgDialog = QMessageBox()
    msgDialog.setIcon(typ)
    msgDialog.setWindowTitle(title)
    if text != None:
        msgDialog.setDetailedText(text)        
    msgDialog.setText(message)
    msgDialog.exec_()

  
def textDialog(title, text):
    dialog = uic.loadUi("/opt/thinclient/bin/dialogtext.ui")    
    dialog.dialogText.setText(text)
    dialog.exec_()   


def cancelDialog(message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(getRessource(message))
    msgBox.setWindowTitle(getRessource("messageTitle"))
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    #msgBox.buttonClicked.connect(msgButtonClick)
    result = False
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
       result = True
    return result
