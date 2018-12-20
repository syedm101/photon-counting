import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.signal import find_peaks

peak_width = 10

folder = "./data/Nov29/Nov_21_Data_Phase_6/Displacement_ND_7.7_both/"
filter_single_photon_level = 86
opo_single_photon_level = 86

photon_ranges = [150, 210] # 2peak min, 3 peak min
opo_photon_ranges = [180,240] #,310 for triple

def windowWigner(matA, matB, peak_width):
    # This is the filtering Channel
    x1 = matB['T1'][0,:]
    y1 = matB['Y1'][0,:]

    yt_filter = y1.astype(float)
    yt_filter -= np.mean(y1)
    #decrese everything by noise threshold, clip to 0

    #find peaks in filter cavity, seperated by 10
    filter_peaks, _ = find_peaks(yt_filter, height=filter_single_photon_level,distance=7,prominence=75) #peaks are the x indices

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

    print("filter single photon prob: " + str(len(single_peaks)/len(filter_peaks)))
    print("filter double photon prob: " + str(len(double_peaks)/len(filter_peaks)))
    print("filter triple photon prob: " + str(len(triple_peaks)/len(filter_peaks)))

    #only use single photon peaks for heralding calculation
    filter_peaks = single_peaks

    #do the same for the OPO channel
    x2 = matA['T1'][0,:]
    y2 = matA['Y1'][0,:]
    yt_opo = y2.astype(float)
    yt_opo -= np.mean(y2)

    opo_peaks, _ = find_peaks(yt_opo, height=opo_single_photon_level,distance=7,prominence=60) #peaks are the x indices

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

    print("opo single photon prob: " + str(len(opo_single_peaks)/len(opo_peaks)))
    print("opo double photon prob: " + str(len(opo_double_peaks)/len(opo_peaks)))
    print("opo triple photon prob: " + str(len(opo_triple_peaks)/len(opo_peaks)))

    return findRatioInRange(int(peak_width/2), filter_peaks, opo_peaks, opo_single_peaks, opo_double_peaks, opo_triple_peaks)


#would want to use a set data structure for B for faster run-time
#returns -1 if not found, else the index
def peakInRange(peakI, peaksA,rng):
    for i in range(-rng,rng+1):
        if (peakI+i in peaksA):
            return peakI+i
    return -1

#returns wigner function value and the heralding ratio   
# Perhaps change parameters to automatically handle all the opo stats in 1 tuple
def findRatioInRange(rng,filter_peaks, opo_peaks, opo_single_peaks, opo_double_peaks, opo_triple_peaks):
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
    print("0 photon opo coincidence: " + str(zero_coincidences) + " " + str(zero_coincidences/len(filter_peaks)))
    print("1 photon opo coincidence: " + str(single_coincidences) + " " + str(single_coincidences/len(filter_peaks)))
    print("2 photon opo coincidence: " + str(double_coincidences) + " " + str(double_coincidences/len(filter_peaks)))
    print("3 photon opo coincidence: " + str(triple_coincidences) + " " + str(triple_coincidences/len(filter_peaks)))
    wigner = (zero_coincidences-single_coincidences+double_coincidences-triple_coincidences)/len(filter_peaks)/3.1415926

    return wigner, single_coincidences/len(filter_peaks)

#iterate through files in folder
files = os.listdir(folder)
wigner = []
heralding = []
for i in range(len(files)):
    if files[i].endswith(".A.mat"):
        matA = scipy.io.loadmat(folder + files[i])
        matB = scipy.io.loadmat(folder + files[i+1])
        wig, herald = windowWigner(matA, matB, peak_width)
        wigner.append(wig)
        heralding.append(herald)

        print(files[i],files[i+1])
        print(wigner)
        print(heralding)

plt.plot(wigner)
plt.show()