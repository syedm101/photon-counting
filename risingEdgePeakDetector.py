import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import scipy.signal


# filename  
dataset = "2018.10.29_18.57.37_1"
zero_level = 7980
photon_ranges = [60, 170] # 2peak min, 3 peak min
diff_threshold = 50
rising_event_window = 10

matA = scipy.io.loadmat('./data/'+dataset+'.A.mat')
matB = scipy.io.loadmat('./data/'+dataset+'.B.mat')

# This is the filtering Channel
x1 = matB['T1'][0,:]
y1 = matB['Y1'][0,:]

#subtract out the zero level
yt_filter = y1.astype(int)
yt_filter -= zero_level

#need to customize this probably
scipy.signal.savgol_filter(yt_filter, 4, 3)





