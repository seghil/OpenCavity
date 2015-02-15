# -*- coding: utf-8 -*-
'''

@author: M.seghilani
'''

from opencavity.beams import HgBasis
from opencavity.propagators import FresnelProp
import numpy as np
import matplotlib.pylab as plt

waist=100; waist_x=waist; waist_y=waist;
H=HgBasis(1,waist_x,waist_y) #creating the Hermite-Gauss basis with initial waist equals to 100 microns
z=0.000000000000000001

x=np.linspace(-6*waist, 6*waist,80); y=x
X,Y=np.meshgrid(x,y)
tem00=H.generate_hg(0, 0, X, Y, z) # generate TEM00 mode 
plt.pcolor(x,y,np.abs(tem00)); plt.set_cmap('hot')
plt.show()


n=x.size
phase=np.ones((n,n))+1j*np.ones((n,n))
m=2*np.pi

for kx in range (n):
    for ky in range (n):
        phase[kx,ky]=np.exp(1j*m*(np.arctan2(y[ky],x[kx]))/(2*np.pi))
         

# create an ABCD matrix to propagate the beam 
L1=50*1e3;# mm
f1=50*1e3; #mm converging lens FL
L2=190e3;# mm
f2=60e3;
L3=120e3;
L4=140e3;

#  definition of the ABCD matrices  
#first interfero arm   
M1=np.array([[1, L1],[0, 1]]); 
M2=np.array([[1, 0],[-1/f1, 1]]);
M3=np.array([[1, L2],[0, 1]]);
M4=np.array([[1, 0],[-1/f2, 1]]);
M5=np.array([[1, L3],[0, 1]]);
M_arm1=M5.dot(M4).dot(M3).dot(M2).dot(M1) # calculating the global matrix 

#second interfero arm
# L2=140e3+140e3+170e3+140e3;
M1=np.array([[1, L1],[0, 1]]); 
M2=np.array([[1, 0],[-1/f1, 1]]);
M6=np.array([[1, L2+L3+2*L4],[0, 1]]);
M_arm2=M6.dot(M2).dot(M1)


opsys1=FresnelProp()
opsys1.set_start_beam(tem00*phase, x)
opsys1.set_ABCD(M_arm1); x2=1*x; y2=1*y;
opsys1.propagate2D_ABCD(x2)
opsys1.show_result_beam()
#opsys1.show_result_beam(what='phase')
plt.show()

opsys2=FresnelProp()
opsys2.set_start_beam(tem00*phase, x)
opsys2.set_ABCD(M_arm2); x2=1*x; y2=1*y;
opsys2.propagate2D_ABCD(x2-5*100,y2-6*100)
opsys2.show_result_beam(what='intensity')
#opsys2.show_result_beam(what='phase')
plt.show()

inter=0.4*opsys1.U2+opsys2.U2
plt.figure()
plt.pcolor(X,Y,np.abs(inter)**2) # X,Y from the meshgrid
plt.show()
