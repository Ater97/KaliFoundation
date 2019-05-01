#Dependencies -> wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
#             -> gunzip GeoLiteCity.dat.gz
#             -> mv GeoLiteCity.dat GeoIP.dat
# this needs to be on the same folder as sniff_scapy.py
#             -> easy_install pygeoip

from scapy.all import *
import pygeoip
from IPy import IP as IPLIB
from socket import*
import time

#Usage: python sniff_scapy.py

conversations={} #hold conversations dictinonary items
exclude_ips= ['10.0.0.18','127.0.0.1']

def saveToFile(traceInfo):
  try:
    #create the filelog object
    filename = 'network_monitor_log_' + time.strftime("%d_%m_%Y") + '.txt'
    fileLog = open(filename,'a')
    #write the trace information  
    fileLog.write(traceInfo)
    #separator
    fileLog.write('\r\n')
    fileLog.write('--------------------------------------')
    fileLog.write('\r\n')
    #close the file log object
    fileLog.close()
  except:
    pass


def getInfo(ipAddress):
  try:
    #try resolve the IP address
    hostName = gethostbyaddr(ipAddress)[0]
  except:
    #could not resolve the address
    hostName= " "
    
  #convert the IP to a valid IP object
  ip = IPLIB(ipAddress)
  # do not proceed if the IP is private
  if(ip.iptype()=='PRIVATE'):
    return 'private IP, Host Name: ' + hostName
  
  try:
    #initialize the GEOIP object
    geoip = pygeoip.GeoIP('GeoIP.dat')
    #get the record Info
    ipRecord = geoip.record_by_addr(ipAddress)
    #extract the country name
    country = ipRecord['country_name']
    #return the string result
    return 'Country: %s, Host: %s'% (country,hostName)
  except:
    #GeoIP could not locate the IP address
    return "Can't locate " + ipAddress + " Host: " + hostName

def printPacket(sourceIP,destinationIP):
  #assemble the message that we need to print and save
  traceInfo = '[+] Source (%s): %s ---> Destination (%s): %s '% (sourceIP,getInfo(sourceIP),destinationIP,getInfo(destinationIP))
  print traceInfo
  saveToFile(traceInfo)


def startMonitoring(pkt):
  try:
    if pkt.haslayer(IP):
      #get the source IP address
      sourceIP = pkt.getlayer(IP).src
      #get the destination IP addresss
      destinationIP = pkt.getlayer(IP).dst
      
      if(destinationIP in exclude_ips):
        return;
      #generate a unique key to avoid duplication
      uniqueKey = sourceIP+destinationIP
      
      #if we already processed the packet, then dont proceed further
      if(not conversations.has_key(uniqueKey)):
        #Store a flag in the array to avoid duplication
        conversations[uniqueKey] = 1
        #call the print packet function
        printPacket(sourceIP, destinationIP)
  except Exception, ex:
    print "Exception: " + str(ex)
    pass


def main():
  # start sniffing by filtering only the IP packets without storing anything inside the memory.
  sniff(prn=startMonitoring,store=0,filter="ip")

if __name__ == "__main__":
	main()
