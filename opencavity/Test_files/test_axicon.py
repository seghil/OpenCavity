# -*- coding: utf-8 -*-
"""
@author: Mohamed
"""

# beam propagation through an axicon 

from opencavity.beams import HgBasis
from opencavity.propagators import FresnelProp
import numpy as np
import matplotlib.pylab as plt

# generate the beam 

wavelength=1
waist=200 #wasit of the laser beam 
H=HgBasis(wavelength,waist,waist) #creating the Hermite-Gauss basis with initial waist equals to 100 microns
z0=1e-8

x=np.linspace(-500, 500,500); # abscissa 
tem00=H.generate_hg(0,0, x,0, z0) # the TEM00 gaussian beam for y=0 so no y component and for z=0 so at the waist.
#plt.plot(x,np.abs(tem00)**2,'r')

k=2*np.pi/wavelength
theta=0.5*3.14/180;# 0.5 deg axicon (induced phase not real angle)
                    # theta can be approximated : (axicon_index-1)*axicon_base_angle
T_axicon=np.exp((+1j*k)*theta*(np.sign(x))*x)

L=10*1e3;
M=np.array([[1, L],[0, 1]]);

prop=FresnelProp(wavelength)
prop.set_start_beam(tem00,x)
prop.set_ABCD(M)
prop.apply_mask1D(T_axicon)
prop.propagate1D_ABCD()
prop.show_result_beam('intensity')
plt.show()

#plot at several successive planes 
prop.yz_prop_chart(3e3,50e3,100,2*x)
plt.set_cmap('hot')
prop.show_prop_yz()
plt.show()
