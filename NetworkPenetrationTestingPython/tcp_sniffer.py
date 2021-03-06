import socket
import struct
from ctypes import *

#Usage: python tcp_sniffer.py

def IPHeader(Structure):
  _fields_ = [
      ("ihl",          c_ubyte, 4),
      ("version",      c_ubyte, 4),
      ("tos",          c_ubyte),
      ("len",          c_short),
      ("id",           c_short),
      ("offset",       c_short),
      ("ttl",          c_ubyte),
      ("protocol_num", c_ubyte),
      ("sum",          c_ushort),
      ("src",          c_unit32),
      ("dst",          c_unit32)
  ]
  def __new__(self, data=None):
    return self.from_buffer_copy(data)
  
  def __init__(self, dara=None):
    #Map source and destination IP addresses
    self.source_address = socket.inet_ntoa(struct.pack("@I",self.src))
    self.destination_address = socket.inet_ntoa(struct.pack("@I",self.dst))
    
    #Map protocol constants
    self.protocols = {1:"ICMP", 6:"TCP", 17:"UDP"}
    # get protocol name
    
    try:
      self.protocol = self.protocols[self.protocol_num]
    except:
      self.protocol = str(self.protocol_num)
  

def initTcpSocket():
  #crate the socket object
  sniffer_tcp = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.IPPROTO_TCP)

  # bind it to localhost
  sniffer_tcp.bind(('0.0.0.0',0))

  #include the ip header
  sniffer_tcp.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL,1)

  #TCP sniffer object
  return sniffer_tcp

def startSniffing():
  #TCP
  sniffer_tcp = initTcpSocket()
  print 'sniffer is listening for incoming connections'
  
  try:
    while True:
      #TCP
      raw_buffer_tcp = sniffer_tcp.recvfrom(65535)[0]
      ip_header_tcp = IPHeader(raw_buffer_tcp[0:20])
      
      if(ip_header_tcp.protocol == "TCP"):
        print "Protocol: %s %s -> %s" % (ip_header_tcp.protocol, ip_header_tcp.source_address, ip_header_tcp.destination_address)
        
  except KeyboardInterrupt: 
    print "Exiting Program ... "
    exit(0)

def main():
  startSniffing()

if __name == "__main__":
  main()
