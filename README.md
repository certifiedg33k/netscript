# netscript

This is a Python/Paramiko script that I used to automate configuration task on network devices via SSH. 

This script assumed you have an username with administrative privilege. It is tested working with Cisco IOS and HP Comware network devices with SSH.
```
Usage:
./netscript.py 
netscript.py -t <target> -u <username> -p <password> -c <command_file> -v

-t target IP address / hostname
-u username
-p password
-c command file (contains set of commands)
-v verbose
```
For detailed guide, visit (http://certifiedgeek.weebly.com/blog/network-scripting-via-ssh-with-python-and-paramiko)

WARNING: This script is currently under development. Use at you own risk.

