#-*- encoding=utf-8 -*-
#!/bin/usr/env python
import socket
import time
import getopt
import sys

# global
quiet = 0

def usage():
	usage_info = '''
Usage:
    %s host:port [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    -q | --quiet                Don't output any status messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    --help                      Print usage
''' %(sys.argv[0])
	print(usage_info)

def log(loginfo):
	global quiet
	if quiet == 0:
		print(loginfo)

def build_log(type,app,time=0):
	# 1=enable_timeout,2=disable_timeout,3=success_msg,4=timeout_msg
	loginfo = {
		 1:"%s: waiting %d seconds for %s" %(sys.argv[0],time,app),
		 2:"%s: waiting for %s without a timeout" %(sys.argv[0],app),
		 3:"%s: %s is available after %d seconds" %(sys.argv[0],app,time),
		 4:"%s: timeout occurred after waiting %d seconds for %s" %(sys.argv[0],time,app),
	}.get(type)
	return loginfo
	
def wait_for(host, port, timeout):
	# output some logs
	disable_timeout = False
	if timeout == 0: enable_timeout = False
	app = "%s:%d" %(host,port)
	loginfo = build_log(1,app,timeout)
	if disable_timeout: loginfo = build_log(2,app)
	log(loginfo)
	
	# get start time, then attempt to connect,
	# if succeed,then timeout_flag=0,otherwise timeout,timeout_flag=1
	timeout_flag = 0
	start_ts = time.time()
	sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	while True:
		try:
			sk.connect((host, port))
			break
		except:
			if disable_timeout:	continue
			time.sleep(1)
			timeout = timeout-1
			if timeout == 0:
				timeout_flag = 1
				break
	#succeed or timeout log
	end_ts = time.time()
	diff_ts = int(end_ts - start_ts)
	if timeout_flag == 0:
		loginfo = build_log(3,app,diff_ts)
	else:
		loginfo = build_log(4,app,diff_ts)
	log(loginfo)

def parse_args():
	global quiet
	host = ''
	port = -1
	helps = 0
	timeout = 15
	
	if(len(sys.argv) == 1):
		raise Exception("Host and port must set.")
	
	offset = 1
	if ':' in sys.argv[1]:
		offset = offset + 1
		hostport = sys.argv[1].split(':')
		host = hostport[0]
		port = int(hostport[1])
	
	s_params = 'h:p:qt:'
	l_params = ['host=','port=','timeout=','quiet','help']
	opts,values= getopt.getopt(sys.argv[offset:],s_params,l_params)
	
	for k,v in opts:
		if k == '--help': helps = 1
		elif k == '-h' or k == '--host': host = v
		elif k == '-q' or k == '--quiet': quiet = 1
		elif k == '-p' or k == '--port': port = int(v)
		elif k == '-t' or k == '--timeout': timeout = int(v)
	
	return host,port,timeout,quiet,helps

		
def start():
	try:
		host,port,timeout,quiet,helps = parse_args()
		if host=='' or port == -1 or helps == 1:
			usage()
			sys.exit(0)
		wait_for(host,port,timeout)
	except Exception as err:
		print(err)
		usage()

if __name__ == '__main__':
	start()
	