# -*- coding: utf-8 -*-

import opencavity.modesolver as oc
from opencavity.propagators import FresnelProp
import numpy as np #import numerical Python 

R1=1e18; R2=250*1e3; Lc=78*1e3; npts=1000; a=2700; # cavity parameters
M1=np.array([[1,0 ],[-2/R1, 1]]);   #concave mirror M1 
M2=np.array([[1, Lc],[0, 1]]);  #propagation distance Lc
M3=np.array([[1, 0],[-2/R2, 1]]); #concave mirror M2
M4=np.array([[1, Lc],[0, 1]]); #propagation distance Lc
M=M4.dot(M3).dot(M2).dot(M1) # calculating the global matrix (note the inversed order)

M11=M2.dot(M1); M22=M4.dot(M3); # sub-system 2 
A11=M11[0,0]; B11=M11[0,1]; C11=M11[1,0]; D11=M11[1,1] # getting the members of subsystem 1 matrix
A22=M22[0,0]; B22=M22[0,1]; C22=M22[1,0]; D22=M22[1,1] # getting the members of subsystem 2 matrix

sys1=oc.CavEigenSys(wavelength=1.04);  
sys2=oc.CavEigenSys(wavelength=1.04);

sys1.build_1D_cav_ABCD(a,npts,A11,B11,C11,D11) #
sys2.build_1D_cav_ABCD(a,npts,A22,B22,C22,D22) # to reinitialize the sub-system 

theta=-0.5*3.14/180;# reflector is quivalent to refractive axcicon with 2 x theta
T_axicon=oc.np.exp((+1j*sys1.k)*2*theta*(oc.np.sign(sys1.x1))*sys1.x1)

sys1.apply_mask1D(T_axicon)
sys1.cascade_subsystem(sys2)

sys1.solve_modes()

sys1.show_mode(0,what='intensity')
sys1.show_mode(0,what='phase')
l,tem00=sys1.get_mode1D(0)
print 1-np.abs(l)**2

#propsys=FresnelProp() # create a propagator object 
#propsys.set_start_beam(tem00, sys1.x1) 
#
#d=-172.0e3
#M=oc.np.array([[1,d ],[0, 1]]);
#propsys.set_ABCD(M)
#propsys.propagate1D_ABCD(x2=sys1.x1/2) # propagate the beam
#propsys.show_result_beam() 
#
#propsys.yz_prop_chart(-250e3,-100e3,100,sys1.x1/2)
#propsys.show_prop_yz()
#propsys.show_prop_yz(what='intensity')
