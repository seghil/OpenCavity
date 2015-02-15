# -*- coding: utf-8 -*-
'''

@author: M.seghilani
'''

import opencavity.modesolver as ms
from opencavity.propagators import FresnelProp

R2=1e13; 
R1=10*1e3; Lc=8*1e3; npts=120; a=250; # cavity parameters 
#R1=15*1e3

g1=1-Lc/R1; g2=1-Lc/R2;
A=2*g1*g2-1; B=2*g2*Lc; C=2*g1/Lc; D=2*g1*g2-1;

print g1*g2
#A1=1; B1=0; C1=-2/R1; D1=1; #concave mirror M1
#A2=1; B2=Lc; C2=0; D2=1;    #propagation 
#A3=1; B3=0; C3=-2/R2; D3=1; #concave mirror M2
#A4=1; B4=Lc; C4=0; D4=1;    #propagation
#
#M1=ms.np.array([[A1,B1 ],[C1, D1]]); M2=ms.np.array([[A2, B2],[C2, D2]]); 
#M3=ms.np.array([[A3, B3],[C3, D3]]); M4=ms.np.array([[A4, B4],[C4, D4]]);
#M=M1.dot(M2).dot(M3).dot(M4) # calculating the global matrix
#
#A=M[0,0]; B=M[0,1]; C=M[1,0]; D=M[1,1]

opsys=ms.CavEigenSys(); 
opsys.build_1D_cav_ABCD(a,npts,A,B,C,D)
opsys.solve_modes()


opsys.show_mode(0); ms.plt.grid()
opsys.show_mode(0,what='phase') 
ms.plt.show()

l,tem00=opsys.get_mode1D(0)
M00=ms.np.array([[0,2*Lc ],[0,1]]);
 
propsys=FresnelProp() # create a propagator object  
propsys.set_start_beam(tem00, opsys.x1)
propsys.set_ABCD(M00)
propsys.propagate1D_ABCD(x2=1*opsys.x1) 
propsys.show_result_beam(); ms.plt.grid()
propsys.show_result_beam(what='phase'); 
#tem00,x2=propsys.get_result_beam()
#propsys.set_start_beam(tem00,x2)
#propsys.yz_prop_chart(-2*Lc,-Lc,50)
#
#propsys.show_prop_yz()
