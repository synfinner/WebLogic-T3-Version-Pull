# WebLogic T3 Version Pull

This script is designed to issue a T3 request to a WebLogic server in order to get the underlying version. I initially borrowed the test string from the nmap NSE script, see: https://svn.nmap.org/nmap/scripts/weblogic-t3-info.nse

## Script Usage

```
synbook-pro :: Python/WebLogic_T3_Version_Pull » ./t3_version.py -h
usage: t3_version.py [-h] [-t TARGET] [-p PORT] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        hotname/ip of target
  -p PORT, --port PORT  port to connect on
  -s, --ssl             negotiate over ssl/t3s
```

## Features

While t3 is useful, it is worth noting that it is plaintext. This is where t3s (secure) comes in. Thankfully, t3s is simply an ssl-wrapped tcp connection. This script will allow you to issue a ssl-wrapped socket connection. 

## Example outputs

**Connecting over T3:**

```
synbook-pro :: Python/WebLogic_T3_Version_Pull » ./t3_version.py -t xxx.xxx.xxx.xx9 -p 80
HOST:  xxx.xxx.xxx.xx9 -- HELO:12.2.1.3.0.false
```

**Connecting over T3S:**

```
synbook-pro :: Python/WebLogic_T3_Version_Pull » ./t3_version.py -t xxx.xxx.xxx.x4 -p 443 -s
HOST:  xxx.xxx.xxx.x4 -- HELO:12.2.1.3.0
```