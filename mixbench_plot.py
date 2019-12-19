import matplotlib.pyplot as plt
import numpy as np
import re

fig, ax = plt.subplots()

format_string="{:<17} max bandwidth {:6.2f} (GB/sec) {:7.2f} GFlops/sec; Achievable GFlops/sec {:6.2f} MatMul GFlops/sec {:7.2f}"

# Plotting application lines for 65 Flops/word and 1 Flop/word
application_gflops=[0, 125*65]
application_bandwidth=[0, 1000]

plt.plot(application_bandwidth, application_gflops, linestyle='--', color='black')
#angle = (180/np.pi)*np.arctan( application_gflops[1]/application_bandwidth[1])
#plt.text(float(200),float(4500), "Matrix Multiplication Application", rotation=angle)
p1 = ax.transData.transform_point((float(application_bandwidth[0]), float(application_gflops[0])))
p2 = ax.transData.transform_point((float(application_bandwidth[1]), float(application_gflops[1])))
dy = (float(p2[1]) - float(p1[1]))
dx = (float(p2[0]) - float(p1[0]))
rotn = np.degrees(np.arctan2(float(dy), float(dx))) + 4.0
xylabel = ((application_bandwidth[0]+application_bandwidth[1])*2/5-20, (application_gflops[0]+application_gflops[1])*2/5+40)
ax.annotate('Matrix Multiplication Application', xy=xylabel, ha='center', va='center', rotation=rotn, color='black')

application_gflops=[0, 125]
application_bandwidth=[0, 1000]

plt.plot(application_bandwidth, application_gflops, linestyle='-', color='black')
angle = (180/np.pi)*np.arctan( application_gflops[1]/application_bandwidth[1])
plt.text(float(500),float(200), "Typical 1 flop/word Application", rotation=angle, color='black')

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

#plt.plot(V100_bandwidth, V100_gflops, "o", linestyle='-')
plt.plot(max_V100_bandwidth, max_V100_gflops, "X", color='#76b900')
plt.text(max_V100_bandwidth+20, max_V100_gflops+20, "V100", color='#76b900')

#Start Vega20 plot

Vega20_gflops = []
Vega20_bandwidth = []

data = open('Vega20.data', 'r')

for line in data:
    if re.match('^      ',line):
        words = line.split()
        dummy, dummy, dummy, dummy, dummy, dummy,  dummy, gflops_in, bandwidth_in, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy = line.split(",")
        Vega20_gflops.append(float(gflops_in))
        Vega20_bandwidth.append(float(bandwidth_in))
        

max_Vega20_bandwidth=max(Vega20_bandwidth)
max_Vega20_gflops=max(Vega20_gflops)
achievable_Vega20_gflops=max_Vega20_bandwidth/8.0

print(format_string.format("Vega20", max_Vega20_bandwidth, max_Vega20_gflops, achievable_Vega20_gflops, max_Vega20_bandwidth*65/8))

#plt.plot(Vega20_bandwidth, Vega20_gflops, "o", linestyle='-')
plt.plot(max_Vega20_bandwidth, max_Vega20_gflops, "X", color='#DF002D')
plt.text(max_Vega20_bandwidth-110, max_Vega20_gflops+20, "Vega20", color='#DF002D')

#Start P100 plot

P100_gflops = []
P100_bandwidth = []

data = open('P100.data', 'r')

for line in data:
    if re.match('^      ',line):
        words = line.split()
        dummy, dummy, dummy, dummy, dummy, dummy,  dummy, gflops_in, bandwidth_in, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy = line.split(",")
        P100_gflops.append(float(gflops_in))
        P100_bandwidth.append(float(bandwidth_in))
        

max_P100_bandwidth=max(P100_bandwidth)
max_P100_gflops=max(P100_gflops)
achievable_P100_gflops=max_P100_bandwidth/8.0

print(format_string.format("P100", max_P100_bandwidth, max_P100_gflops, achievable_P100_gflops, max_P100_bandwidth*65/8))

#plt.plot(P100_bandwidth, P100_gflops, "o", linestyle='-')
plt.plot(max_P100_bandwidth, max_P100_gflops, "X", color='green')
plt.text(max_P100_bandwidth-80, max_P100_gflops+10, "P100", color='green')

#Start GeForce_GTX1080Ti plot

GeForce_GTX1080Ti_gflops = []
GeForce_GTX1080Ti_bandwidth = []

data = open('GeForce_GTX1080Ti.data', 'r')

for line in data:
    if re.match('^      ',line):
        words = line.split()
        dummy, dummy, dummy, dummy, dummy, dummy,  dummy, gflops_in, bandwidth_in, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy = line.split(",")
        GeForce_GTX1080Ti_gflops.append(float(gflops_in))
        GeForce_GTX1080Ti_bandwidth.append(float(bandwidth_in))
        

max_GeForce_GTX1080Ti_bandwidth=max(GeForce_GTX1080Ti_bandwidth)
max_GeForce_GTX1080Ti_gflops=max(GeForce_GTX1080Ti_gflops)
achievable_GeForce_GTX1080Ti_gflops=max_GeForce_GTX1080Ti_bandwidth/8.0

