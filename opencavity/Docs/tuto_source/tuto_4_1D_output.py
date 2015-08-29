# -*- coding: utf-8 -*-
'''

@author: M.seghilani
'''

import opencavity.modesolver as ms
from opencavity.propagators import FresnelProp

R1=1e13; R2=10*1e3; Lc=8*1e3; npts=120; a=150; # cavity parameters 
g1=1-Lc/R1; g2=1-Lc/R2;
A=2*g1*g2-1; B=2*g2*Lc; C=2*g1/Lc; D=2*g1*g2-1;

opsys=ms.CavEigenSys(); 
opsys.build_1D_cav_ABCD(a,npts,A,B,C,D)
opsys.solve_modes()
opsys.show_mode(0)
#opsys.show_mode(2,what='intensity') 
opsys.show_mode(0,what='phase') 
ms.plt.show()

# creating ABCD matrix of the beam path from the mode calculation plane to the output calculation plane
M00=ms.np.array([[1,Lc ],[0, 1]]);
M01=ms.np.array([[1,0 ],[(1-1.5)/(-R2*1.5), 1/1.5]]);
M02=ms.np.array([[1,5e3 ],[0, 1]]);
M03=ms.np.array([[1,1 ],[0, 1.5/1]]);
M04=ms.np.array([[1,50e3 ],[0, 1]]);

M_out=M04.dot(M03.dot(M02.dot(M01.dot(M00)))); # global matrix 
M_out2=ms.np.array([[1,Lc+5e3+50e3 ],[0, 1]]); # free space ABCD system from mode calculation plane to output calculation plane

l,tem00=opsys.get_mode1D(0)
 
propsys=FresnelProp() # create a propagator object 
propsys2=FresnelProp() 
propsys.set_start_beam(tem00, opsys.x1) 
propsys2.set_start_beam(tem00, opsys.x1)
propsys.set_ABCD(M_out) # set the propagation matrix 
propsys2.set_ABCD(M_out2) 

propsys.propagate1D_ABCD(x2=10*opsys.x1) # propagate the beam 
propsys2.propagate1D_ABCD(x2=10*opsys.x1)

propsys.show_result_beam(what='intensity') # show the propagated beam
propsys2.show_result_beam(what='intensity')

tem00_1,x=propsys.get_result_beam()# fetch propagated beam and abscissa 
tem00_2,x=propsys2.get_result_beam()

print opsys.find_waist(tem00_1,x) # find the wais of the beam
print opsys.find_waist(tem00_2,x)

ms.plt.show()