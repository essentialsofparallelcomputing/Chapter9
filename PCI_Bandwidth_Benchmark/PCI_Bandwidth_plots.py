
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import csv 
import sys
 

# Set the default font settings
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 18}

matplotlib.rc('font', **font)

title_properties = {'fontsize': 18,
                    'fontweight' : 'bold',
                    'verticalalignment': 'baseline',
                    'horizontalalignment': 'center'}

# Read in the Pinned memory bandwidth results
# Pinned memory results will be closer to the theoretial peak bandwidth
bandwidth_results = np.loadtxt(open("h2d_bandwidth_pinned.csv", "rb"),
                               delimiter=",", skiprows=1)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
clrs = sns.color_palette("husl", 5)

# Empirical mean and +/- standard deviation plot
ax.plot(bandwidth_results[:,0],bandwidth_results[:,1], c=(0,0,0))
ax.fill_between(bandwidth_results[:,0], 
                bandwidth_results[:,1]-np.sqrt(bandwidth_results[:,2]),
                bandwidth_results[:,1]+np.sqrt(bandwidth_results[:,2]), 
                alpha=0.3, facecolor=(0,0,0))

# Theoretical Peak Bandwidth Plot
gen3_x16_peak_bandwidth = [15.7536, 15.7536]
gen3_x16_bytesize       = [1, 650000000.0]

ax.plot(gen3_x16_bytesize, gen3_x16_peak_bandwidth, 
        '--', linewidth=2, c=(1,0,0) )

plt.xlabel('Array Size (B)')
plt.ylabel('Bandwidth (GB/s)')
ax.set_xscale('log')
ax.legend(['Benchmark', 'Theoretical Peak'], fontsize=12)
plt.title( 'Theoretical and Benchmark Bandwidth\n Gen3 x16 PCIe', 
           fontdict=title_properties )
plt.savefig("PCIe_Bandwidth_Gen3x16.svg")
plt.show()

