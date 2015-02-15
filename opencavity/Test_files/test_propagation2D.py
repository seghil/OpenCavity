# -*- coding: utf-8 -*-
'''
Created on 18 sept. 2014

@author: Mohamed
'''

from opencavity.beams import HgBasis
from opencavity.propagators import FresnelProp
import numpy as np
import matplotlib.pylab as plt

H=HgBasis(1,100,100) #creating the Hermite-Gauss basis with initial waist equals to 100 microns
z=0.000000000000000001

W_lc=H.Wx(z) #we simply measure the waist of the beam to adapt the plot window
x=np.linspace(-3*W_lc, 3*W_lc,64); y=x
X,Y=np.meshgrid(x,y)
tem00=H.generate_hg(0, 0, X, Y, z)
#plt.imshow(np.abs(tem00),extent=[-10*W_lc, 10*W_lc,-10*W_lc, 10*W_lc])
plt.pcolor(x,y,np.abs(tem00))
#plt.set_cmap('hot')
plt.set_cmap('jet')
plt.show()

# create an ABCD matrix to propagate the beam 
L1=20*1e3;# mm
f=20*1e3; #mm converging lens FL
L2=20e3;# mm
#  definition of the ABCD matrices     
M1=np.array([[1, L1],[0, 1]]); M2=np.array([[1, 0],[-1/f, 1]]); M3=np.array([[1, L2],[0, 1]])
M=M3.dot(M2).dot(M1) # calculating the global matrix 
#M=M3.dot(M2)

opsys=FresnelProp()
opsys.set_start_beam(tem00, x)
opsys.set_ABCD(M)
opsys.propagate2D_ABCD(x2=x)
opsys.show_result_beam()
opsys.show_result_beam(what='phase')
plt.show()