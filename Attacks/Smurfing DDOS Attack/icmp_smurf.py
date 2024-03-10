import sys
from scapy.all import *

# Layer 3
# Define the ICMP packet with echo request (ping)
icmp_packet = IP(src=sys.argv[1], dst=sys.argv[2]) / ICMP()

# Send the ICMP packet in a loop
while(1):
    send(icmp_packet)
