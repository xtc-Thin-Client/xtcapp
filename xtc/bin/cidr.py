import sys
import socket
import struct

def cidrToNetmask(cidr):
    host_bits = 32 - int(cidr)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask

if __name__ == "__main__":
    netmask = cidrToNetmask("18")
    print(netmask)
