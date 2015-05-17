#!/usr/bin/env python
# modified April 21, 2015 - cwgueco
# modified May 11, 2015 - cwgueco
# modified May 15, 2015 - fixed newline output in verbose mode - cwgueco
# modified May 17, 2015 - added more comments - cwgueco
import paramiko
import sys, getopt, time, re

def send_string_and_wait(command, wait_time, should_print):
    shell.send(command+'\n')
    response = shell.recv(9999)
    time.sleep(wait_time)
    if should_print:
       sys.stdout.write(response)
       sys.stdout.flush()

def process_comments(string, should_print):
    if should_print:
        print "Comments: "+string.strip()

def process_actions(string, should_print):
    actions = mysplit(string)

    response = shell.recv(9999)
    if should_print:
       sys.stdout.write(response)
       sys.stdout.flush()

    if should_print:
        print "\nActions: "+string
    if 'wait' in string:
        shell.send('\n')
	if len(actions) > 1:
            wait_time = int(actions[1])
        else:
	    wait_time = wait
        if should_print:
            sys.stdout.write("Waiting: "+str(wait_time)+" seconds")
            sys.stdout.flush()
        time.sleep(wait_time)

def mysplit(string):
    words = []
    inword = 0
    for c in string:
        if c in " \r\n\t": # whitespace
            inword = 0
        elif not inword:
            words = words + [c]
            inword = 1
        else:
            words[-1] = words[-1] + c
    return words

def getarg(argv):
    global target
    global username
    global password
    global cmdfile
    global verbose
    global wait    
    global interval

    target = ''
    username = ''
    password = ''
    cmdfile = ''
    verbose = False
    wait = 5
    interval = .2 

    try:
        opts, args = getopt.getopt(argv,"t:u:p:i:v",["target=","username=","password=","ifile=","verbose"])
    except getopt.GetoptError:
        print 'netscript.py -t <target> -u <username> -p <password> -i <command_file> -v'
        sys.exit(2)
      
    for opt, arg in opts:
        if opt == '-h':
            print 'netscript.py -t <target> -u <username> -p <password> -i <command_file> -v'
            sys.exit()
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-i", "--ifile"):
            cmdfile = arg
        elif opt in ("-v", "--verbose"):
            verbose = True    
    if verbose:
        print "-----------------------"
	print 'Input parameters'
        print 'Target host  :', target 
        print 'Username     :', username
        print 'Password     :', password
        print 'Command file :', cmdfile
        print 'Verbose      :', verbose
        print 'Global wait  :', wait,'seconds'
	print 'Interval     :', interval,'seconds' 
        print "-----------------------"

if __name__ == '__main__':

    # Get the command-line arguments
    getarg(sys.argv[1:])

    # Create the SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (be careful with this unless you trust your network) 
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Initiate SSH connection
    remote_conn_pre.connect(target, username=username, password=password)
    print "SSH connection established to %s" % target

    # Invoke interactive SSH shel
    shell = remote_conn_pre.invoke_shell()

    # Looping the command file and executing them in the shell 
    with open(cmdfile) as fp:
        for line in fp:
            line = line.strip()

            # Processing comments which starts with #'
            if re.match(r'#', line):
                process_comments(line, verbose)

            # Processing actions which start with '!' (so far 'wait' is allowed)
            elif re.match(r'!', line):
                process_actions(line, verbose)

            # Processing commands to the device
            else:
                send_string_and_wait(line, interval, verbose)
            
    # Closing SSH connection
    print "\nSSH connection closed from %s" % target
    remote_conn_pre.close()

    quit()
