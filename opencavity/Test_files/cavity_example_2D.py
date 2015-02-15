# -*- coding: utf-8 -*-
'''
Created on 13 juil. 2014

@author: seghil
'''
#import matplotlib.pylab as plt
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
from opencavity.utilsfunc import UtilsFunc 
#import numpy as np
#import scipy.sparse.linalg as la
import opencavity.modesolver as oc





utils=UtilsFunc()
sys=oc.CavEigenSys() #creating a oc object
R1=1e13; R2=10*1e3; Lc=8*1e3; npts=64; a=80; # cavity parameters 
#sys.build_2D_cav(a, npts, R1, R2, Lc) 
#x1=sys.x1; y1=sys.y1
## build the matrix-kernel of the cavity system and returns x,y Legendre-Gauss abscissa (for exact integration)    
#
#apert=oc.AmpMask2D(x1,y1) # create a mask object 
#apert.add_circle(100)#create an aperture in x1,y1 coordinates with radius=100
##apert.add_rectangle(3, 50,positive='False')
##apert.add_rectangle(50, 3,positive='False')
#
#apert.add_rectangle(1, 50,positive='False')
#apert.add_rectangle(50, 1,positive='False')
#
#
#apert.show_msk3D()
#sys.apply_mask2D(apert)
#
#g1=1-Lc/R1; g2=1-Lc/R2;
#A1=2*g1*g2-1; B1=2*g2*Lc; C1=2*g1/Lc; D1=2*g1*g2-1;
#sys2=oc.CavEigenSys() #creating a oc object
##sys2.build_2D_cav_ABCD(a, npts, A1,B1,C1,D1)
#
#sys.solve_modes()
##sys2.solve_modes()
##sys.show_mode(0)
##oc.plt.show()

#define the system using ABCD matrix directly

A1=1; B1=0; C1=-2/R1; D1=1; #concave
A2=1; B2=Lc; C2=0; D2=1;    #propagation
A3=1; B3=0; C3=-2/R2; D3=1; #concave
A4=1; B4=Lc; C4=0; D4=1;    #propagation
f=R2/2

M1=oc.np.array([[A1,B1 ],[C1, D1]]); M2=oc.np.array([[A2, B2],[C2, D2]]); 
M3=oc.np.array([[A3, B3],[C3, D3]]); M4=oc.np.array([[A4, B4],[C4, D4]]);
M=M1.dot(M2).dot(M3).dot(M4) # calculating the global matrix
#M=oc.np.dot(M2,M1) # calculating the global matrix  
A=M[0,0]; B=M[0,1]; C=M[1,0]; D=M[1,1]
sys3=oc.CavEigenSys() #creating a oc object
sys3.build_2D_cav_ABCD(a, npts, A,B,C,D)

sys3.solve_modes()
sys3.show_mode(0)
#sys.show_mode(1)
oc.plt.show()

