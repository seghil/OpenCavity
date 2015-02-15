# -*- coding: utf-8 -*-
'''
Created on 17 sept. 2014

@author: Mohamed
'''
from opencavity.beams import HgBasis
from opencavity.propagators import FresnelProp
import numpy as np
import matplotlib.pylab as plt

H=HgBasis(1,30,30) #creating the Hermite-Gauss basis with initial waist equals to 100 microns
z=0.000000000000000001

W_lc=H.Wx(z) #we simply measure the waist of the beam to adapt the plot window
print W_lc
x=np.linspace(-5*20, 5*20,215); y=x
tem00=H.generate_hg(2,0, x,0, z) # the TEM00 gaussian beam for y=0 so no y component and for z=0 so at the waist.
#plt.Figure()
#plt.subplot(211)
#plt.plot(x,np.abs(tem00),'r')
#plt.subplot(212)
#plt.plot(x,np.angle(tem00),'r')
#plt.show()

# create an ABCD matrix to propagate the beam 
L1=1*1e3*1;# mm
f=10*1e3; #mm converging lens FL
#R=-0.2*1e3; dn=0.5;  #n2-n1=1.5-1
#f=R/(2*dn); 

L2=10e3;# mm
#  definition of the ABCD matrices     
M1=np.array([[1, L1],[0, 1]]); M2=np.array([[1, 0],[-1/f, 1]]); M3=np.array([[1, L2],[0, 1]])
M=M3.dot(M2).dot(M1) # calculating the global matrix 
#M=M3.dot(M1)


opSys=FresnelProp()

T_lens=np.exp((1j*opSys.k/(2*f))*(x-0)**2);
opSys.set_start_beam(tem00, x)
opSys.set_ABCD(M1)
#opSys.apply_mask1D(T_lens)
#opSys.propagate1D_ABCD(x2=4*x)
opSys.propagate1Dfft(x2=4*x)
opSys.show_result_beam(what='intensity')
#opSys.show_result_beam(what='phase')

#opSys.yz_prop_chart(5e3,L1,100,30*x)
#opSys.show_prop_yz()
#opSys.show_prop_yz(what='intensity')
plt.show()
