# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 14:53:51 2014

@author: Mohamed
"""
# -*- coding: utf-8 -*-


import opencavity.modesolver as oc
from opencavity.propagators import FresnelProp

R1=1e13; R2=10*1e3; Lc=8*1e3; npts=120; a=150; # cavity parameters 


A1=1; B1=0; C1=-2/R1; D1=1; #concave mirror M1
A2=1; B2=Lc; C2=0; D2=1;    #propagation 
A3=1; B3=0; C3=-2/R2; D3=1; #concave mirror M2
A4=1; B4=Lc; C4=0; D4=1;    #propagation

M1=oc.np.array([[A1,B1 ],[C1, D1]]); M2=oc.np.array([[A2, B2],[C2, D2]]); 
M3=oc.np.array([[A3, B3],[C3, D3]]); M4=oc.np.array([[A4, B4],[C4, D4]]);
M=M1.dot(M2).dot(M3).dot(M4) # calculating the global matrix

A=M[0,0]; B=M[0,1]; C=M[1,0]; D=M[1,1]

opsys=oc.CavEigenSys(); 
opsys.build_1D_cav_ABCD(a,npts,A,B,C,D)
opsys.solve_modes()
opsys.show_mode(0)
#opsys.show_mode(2,what='intensity') 
opsys.show_mode(0,what='phase') 
oc.plt.show()

M00=oc.np.array([[1,Lc ],[0, 1]]);
M01=oc.np.array([[1,0 ],[(1-1.5)/(-R2*1.5), 1/1.5]]);
M02=oc.np.array([[1,5e3 ],[0, 1]]);
M03=oc.np.array([[1,1 ],[0, 1.5/1]]);
M04=oc.np.array([[1,50e3 ],[0, 1]]);

M_out=M04.dot(M03.dot(M02.dot(M01.dot(M00))));
M_out2=oc.np.array([[1,Lc+5e3+50e3 ],[0, 1]]);
#
l,tem00=opsys.get_mode1D(0)

propsys=FresnelProp()
propsys2=FresnelProp()
propsys.set_start_beam(tem00, opsys.x1)
propsys2.set_start_beam(tem00, opsys.x1)
propsys.set_ABCD(M_out)
propsys2.set_ABCD(M_out2)
propsys.propagate1D_ABCD(x2=10*opsys.x1)
propsys2.propagate1D_ABCD(x2=10*opsys.x1)

propsys.show_result_beam(what='intensity')
propsys2.show_result_beam(what='intensity')

tem00_1,x=propsys.get_result_beam()
tem00_2,x=propsys2.get_result_beam()

print opsys.find_waist(tem00_1,x)
print opsys.find_waist(tem00_2,x)