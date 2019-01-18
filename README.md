# photon-counting

Use `thresholdChooser.py` to determine filter channel and OPO channel photon level thresholds, change these corresponding values in `peakFinderWindowHeralding.py` and then run this program to obtain photon numbers and heralding ratios. `wignerCalculator.py` takes in similar parameters but processes an entire folder to create a Wigner function plot over several data traces, assumed to be at different displacements.

The python notebooks look at different cases of specific data sets for analysis. 

Raj's comment.
Look great, a few more things to add on, 
a). ND 7.7 is still low displacement, It's good to have the Wigner function for higher displacements as well, which is ND7.0 folder. 
b). Bar plots of probalities for both channels as we discussed, in particular OPO for higher displacements.  
c). In ND 7.7 folder, first file is not actually the zero displacement file. For Zero displacement value of Wigner function, just use the heralding dataset because displacement is completely blocked. 


Displacements : 1.414*[0,0.150522604890110,0.154760546075057,0.167290911202892,0.177538728169377,0.192387043015741,0.209983089829007,0.234947906274117,0.244960331475653,0.246170173737210,0.251939962989106,0.275853292761768,0.299713380446613,0.365347291175678,0.404412387545639,0.498520910256696,0.570713426451128,0.636868015650690,0.714050777524613,0.796102627910160]
