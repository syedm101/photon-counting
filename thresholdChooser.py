import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.signal import find_peaks, correlate


# filename  
dataSet = "Nov29/Nov_21_Data_Phase_6/Displacement_ND_7.0_both/2018.11.22_04.50.04_1"
matA = scipy.io.loadmat('./data/'+dataSet+'.A.mat')
matB = scipy.io.loadmat('./data/'+dataSet+'.B.mat')

xf = matB['T1'][0,:]
yf = matB['Y1'][0,:]

xo = matA['T1'][0,:]    
yo = matA['Y1'][0,:]

#subtract out the zero level
yt_filter = yf.astype(float)
filter_mean = np.mean(yt_filter)
yt_filter -= filter_mean
print("filter mean is: " + str(filter_mean))

plt.figure()
plt.title("Centered Raw Filter Data")
plt.plot(yt_filter)
plt.show()

yt_opo = yo.astype(float)
opo_mean = np.mean(yt_opo)
yt_opo -= opo_mean
print("opo mean: " + str(opo_mean))

plt.figure()
plt.title("Centered Raw OPO Data")
plt.plot(yt_opo)
plt.show()


def peakAnalyzer(x,y):
    height = int(input())
    #find peaks in filter cavity
    peaks, _ = find_peaks(y, height=height,distance=7, prominence=60) #peaks are the x indices
    print("peak#: ", len(peaks))

    plt.figure()
    # plot graph with detected peaks over it
    plt.plot(y)
    plt.plot(peaks, y[peaks], "x")

    # formatting
    plt.xticks(rotation='vertical')
    plt.xlabel("Datapoint Number")
    plt.show(block=True)

    #histogram of filter peak heights
    plt.figure()
    plt.hist(y[peaks], bins=1500, log=False,histtype='step')
    plt.show(block=True)

while (True):
    print("Choose your min filter channel photon level threshold")
    peakAnalyzer(xf, yt_filter)

    print("Choose your min opo channel photon level threshold")
    peakAnalyzer(xo, yt_opo)
