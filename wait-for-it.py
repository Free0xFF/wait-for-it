#-*- encoding=utf-8 -*-

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

def log(info):
	global quiet
	if quiet == 0:
		print(info)

def wait_for(host, port, timeout):
	# output some logs
	notimeout = False
	if timeout == '0':
		notimeout = True
	app = host+":"+str(port)
	if notimeout:
		log(sys.argv[0]+": waiting for "+app+" without a timeout")
	else:
		log(sys.argv[0]+": waiting "+str(timeout)+" seconds for "+app)
	
	# start time
	start_ts = time.time()
	
	# attemp to connect
	sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	while True:
		try:
			sk.connect((host, port))
			end_ts = time.time()
			diff_ts = int(end_ts - start_ts)
			log(sys.argv[0]+": "+app+" is available after "+str(diff_ts)+" seconds")
			break
		except:
			if notimeout:
				continue
			time.sleep(1)
			timeout -= 1
			if timeout == 0:
				end_ts = time.time()
				diff_ts = int(end_ts - start_ts)
				log(sys.argv[0]+": timeout occurred after waiting "+str(diff_ts)+" seconds for "+host+":"+str(port))
				break

def start():
	try:
		host,port,timeout,quiet,helps = parse_args()
		if helps == 1:
			raise Exception("Help information.")
		if host == '' or port == -1:
			raise Exception("Host and port must set.")
		wait_for(host,port,timeout)
	except Exception as err:
		print(err)
		usage()

def parse_args():
	global quiet
	host = ''
	port = -1
	flag = 1
	helps = 0
	timeout = 15
	if(len(sys.argv) == 1):
		raise Exception("Host and port must set.")
	if ':' in sys.argv[1]:
		flag = 2
	opts,values= getopt.getopt(sys.argv[flag:],'h:p:qt:',['host=','port=','timeout=','quiet','help'])
	for k,v in opts:
		if k == '-t' or k == '--timeout':
			timeout = int(v)
		elif k == '-h' or k == '--host':
			host = v
		elif k == '-p' or k == '--port':
			port = int(v)
		elif k == '-q' or k == '--quiet':
			quiet = 1
		elif k == '--help':
			helps = 1
	if flag == 2:
		hostport = sys.argv[1].split(':')
		host = hostport[0]
		port = hostport[1]
	return host,port,timeout,quiet,helps


if __name__ == '__main__':
	start()