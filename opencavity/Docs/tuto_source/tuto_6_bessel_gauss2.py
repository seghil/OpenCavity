# -*- coding: utf-8 -*-
'''

@author: M.seghilani
'''

import opencavity.modesolver as ms
from opencavity.propagators import FresnelProp
import numpy as np #import numerical Python 

R1=1e18; R2=250*1e3; Lc=78*1e3; npts=500; a=2000; # cavity parameters
M1=np.array([[1,0 ],[-2/R1, 1]]);   #concave mirror M1 
M2=np.array([[1, Lc],[0, 1]]);  #propagation distance Lc
M3=np.array([[1, 0],[-2/R2, 1]]); #concave mirror M2
M4=np.array([[1, Lc],[0, 1]]); #propagation distance Lc
M=M4.dot(M3).dot(M2).dot(M1) # calculating the global matrix (note the inversed order)

M11=M2.dot(M1); M22=M4.dot(M3); # sub-system 2 
A11=M11[0,0]; B11=M11[0,1]; C11=M11[1,0]; D11=M11[1,1] # getting the members of subsystem 1 matrix
A22=M22[0,0]; B22=M22[0,1]; C22=M22[1,0]; D22=M22[1,1] # getting the members of subsystem 2 matrix

sys1=ms.CavEigenSys(wavelength=1.04);  
sys2=ms.CavEigenSys(wavelength=1.04);

sys1.build_1D_cav_ABCD(a,npts,A11,B11,C11,D11) #
sys2.build_1D_cav_ABCD(a,npts,A22,B22,C22,D22) # 

theta=0.5*3.14/180;# reflector is quivalent to refractive axcicon with 2 x theta
T_axicon=ms.np.exp((+1j*sys1.k)*2*theta*(ms.np.sign(sys1.x1))*sys1.x1)

sys1.apply_mask1D(T_axicon)
sys1.cascade_subsystem(sys2)

sys1.solve_modes()

sys1.show_mode(0,what='intensity')
sys1.show_mode(0,what='phase')
l,tem00=sys1.get_mode1D(0)
print 1-np.abs(l)**2



# the output beam & propagation
M00=np.array([[1,Lc ],[0, 1]]);   
M01=np.array([[1,0 ],[(1-1.5)/(-R2*1.5), 1/1.5]]);# -R2  (<0 because it is a concave interface)
M02=np.array([[1,5e3 ],[0, 1]]);   
M03=np.array([[1,1 ],[0, 1.5/1]]);
M04=np.array([[1,100e3 ],[0, 1]]);   
M_out=M04.dot(M03.dot(M02.dot(M01.dot(M00))));

propsys2=FresnelProp()   
l,tem00=sys1.get_mode1D(0) # get the fundamental mode of the cavity    
propsys2.set_start_beam(tem00, sys1.x1) # set the beam to propagate
propsys2.set_ABCD(M_out) # set the ABCD matrix 
propsys2.propagate1D_ABCD(x2=sys1.x1) # calculate the propagation from initial plane to a plane 10 times larger (the beam is wider) 
propsys2.show_result_beam(what='intensity') # show propagation result

U,x=propsys2.get_result_beam()
propsys2.set_start_beam(U, x)
propsys2.yz_prop_chart(-100e3,-50e3,100,0.5*sys1.x1)
propsys2.show_prop_yz()

ms.plt.show()