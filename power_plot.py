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
        (dummy, dummy, dummy, gpu_power_in, dummy, dummy, sm_utilization_in,
         dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy, dummy) = line.split()
        if (float(sm_utilization_in) > 80):
          gpu_power.append(float(gpu_power_in))
          sm_utilization.append(float(sm_utilization_in))
          gpu_time.append(count)
          count = count + 1
          energy = (energy +
                    float(gpu_power_in)*1.0)
          nominal_energy = (nominal_energy + 
                            float(300.0)*1.0)

print(energy, "watts-secs", simps(gpu_power, gpu_time))
print(nominal_energy, "watts-secs", "  ratio ",energy/nominal_energy*100.0)
        
ax1.plot(gpu_time, gpu_power, "o", linestyle='-', color='red')
ax1.fill_between(gpu_time, gpu_power, color='orange')
ax1.set_xlabel('Time (secs)',fontsize=16)
ax1.set_ylabel('Power Consumption (watts)',fontsize=16, color='red')
#ax1.set_title('GPU Power Consumption from nvidia-smi')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.plot(gpu_time, sm_utilization, "o", linestyle='-', color='green')
ax2.set_ylabel('GPU Utilization (%)',fontsize=16, color='green')

fig.tight_layout()
plt.savefig("power.pdf")
plt.savefig("power.svg")
plt.savefig("power.png", dpi=600)

plt.show()
