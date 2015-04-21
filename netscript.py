#!/usr/bin/env python
# created by cwgueco April 21, 2015
import paramiko
import sys, getopt, time, re


def command_wait(command, wait_time, should_print):
    if 'quit' in command:
        if should_print:
            print "Sleeping in "+str(wait_time)+" seconds"
        time.sleep(wait_time)
    if 'return' in command:
        if should_print:
            print "Sleeping in "+str(wait_time)+" seconds"
        time.sleep(wait_time)    
    if 'end' in command:
        if should_print:
            print "Sleeping in "+str(wait_time)+" seconds"
        time.sleep(wait_time)
    if 'exit' in command:
        if should_print:
            print "Sleeping in "+str(wait_time)+" seconds"
        time.sleep(wait_time)
    if 'save' in command:
        if should_print:
            print "Sleeping in "+str(wait_time)+" seconds"
        time.sleep(wait_time)
    if 'write' in command:
        if should_print:
            print "Sleeping in "+str(wait_time)+" seconds"
        time.sleep(wait_time)
        
def send_string_and_wait(command, wait_time, should_print):
    shell.send(command)
    time.sleep(wait_time)
    receive_buffer = shell.recv(1024)
    if should_print:
        print receive_buffer

def process_comments(string, should_print):
    if should_print:
        print "Comments: "+string.strip()

def process_actions(string, should_print):
    actions = mysplit(string)
    
    if should_print:
        print "Actions: "+string
    if 'wait' in string:
        wait_time = int(actions[1])
        if should_print:
            print "Waiting: "+str(wait_time)
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
    
    target = ''
    username = ''
    password = ''
    cmdfile = ''
    verbose = False

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
        print "-----------------------"

if __name__ == '__main__':

    # Get the command-line arguments
    getarg(sys.argv[1:])

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(target, username=username, password=password)
    print "SSH connection established to %s" % target

    shell = remote_conn_pre.invoke_shell()

    with open(cmdfile) as fp:
        for line in fp:
            if re.match(r'#', line):
                process_comments(line, verbose)
            elif re.match(r'!', line):
                process_actions(line, verbose)
            else:
                send_string_and_wait(line, 1, verbose)
            
    print "Closing SSH connection"

    remote_conn_pre.close()

    quit()
