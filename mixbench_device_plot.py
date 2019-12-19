import matplotlib.pyplot as plt
import numpy as np
import re

fig, ax = plt.subplots()

format_string="{:<17} max bandwidth {:6.2f} (GB/sec) {:7.2f} GFlops; Achievable GFlops {:6.2f} MatMul GFlops {:7.2f}"

#Start V100 plot

V100_gflops = []
V100_bandwidth = []

# Collect the data from the file, ignore empty lines
data = open('V100-power9.data', 'r')

for line in data:
    if re.match('^      ',line):
        words = line.split()
        dummy, dummy, dummy, dummy, dummy, dummy,  dummy, gflops_in, bandwidth_in, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy = line.split(",")
        V100_gflops.append(float(gflops_in))
        V100_bandwidth.append(float(bandwidth_in))

max_V100_bandwidth=max(V100_bandwidth)
max_V100_gflops=max(V100_gflops)
achievable_V100_gflops=max_V100_bandwidth/8.0

print(format_string.format("V100", max_V100_bandwidth, max_V100_gflops, achievable_V100_gflops, max_V100_gflops))

plt.plot(V100_bandwidth, V100_gflops, "o", linestyle='-', color='#76b900')
plt.plot(max_V100_bandwidth, max_V100_gflops, "X", color='#76b900')
plt.text(max_V100_bandwidth+20, max_V100_gflops+20, "V100")

axes = plt.gca() # get current axes
axes.set_xlim([0,1000])
axes.set_ylim([1,7000])

ax.grid()

plt.xlabel('Memory Bandwidth (GB/sec)',fontsize=16)
plt.ylabel('Compute Rate (GFlops/sec)',fontsize=16)

fig.tight_layout()
plt.savefig("mixbench_device.pdf")
plt.savefig("mixbench_device.svg")
plt.savefig("mixbench_device.png", dpi=900)

plt.show()
