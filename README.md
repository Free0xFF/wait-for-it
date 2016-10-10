# wait-for-it
python wait-for-it for docker container 

## Usage

```
Usage: wait-for-it.py [options]

Options:
  -h, --help            show this help message and exit
  -a ADDRESS, --address=ADDRESS
                        Host or IP under test
  -p PORT, --port=PORT  TCP port under test
  -t TIMEOUT, --timeout=TIMEOUT
                        Timeout in seconds, zero for no timeout
  -q, --quiet           Don't output any status messages
```

## Examples

For example, let's test to see if we can access port 80 on www.baidu.com, and if it is available, the script will print the successful message `wait-for-it.py: www.baidu.com:80 is available after n seconds`,where the n is the waiting seconds,otherwise it will output the timeout message `wait-for-it.py: timeout occurred after waiting n seconds for wait-for-it.py`,where the n equals timeout seconds,the default value is 15 seconds, you can modify it's value by setting `-t` or `--timeout` options.

```
$ python wait-for-it.py www.baidu.com:80
wait-for-it.sh: waiting 15 seconds for www.baidu.com:80
wait-for-it.sh: www.baidu.com:80 is available after 0 seconds
```

You can set your own timeout with the `-t` or `--timeout=` option.  Setting the timeout value to 0 will disable the timeout:

```
$ python wait-for-it.py  -a www.baidu.com -p 8080 -t 5
wait-for-it.py: waiting 5 seconds for www.baidu.com:8080
wait-for-it.py: timeout occurred after waiting 5 seconds for www.baidu.com:8080
```

If you don't want to output any log messge, you can set the `-q` or `--quiet` option to close the logger¡£
```
$ python wait-for-it.py  -a www.baidu.com -p 8080 -t 5 --quiet

```