import subprocess
import sys

import numpy as np

IS_ONLINE = False
SCALE = 1024*1024
BUFFER_LEN = 128 * 1024
PROTOCOL_EFFICIENCY = 0.85
# MSS
MSS = int(sys.argv[1])
# Totol Number of hosts
n1 = int(sys.argv[2])
# this host index
n2 = int(sys.argv[3])

# is online training
IS_ONLINE = int(sys.argv[4]) > 0

# destination preparation
destination_index_pool = range(n1)
destination_index_pool.remove(n2)
destination_pool = []
for idx in destination_index_pool:
    destination_pool.append('10.0.0.%d' % (idx + 1))
'''
destination_pool = [
    '10.108.125.234',
    '10.108.126.4',
]
'''
if not IS_ONLINE:
    # total request number
    n3 = int(sys.argv[5])

    # destination
    dest_idx = np.random.randint(0,len(destination_pool),n3)
    dests = []
    for idx in dest_idx:
        dest = destination_pool[idx]
        dests.append(dest)

    # file_size generation
    file_sizes = np.random.weibull(a=1.5, size=n3)*SCALE

    for addr,file_size in zip(dests, file_sizes):
        num_byte = int(file_size / PROTOCOL_EFFICIENCY)
        #bashCommand = 'iperf3 -c %s -l %d -n %d -Z -M %d' % (addr, BUFFER_LEN, num_byte, MSS)
        bashCommand = 'iperf -c %s -l %d -n %d -M %d' % (addr, BUFFER_LEN, num_byte, MSS)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print output
        print error
else:
    while True:
        try:
            dest_idx = np.random.randint(0, len(destination_pool))
            addr = destination_pool[dest_idx]
            file_size = np.random.weibull(a=1.5) * SCALE
            num_byte = int(file_size / PROTOCOL_EFFICIENCY)
            #bashCommand = 'iperf3 -c %s -l %d -n %d -Z -M %d' % (addr, BUFFER_LEN, num_byte, MSS)
            bashCommand = 'iperf -c %s -l %d -n %d -M %d' % (addr, BUFFER_LEN, num_byte, MSS)
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        except:
            pass
