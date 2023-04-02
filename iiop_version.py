#!/usr/bin/env python3

# 2 APRIL 2023, THIS CODE IS CURRENTLY UNTESTED
import socket
import struct


def send_iiop_request(target_host, target_port):
    """Sends an IIOP request to the target host and port and receives the response.

    Args:
        target_host (str): The target host.
        target_port (int): The target port.

    Returns:
        bytes: The received IIOP response.
    """
    request = b'\x49\x49\x4f\x50\x01\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x0e\x4a\x61\x76\x61\x20\x76\x65\x72\x73\x69\x6f\x6e\x3a\x20\x31\x2e\x30'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            server_address = (target_host, target_port)
            sock.connect(server_address)
            sock.sendall(request)
            data = sock.recv(1024)
            return data
        except socket.error as e:
            print(f"Socket error: {e}")
            return None


def extract_version(data):
    """Extracts the WebLogic version from the IIOP response.

    Args:
        data (bytes): The IIOP response.

    Returns:
        str: The WebLogic version if found, None otherwise.
    """
    if data and data[0:4] == b'\x49\x49\x4f\x50':
        body_len = struct.unpack('!i', data[8:12])[0]
        body = data[12:12+body_len]

        if body[0:8] == b'\x00\x00\x00\x01\x00\x00\x00\x00':
            version_len = struct.unpack('!i', body[24:28])[0]
            version = body[28:28+version_len].decode('utf-8')
            return version

    return None


def get_weblogic_version(target_host, target_port):
    """Attempts to get the WebLogic version using IIOP.

    Args:
        target_host (str): The target host.
        target_port (int): The target port.

    Returns:
        str: The WebLogic version if found, None otherwise.
    """
    data = send_iiop_request(target_host, target_port)
    version = extract_version(data)
    return version


if __name__ == "__main__":
    target_host = 'localhost'
    target_port = 7001
    version = get_weblogic_version(target_host, target_port)

    if version:
        print(f"WebLogic version: {version}")
    else:
        print("Failed to get WebLogic version")
