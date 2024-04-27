#!/usr/bin/env python3
# prereq: pip install python-a2s
import sys, a2s

if sys.argv[-1] in ("--help", "-h"):
    print("Usage: python3 a2squery.py <server_IP/FQDN> <query_port>")
elif len(sys.argv) <= 2:
    print("Error: Missing arguments.. [use '-h' for usage]")
else:
    server_ip = str(sys.argv[1])
    server_port = int(sys.argv[2])
    server_address = (server_ip, server_port)
    info = a2s.info(server_address)
    print(info)

