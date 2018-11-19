import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.signal import find_peaks


# filename  
dataSet = "2018.10.29_18.57.37_1"
filter_single_photon_level = 8146
opo_single_photon_prominence = 100
photon_ranges = [170, 170] # 2peak min, 3 peak min

matA = scipy.io.loadmat('./data/'+dataSet+'.A.mat')
matB = scipy.io.loadmat('./data/'+dataSet+'.B.mat')

# This is the filtering Channel
x1 = matB['T1'][0,:]
y1 = matB['Y1'][0,:]

#opo channel
x2 = matA['T1'][0,:]
y2 = matA['Y1'][0,:]

# x1 = x1[10000:100000]
# y1 = y1[10000:100000]

# x2 = x2[10000:100000]
# y2 = y2[10000:100000]
print(len(x2))
#smooth data
# y1 = scipy.signal.savgol_filter(y1, 37, 7)


# plt.figure()
# plt.plot(x1,y1)
# plt.show(block=True)

# plt.figure()
# plt.title("Raw Histogram")
# plt.hist(y1, bins=1500, log=True,histtype='step')
# plt.show(block=True)

#subtract out the zero level
yt_filter = np.clip(y1, a_min=filter_single_photon_level,a_max=None)
yt_filter -= filter_single_photon_level

plt.figure()
plt.title("Raw clipped filter data")
plt.plot(x1,yt_filter)
plt.show(block=True)

#zero the opo data

yt_opo = y2.astype(float)
yt_opo -= np.mean(y2)

filter_peaks , _ = find_peaks(yt_filter, height=0,distance=15) #peaks are the x indices
print("filter peak#: ", len(filter_peaks))


mulChannel = yt_filter * yt_opo
plt.plot(x1,mulChannel)
plt.show(block=True)

mul_peaks, _ = find_peaks(mulChannel, height=10000,distance=15) #peaks are the x indices

print("Heralding Ratio: " + str(len(mul_peaks)/len(filter_peaks)))

