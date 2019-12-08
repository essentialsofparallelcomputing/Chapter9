
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
maxbandwidth = max(bandwidth_results[:,1])
ax.plot(bandwidth_results[:,0],bandwidth_results[:,1], c=(0,0,0))
ax.fill_between(bandwidth_results[:,0], 
                bandwidth_results[:,1]-np.sqrt(bandwidth_results[:,2]),
                bandwidth_results[:,1]+np.sqrt(bandwidth_results[:,2]), 
                alpha=0.3, facecolor=(0,0,0))

# Read in the Pageable memory bandwidth results
pageable_bandwidth_results = np.loadtxt(open("h2d_bandwidth_pageable.csv", "rb"),
                               delimiter=",", skiprows=1)
ax.plot(pageable_bandwidth_results[:,0],pageable_bandwidth_results[:,1], '--', c=(0,0,0))
ax.fill_between(pageable_bandwidth_results[:,0], 
                pageable_bandwidth_results[:,1]-np.sqrt(pageable_bandwidth_results[:,2]),
                pageable_bandwidth_results[:,1]+np.sqrt(pageable_bandwidth_results[:,2]), 
                alpha=0.3, facecolor=(0,0,0))

# Theoretical Peak Bandwidth Plot
gen3_x16_peak_bandwidth = [15.7536, 15.7536]
gen3_x16_bytesize       = [1, 650000000.0]

ax.plot(gen3_x16_bytesize, gen3_x16_peak_bandwidth, 
        '--', linewidth=2, c=(1,0,0) )

gen2_x16_peak_bandwidth = [8, 8]
gen2_x16_bytesize       = [1, 650000000.0]

ax.plot(gen2_x16_bytesize, gen2_x16_peak_bandwidth, 
        '-.', linewidth=2, c=(1,0,0) )

gen1_x16_peak_bandwidth = [4, 4]
gen1_x16_bytesize       = [1, 650000000.0]

ax.plot(gen1_x16_bytesize, gen1_x16_peak_bandwidth, 
        ':', linewidth=2, c=(1,0,0) )

plt.xlabel('Array Size (B)')
plt.ylabel('Bandwidth (GB/s)')
ax.set_xscale('log')
ax.set_xlim([10**2,10**8])
ax.set_xticks([10**2,10**3,10**4,10**5,10**6,10**7,10**8])
ax.set_ylim([0,16])
ax.set_yticks(np.arange(0,16,2))
ax.legend(['Pinned Benchmark', 'Pageable Benchmark', 'Gen3 Theoretical Peak', 'Gen2 Theoretical Peak', 'Gen1 Theoretical Peak'], fontsize=12)
plt.title( 'Theoretical and Benchmark Bandwidth\n', 
           fontdict=title_properties )
plt.savefig("PCIe_Bandwidth.svg")
plt.show()

