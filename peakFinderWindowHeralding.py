import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.signal import find_peaks


# filename
dataSet = "2018.10.29_18.57.37_1"
zero_level = 7980
photon_ranges = [60, 170] # 2peak min, 3 peak min

matA = scipy.io.loadmat('./data/'+dataSet+'.A.mat')
matB = scipy.io.loadmat('./data/'+dataSet+'.B.mat')

# This is the filtering Channel
x1 = matB['T1'][0,:]
y1 = matB['Y1'][0,:]

yt_filter = np.clip(y1, a_min=zero_level,a_max=None)
yt_filter -= zero_level
#decrese everything by noise threshold, clip to 0

#find peaks in filter cavity
filter_peaks, _ = find_peaks(yt_filter, height=0,distance=15) #peaks are the x indices

# plt.figure()
# # plot graph with detected peaks over it
# plt.plot(x1,yt)
# plt.plot(x1[filter_peaks], yt[filter_peaks], "x")

#formatting
# plt.xticks(rotation='vertical')
# plt.xlabel("Time (s)")
# plt.show(block=True)

# plt.figure()
# plt.hist(yt[filter_peaks], bins=1500, log=False,histtype='step')
# plt.show(block=True)

single_peaks = []
double_peaks = []
triple_peaks = []
for i in range(len(filter_peaks)):
    if yt_filter[filter_peaks[i]] < photon_ranges[0]:
        single_peaks.append(filter_peaks[i])
    elif yt_filter[filter_peaks[i]] < photon_ranges[1]:
        double_peaks.append(filter_peaks[i])
    else:
        triple_peaks.append(filter_peaks[i])

#only use single photon peaks for heralding calculation
filter_peaks = single_peaks

#do the same for the OPO channel
x2 = matA['T1'][0,:]
y2 = matA['Y1'][0,:]

yt_opo = np.clip(y2, a_min=zero_level,a_max=None)
yt_opo -= zero_level

opo_peaks, _ = find_peaks(yt_opo, height=0,distance=15) #peaks are the x indices

#would want to use a set data structure for B for faster run-time
def peakInRange(peakI, peaksA,rng):
    for i in range(-rng,rng+1):
        if (peakI+i in peaksA):
            return True
    return False
        
def findRatioInRange(rng,filter_peaks, opo_peaks):
    coincidences= 0
    for peakI in filter_peaks:
        if peakInRange(peakI,opo_peaks,rng):
            coincidences+=1
    return coincidences/len(filter_peaks)

#heralding ratios for different windows
ratios = []
for i in range (0,20):
    ratios.append(findRatioInRange(i, filter_peaks, opo_peaks))
    print("window: "+ str(i), " ratio: " + str(ratios[i]))

