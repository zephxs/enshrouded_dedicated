#!/usr/bin/env python3
# prereq: pip install steamquery
from steam import SteamQuery
import sys
if sys.argv[-1] in ("--help", "-h"):
    print("Usage: python3 steamquery.py <server IP or FQDN> <query port number>")
elif len(sys.argv) <= 1:
    print("Error: No arguments provided.")
    print("Usage: python query.py <server IP or FQDN> <query port number>")
else:
    server_ip = str(sys.argv[1])
    server_port = int(sys.argv[2])
    server = SteamQuery(server_ip,server_port)
    info = server.query_server_info()
    print(str(info))

