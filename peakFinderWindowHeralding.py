import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.signal import find_peaks


# filename
dataSet = "Nov 18th/2018.11.18_16.11.12_1"

filter_single_photon_level = 90
opo_single_photon_level = 90

photon_ranges = [300, 500] # 2peak min, 3 peak min
opo_photon_ranges = [160,300]

matA = scipy.io.loadmat('./data/'+dataSet+'.A.mat')
matB = scipy.io.loadmat('./data/'+dataSet+'.B.mat')

# This is the filtering Channel
x1 = matB['T1'][0,:]
y1 = matB['Y1'][0,:]


# yt_filter = np.clip(y1, a_min=filter_single_photon_level,a_max=None)
# yt_filter -= filter_single_photon_level
yt_filter = y1.astype(float)
yt_filter -= np.mean(y1)
#decrese everything by noise threshold, clip to 0

#find peaks in filter cavity
filter_peaks, _ = find_peaks(yt_filter, height=filter_single_photon_level,distance=10,prominence=50) #peaks are the x indices

plt.figure()
# plot graph with detected peaks over it
plt.plot(x1,yt_filter)
plt.plot(x1[filter_peaks],yt_filter[filter_peaks], "x")
plt.show()

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

single_peaks = np.asarray(single_peaks)
double_peaks = np.asarray(double_peaks)
triple_peaks = np.asarray(triple_peaks)

#only use single photon peaks for heralding calculation
filter_peaks = single_peaks

#do the same for the OPO channel
x2 = matA['T1'][0,:]
y2 = matA['Y1'][0,:]

# yt_opo = np.clip(y2, a_min=opo_single_photon_level,a_max=None)
# yt_opo -= opo_single_photon_level
yt_opo = y2.astype(float)
yt_opo -= np.mean(y2)

opo_peaks, _ = find_peaks(yt_opo, height=opo_single_photon_level,distance=10,prominence=50) #peaks are the x indices

opo_single_peaks = []
opo_double_peaks = []
opo_triple_peaks = []
for i in range(len(opo_peaks)):
    if yt_opo[opo_peaks[i]] < opo_photon_ranges[0]:
        opo_single_peaks.append(opo_peaks[i])
    elif yt_opo[opo_peaks[i]] < opo_photon_ranges[1]:
        opo_double_peaks.append(opo_peaks[i])
    else:
        opo_triple_peaks.append(opo_peaks[i])

opo_single_peaks = np.asarray(opo_single_peaks)
opo_double_peaks = np.asarray(opo_double_peaks)
opo_triple_peaks = np.asarray(opo_triple_peaks)

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
peak_width = 50
for i in range (0,int(peak_width/2)):
    ratios.append(findRatioInRange(i, filter_peaks, opo_single_peaks))
    print("peak width: "+ str(i*2), " ratio: " + str(ratios[i]))

plt.plot(ratios)
plt.show()