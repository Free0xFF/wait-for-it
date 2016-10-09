# wait-for-it
python wait-for-it for docker container 

## Usage

```
wait-for-it.py host:port [-s] [-t timeout]
-h HOST | --host=HOST       Host or IP under test
-p PORT | --port=PORT       TCP port under test
                            Alternatively, you specify the host and port as host:port
-q | --quiet                Don't output any status messages
-t TIMEOUT | --timeout=TIMEOUT
                            Timeout in seconds, zero for no timeout
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
$ python wait-for-it.py -t 0 www.baidu.com:80
wait-for-it.py: waiting for www.google.com:80 without a timeout
wait-for-it.py: www.baidu.com:80 is available after 0 seconds
```

The subcommand will be executed regardless if the service is up or not.  If you wish to execute the subcommand only if the service is up, add the `--strict` argument. In this example, we will test port 81 on www.google.com which will fail:

```
$ ./wait-for-it.sh www.google.com:81 --timeout=1 --strict -- echo "google is up"
wait-for-it.sh: waiting 1 seconds for www.google.com:81
wait-for-it.sh: timeout occurred after waiting 1 seconds for www.google.com:81
wait-for-it.sh: strict mode, refusing to execute subprocess
```

If you don't want to execute a subcommand, leave off the `--` argument.  This way, you can test the exit condition of `wait-for-it.sh` in your own scripts, and determine how to proceed:

```
$ ./wait-for-it.sh www.google.com:80
wait-for-it.sh: waiting 15 seconds for www.google.com:80
wait-for-it.sh: www.google.com:80 is available after 0 seconds
$ echo $?
0
$ ./wait-for-it.sh www.google.com:81
wait-for-it.sh: waiting 15 seconds for www.google.com:81
wait-for-it.sh: timeout occurred after waiting 15 seconds for www.google.com:81
$ echo $?
124
```