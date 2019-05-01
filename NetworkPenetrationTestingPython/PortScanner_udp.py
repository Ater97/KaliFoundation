import argparse
from socket import *
#netcat -v -l -u -p 5555
#Usage: python PortScanner_udp.py --udp -a localhost -p 5555

def printBanner(connSock,tgtPort):
  try:
    # Send data to target
    if(tgtPort == 80):
      connSock.send("GET HTTP/1.1 \r\n")
    else:
      connSock.send("\r\n")
      
    # Receive data from target
    results = connSock.recv(4096)
    # Print the banner
    print '[+] Banner: ' + str(results)
  except:
    print '[-] Banner not available\n'

def connScan(tgtHost,tgtPort):
  try:
    # Create the socket object
    connSock=socket(AF_INET,SOCK_STREAM)
    # try to connect with the target
    connSock.connect((tgtHost,tgtPort))
    print '[+] %d tcp open'% tgtPort
    printBanner(connSock,tgtPort)
  except:
    # Print the failure results
    print '[+] %d rcp closed'% tgtPort
  finally:
    # close the socket object
    connSock.close()

def connScanUdp(tgtHost,tgtPort):
  try:
    #Create the socket object
    connSock=socket(AF_INET,SOCK_DGRAM)
    #try to connect with the target
    connSock.connect((tgtHost,tgtPort))
    print '[+] %d udp open' % tgtPort
    printBanner(connSock,tgtPort)
  except:
    #print the failure results
    print '[+] %d udp closed' % tgtPort
    
def portScan(tgtHost,tgtPorts,isUdp):
  try:
    #if -a was not an IP address this will resolve it to an IP/ if its an IP thats 
    tgtIP = gethostbyname(tgtHost)
  except:
    print "[-] Error: Unknow Host"
    exit(0)
  
  try:
    #if the domain can be resolved thats good, the results will be like:
    tgtName = gethostbyaddr(tgtIP)
    print "[+] --- Scan result for: " + tgtName[0] + " ---"
  except:
    print "[+] --- Scan result for: " + tgtIP + " ---"

  setdefaulttimeout(10)
  
  # For each port number call the connScan function
  for tgtPort in tgtPorts:
    if not isUdp:
      connScan(tgtHost, int(tgtPort))
    else:
      connScanUdp(tgtHost, int(tgtPort))

def main():
  #Parse the command line arguments
  parser = argparse.ArgumentParser('Smart TCP Clinet Scanner')
  parser.add_argument("-a","--address",type=str,help="The target IP address")
  parser.add_argument("-p","--port",type="The port number to connect with")
  parser.add_argument("-u", "--udp",help="Include a UDP port scan", action="store_true")
  args = parser.parse_args()
  
  #Store the argumentes values
  ipaddress = args.address
  portNumbers = args.port.split(',')
  isUdp = args.udp
  
  #Call the Port Scan function
  portScan(ipaddress,portNumbers,isUdp)
  
if __name__ == "__main__":
  # Call the main function
  main()
