# BSIM-CMG model (DC only) in Python

Updated: 3/28/2018

Python version: v3.6.4

This is an attempt to write a working BSIM-CMG model in Python. Currently DC and RDSMOD = 0 only.

## Usage
Step 1: Add or modify model and instance parameters in 'modelcard.l'

Step 2: Run 'test.py' and see results.

Note: You can compare the results with commercial simulators like HSPICE.

Please help me debug this tool. Send feedback to huanlin@berkeley.edu

## Example modelcard.l
vd = 1.0  
vg = 1.0  
vs = 0.0  
vb = 0.0  
temp = 27.0  
L = 16e-9  
NFIN = 4  
VSAT = 125000  
U0 = 0.025  
DVTSHIFT = 0.01  

## Results
Id =  3.592760184e-04 A  
Ig =  0.000000000e+00 A  
Is = -3.592760184e-04 A  
Ib =  0.000000000e+00 A