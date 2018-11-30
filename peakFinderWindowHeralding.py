import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.signal import find_peaks


# filename
dataSet = "Nov29/Nov_21_Data_Phase_6/Displacement_ND_7.7_both/2018.11.22_04.57.37_1"

filter_single_photon_level = 86
opo_single_photon_level = 86

photon_ranges = [150, 250] # 2peak min, 3 peak min
opo_photon_ranges = [180,240] #,310 for triple

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

# plt.figure()
# # plot graph with detected peaks over it
# plt.plot(x1,yt_filter)
# plt.plot(x1[filter_peaks],yt_filter[filter_peaks], "x")
# plt.show()

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
#returns -1 if not found, else the index
def peakInRange(peakI, peaksA,rng):
    for i in range(-rng,rng+1):
        if (peakI+i in peaksA):
            return peakI+i
    return -1
        
#gets the opo photon number as well
def findRatioInRange(rng,filter_peaks, opo_peaks):
    zero_coincidences = 0
    single_coincidences = 0
    double_coincidences= 0
    triple_coincidences= 0
    for peakI in filter_peaks:
        peakIndex = peakInRange(peakI,opo_peaks,rng)
        if peakIndex != -1:
            if peakIndex in opo_single_peaks:
                single_coincidences+=1
            elif peakIndex in opo_double_peaks:
                double_coincidences+=1
            elif peakIndex in opo_triple_peaks: 
                triple_coincidences+=1
        else:
            zero_coincidences+=1
    print("0 photon opo coincidence: " + str(zero_coincidences))
    print("1 photon opo coincidence: " + str(single_coincidences))
    print("2 photon opo coincidence: " + str(double_coincidences))
    print("3 photon opo coincidence: " + str(triple_coincidences))
    print("wigner: ",(zero_coincidences-single_coincidences+double_coincidences-triple_coincidences)/len(filter_peaks)/3.1415926)

    return single_coincidences/len(filter_peaks)

#heralding ratios for different windows
ratios = []
peak_width = 50
for i in range (0,int(peak_width/2)):
    ratios.append(findRatioInRange(i, filter_peaks, opo_peaks))
    print("peak width: "+ str(i*2), " ratio: " + str(ratios[i]))

print("Single photon #: " + str(len(single_peaks)))
print("Double photon #: " + str(len(double_peaks)))
print("Triple photon #: " + str(len(triple_peaks)))

# print("opo Single photon #: " + str(single_coincidences))
# print("opo Double photon #: " + str(double_coincidences))
# print("opo Triple photon #: " + str(triple_coincidences))

plt.plot(ratios)
plt.title("peak width/2 by ratio")
plt.show()