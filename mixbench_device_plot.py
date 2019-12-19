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

plt.plot(V100_bandwidth, V100_gflops, "o", linestyle='-')
plt.plot(max_V100_bandwidth, max_V100_gflops, "X")
plt.text(max_V100_bandwidth+20, max_V100_gflops+20, "V100")

# Plotting performance limitation lines
#plt.plot([max_V100_bandwidth,max_V100_bandwidth],[achievable_V100_gflops,max_V100_gflops],linestyle='-')
#plt.plot([max_V100_bandwidth,max_V100_gflops/65*8],[max_V100_gflops,max_V100_gflops],linestyle='-')
#plt.plot([max_Vega20_bandwidth,max_Vega20_bandwidth],[achievable_Vega20_gflops,max_Vega20_gflops],linestyle='-')
#plt.plot([max_P100_bandwidth,max_P100_bandwidth],[achievable_P100_gflops,max_P100_gflops],linestyle='-')
#plt.plot([max_GeForce_GTX1080Ti_bandwidth,max_GeForce_GTX1080Ti_bandwidth],[achievable_GeForce_GTX1080Ti_gflops,max_GeForce_GTX1080Ti_gflops],linestyle='-')
#plt.plot([max_GeForce_GTX1080Ti_bandwidth,max_GeForce_GTX1080Ti_gflops/65*8],[max_GeForce_GTX1080Ti_gflops,max_GeForce_GTX1080Ti_gflops],linestyle='-')
#plt.plot([max_Quadro_bandwidth,max_Quadro_bandwidth],[achievable_Quadro_gflops,max_Quadro_gflops],linestyle='-')
#plt.plot([max_Quadro_bandwidth,max_Quadro_gflops/65*8],[max_Quadro_gflops,max_Quadro_gflops],linestyle='-')
#plt.plot([max_TeslaS2050_bandwidth,max_TeslaS2050_bandwidth],[achievable_TeslaS2050_gflops,max_TeslaS2050_gflops],linestyle='-')
#plt.plot([max_TeslaS2050_bandwidth,max_TeslaS2050_gflops/65*8],[max_TeslaS2050_gflops,max_TeslaS2050_gflops],linestyle='-')

axes = plt.gca() # get current axes
axes.set_xlim([0,1000])
axes.set_ylim([1,7000])

ax.grid()

plt.xlabel('Memory Bandwidth (GB/sec)',fontsize=16)
plt.ylabel('Compute Rate (GFLOPS)',fontsize=16)

fig.tight_layout()
plt.savefig("mixbench_device.pdf")
plt.savefig("mixbench_device.svg")
plt.savefig("mixbench_device.png", dpi=900)

plt.show()
