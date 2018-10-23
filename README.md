# photon-counting

Comments on data analysis - A great start! 

Data Processing: 
0.1 You can define the noise threshold by looking at the whole data set, it will be very clear to you about what Voltage value is actual signal, you can just zero them or just get rid of that data. You can also see the code in Niranjan's thesis at the very end, he also has noisethres and even offset the data to get rid of white noise. It seems that in your data threshold happens to be 8060ish. 

0.2 Yes, the very first histogram is the background noise, in particular blackbody radiation. We don't need to worry about it,in fact you can get rid of that by picking a noise thres. 

0.3 I am not sure how good is your analysis in picking pileup events, have you looked into it? The peaks you had in the notebook don't have pile ups. 


0.3 https://arxiv.org/pdf/1808.08830.pdf I found this paper yesterday, it seems like they are dealing with this issue now. It's a new paper where they started using TES with CW laser. It exacly solve what we are working on. Good news in a way what we are solving a real issue, bad news - they used this schmidt trigger while acquiring the data. I need to look into that. 