print(format_string.format("GeForce GTX1080Ti", max_GeForce_GTX1080Ti_bandwidth, max_GeForce_GTX1080Ti_gflops, achievable_GeForce_GTX1080Ti_gflops,max_GeForce_GTX1080Ti_gflops))

#plt.plot(GeForce_GTX1080Ti_bandwidth, GeForce_GTX1080Ti_gflops, "o", linestyle='-')
plt.plot(max_GeForce_GTX1080Ti_bandwidth, max_GeForce_GTX1080Ti_gflops, "X", color='#75BA01')
plt.text(max_GeForce_GTX1080Ti_bandwidth+10, max_GeForce_GTX1080Ti_gflops+10, "GeForce GTX1080Ti", color='#75BA01')

#Start Quadro_K6000 plot

Quadro_K6000_gflops = []
Quadro_K6000_bandwidth = []

data = open('Quadro_K6000.data', 'r')

for line in data:
    if re.match('^      ',line):
        words = line.split()
        dummy, dummy, dummy, dummy, dummy, dummy,  dummy, gflops_in, bandwidth_in, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy = line.split(",")
        Quadro_K6000_gflops.append(float(gflops_in))
        Quadro_K6000_bandwidth.append(float(bandwidth_in))
        
max_Quadro_bandwidth=max(Quadro_K6000_bandwidth)
max_Quadro_gflops=max(Quadro_K6000_gflops)
achievable_Quadro_gflops=max_Quadro_bandwidth/8.0

print(format_string.format("Quadro K6000", max_Quadro_bandwidth, max_Quadro_gflops, achievable_Quadro_gflops,max_Quadro_gflops))

#plt.plot(Quadro_K6000_bandwidth, Quadro_K6000_gflops, "o", linestyle='-')
plt.plot(max_Quadro_bandwidth, max_Quadro_gflops, "X", color='#004FFF')
plt.text(max_Quadro_bandwidth+10, max_Quadro_gflops+10, "Quadro K6000", color='#004FFF')

#Start TeslaS2050 plot

max_TeslaS2050_bandwidth = 148
max_TeslaS2050_gflops = 514
achievable_TeslaS2050_gflops=max_TeslaS2050_bandwidth/8.0

print(format_string.format("Tesla S2050", max_TeslaS2050_bandwidth, max_TeslaS2050_gflops, achievable_TeslaS2050_gflops,max_TeslaS2050_gflops))
plt.plot(max_TeslaS2050_bandwidth, max_TeslaS2050_gflops, "X", color='#66FFFF')
plt.text(max_TeslaS2050_bandwidth+20, max_TeslaS2050_gflops+20, "Tesla S2050", color='#66FFFF')

# Plotting performance limitation lines
plt.plot([max_V100_bandwidth,max_V100_bandwidth],[achievable_V100_gflops,max_V100_gflops],linestyle='-',color='#76b900')
plt.plot([max_V100_bandwidth,max_V100_gflops*8/65],[max_V100_gflops,max_V100_gflops],linestyle='-',color='#76b900')
plt.plot([max_Vega20_bandwidth,max_Vega20_bandwidth],[achievable_Vega20_gflops,max_Vega20_gflops],linestyle='-', color='#DF002D')
plt.plot([max_P100_bandwidth,max_P100_bandwidth],[achievable_P100_gflops,max_P100_gflops],linestyle='-', color='green')
plt.plot([max_GeForce_GTX1080Ti_bandwidth,max_GeForce_GTX1080Ti_bandwidth],[achievable_GeForce_GTX1080Ti_gflops,max_GeForce_GTX1080Ti_gflops],linestyle='-',color='#75BA01')
plt.plot([max_GeForce_GTX1080Ti_bandwidth,max_GeForce_GTX1080Ti_gflops*8/65],[max_GeForce_GTX1080Ti_gflops,max_GeForce_GTX1080Ti_gflops],linestyle='-',color='#75BA01')
plt.plot([max_Quadro_bandwidth,max_Quadro_bandwidth],[achievable_Quadro_gflops,max_Quadro_gflops],linestyle='-', color='#004FFF')
plt.plot([max_Quadro_bandwidth,max_Quadro_gflops*8/65],[max_Quadro_gflops,max_Quadro_gflops],linestyle='-', color='#004FFF')
plt.plot([max_TeslaS2050_bandwidth,max_TeslaS2050_bandwidth],[achievable_TeslaS2050_gflops,max_TeslaS2050_gflops],linestyle='-', color='#66FFFF')
plt.plot([max_TeslaS2050_bandwidth,max_TeslaS2050_gflops*8/65],[max_TeslaS2050_gflops,max_TeslaS2050_gflops],linestyle='-', color='#66FFFF')

axes = plt.gca() # get current axes
axes.set_xlim([0,1000])
axes.set_ylim([1,7000])

ax.grid()

plt.xlabel('Memory Bandwidth (GB/sec)',fontsize=16)
plt.ylabel('Compute Rate (GFlops/sec)',fontsize=16)

fig.tight_layout()
plt.savefig("mixbench.pdf")
plt.savefig("mixbench.svg")
plt.savefig("mixbench.png", dpi=900)

plt.show()
