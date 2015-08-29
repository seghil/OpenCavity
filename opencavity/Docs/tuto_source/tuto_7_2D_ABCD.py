# -*- coding: utf-8 -*-

import opencavity.modesolver as ms
import numpy as np #import numerical Python 

R1=1e13; R2=10*1e3; Lc=8*1e3; npts=64; a=100; # cavity parameters
M1=np.array([[1,0 ],[-2/R1, 1]]);   #concave mirror M1 
M2=np.array([[1, Lc],[0, 1]]);  #propagation distance Lc
M3=np.array([[1, 0],[-2/R2, 1]]); #concave mirror M2
M4=np.array([[1, Lc],[0, 1]]); #propagation distance Lc
M=M4.dot(M3).dot(M2).dot(M1) # calculating the global matrix (note the inversed order)

A=M[0,0]; B=M[0,1]; C=M[1,0]; D=M[1,1]   
opsys=ms.CavEigenSys() #creating a Cavity eigensolver object
opsys.build_2D_cav_ABCD(a, npts, A,B,C,D)
opsys.solve_modes()    

# show some modes 
opsys.show_mode(0)
opsys.show_mode(0,what='phase')
opsys.show_mode(1,what='intensity')
opsys.show_mode(1,what='phase')
opsys.show_mode(2,what='intensity')
opsys.show_mode(2,what='phase')

l,v=opsys.get_mode2D(0);# l: eigenvalue, v: eigenvector (the mode)
print (1-np.abs(l)**2)*100 # in percent
l,v=opsys.get_mode2D(2);
print (1-np.abs(l)**2)*100 

ms.plt.show()