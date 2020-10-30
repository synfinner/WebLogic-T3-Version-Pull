#!/usr/bin/env python3

##################################################
# Author: synfinner                              #
# Description: Get Weblogic version via T3.      #
##################################################

import sys
import socket
import argparse
import ssl


def t3ssl(host,port):

    # Setup SSL context
    context = ssl.create_default_context()
    # Ignore ssl validations
    context.check_hostname = False
    context.verify_mode |= ssl.CERT_NONE
    # Specify that we want to use T3S
    msg = "t3s 12.1.2\nAS:2048\nHL:19\n\n"
    try:
        logicSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SSL wrap the socket
        secureLogicSocket = context.wrap_socket(logicSocket, server_side=False, server_hostname=host)
        secureLogicSocket.connect((host, port))
        secureLogicSocket.send(msg.encode())
        data = secureLogicSocket.recv(1024)
        print("HOST: ", host,"--",data.decode().rstrip())
        secureLogicSocket.close()
    except Exception as e:
        print(e)
        exit()

def t3(host,port):
    # construct TCP socket.
    logicSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    try:
        logicSocket.connect((host,port))
    except Exception as e:
        print("[+]Error: ",e)
        exit()
    # Send t3 request. 
    msg = "t3 12.1.2\nAS:2048\nHL:19\n\n"
    try:
        logicSocket.send(msg.encode())
    except Exception as e:
        print("[+]Error: ",e)
        exit()

    data = logicSocket.recv(1024)
    print("HOST: ", host,"--",data.decode().rstrip())
    logicSocket.close()
    

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", type=str,
                    help="hotname/ip of target")
    parser.add_argument("-p", "--port", type=int,
                    help="port to connect on")
    parser.add_argument("-s", "--ssl",
                    help="negotiate over ssl/t3s",
                    action='store_true')
    args = parser.parse_args()
    host = args.target
    port = args.port
    if args.ssl:
        t3ssl(host,port)
    else:
        t3(host,port)

if __name__ == '__main__':
    main()