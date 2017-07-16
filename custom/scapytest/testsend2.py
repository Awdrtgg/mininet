from scapy.all import *
from scapy.layers.inet import IP
start = time.time()
global p_start
p_start = -1

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

ip_map = {'111.62.242.25':'10.0.0.1', '10.21.238.36':'10.0.0.2'}

for p in PcapReader('testtcp.pcap'):
    if IP not in p:
        continue
    p_time = p.time
    p = p[IP]
    if (p.src != '10.21.238.36'):
        continue
    p.src = ip_map.get(p.src, p.src)
    p.dst = ip_map.get(p.dst, p.dst)
    del(p.chksum)
    
    #global p_start
    if (p_start < 0):
        p_start = p_time
        send(p)
    else:
        now = time.time() - start
        print now, p_time - p_start
        while (now < p_time - p_start):
            time.sleep(0.1)
            now = time.time() - start
            print now, p_time - p_start
        print '1'
        send(p)
    