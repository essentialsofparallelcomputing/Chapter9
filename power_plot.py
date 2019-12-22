import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.integrate import simps

fig, ax1 = plt.subplots()

gpu_power = []
gpu_time = []
sm_utilization = []

# Collect the data from the file, ignore empty lines
data = open('gpu_monitoring.log', 'r')

count = 0
energy = 0.0
nominal_energy = 0.0

for line in data:
    if re.match('^ 2019',line):
        line = line.rstrip("\n")
        #words = line.split()
        print(line)
        dummy, dummy, dummy, gpu_power_in, dummy, dummy,  sm_utilization_in, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy = line.split()
        if (float(sm_utilization_in) > 80):
          gpu_power.append(float(gpu_power_in))
          sm_utilization.append(float(sm_utilization_in))
          gpu_time.append(count)
          count = count + 1
          energy = energy + float(gpu_power_in)*1.0
          nominal_energy = nominal_energy + float(300.0)*1.0
#        V100_gflops.append(float(gflops_in))
#        V100_bandwidth.append(float(bandwidth_in))

print(energy, "watts-secs", simps(gpu_power, gpu_time))
print(nominal_energy, "watts-secs", "  ratio ",energy/nominal_energy*100.0)
        
print(gpu_power)
print(sm_utilization)
print(gpu_time)

ax1.plot(gpu_time, gpu_power, "o", linestyle='-', color='red')
ax1.fill_between(gpu_time, gpu_power, color='orange')
ax1.set_xlabel('Time (secs)',fontsize=16)
ax1.set_ylabel('Power Consumption (watts)',fontsize=16, color='red')
#ax1.set_title('GPU Power Consumption from nvidia-smi')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.plot(gpu_time, sm_utilization, "o", linestyle='-', color='green')
ax2.set_ylabel('GPU Utilization (%)',fontsize=16, color='green')

## Plotting performance limitation lines
#plt.plot([max_V100_bandwidth,max_V100_bandwidth],[achievable_V100_gflops,max_V100_gflops],linestyle='-',color='#76b900')
#plt.plot([max_V100_bandwidth,max_V100_gflops*8/65],[max_V100_gflops,max_V100_gflops],linestyle='-',color='#76b900')
#plt.plot([max_Vega20_bandwidth,max_Vega20_bandwidth],[achievable_Vega20_gflops,max_Vega20_gflops],linestyle='-', color='#DF002D')
#plt.plot([max_P100_bandwidth,max_P100_bandwidth],[achievable_P100_gflops,max_P100_gflops],linestyle='-', color='green')
#plt.plot([max_GeForce_GTX1080Ti_bandwidth,max_GeForce_GTX1080Ti_bandwidth],[achievable_GeForce_GTX1080Ti_gflops,max_GeForce_GTX1080Ti_gflops],linestyle='-',color='#75BA01')
#plt.plot([max_GeForce_GTX1080Ti_bandwidth,max_GeForce_GTX1080Ti_gflops*8/65],[max_GeForce_GTX1080Ti_gflops,max_GeForce_GTX1080Ti_gflops],linestyle='-',color='#75BA01')
#plt.plot([max_Quadro_bandwidth,max_Quadro_bandwidth],[achievable_Quadro_gflops,max_Quadro_gflops],linestyle='-', color='#004FFF')
#plt.plot([max_Quadro_bandwidth,max_Quadro_gflops*8/65],[max_Quadro_gflops,max_Quadro_gflops],linestyle='-', color='#004FFF')
#plt.plot([max_TeslaS2050_bandwidth,max_TeslaS2050_bandwidth],[achievable_TeslaS2050_gflops,max_TeslaS2050_gflops],linestyle='-', color='#66FFFF')
#plt.plot([max_TeslaS2050_bandwidth,max_TeslaS2050_gflops*8/65],[max_TeslaS2050_gflops,max_TeslaS2050_gflops],linestyle='-', color='#66FFFF')
#
#axes = plt.gca() # get current axes
#axes.set_xlim([0,1000])
#axes.set_ylim([1,7000])
#
#ax.grid()

fig.tight_layout()
plt.savefig("power.pdf")
plt.savefig("power.svg")
plt.savefig("power.png", dpi=900)
#
plt.show()
