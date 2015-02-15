# -*- coding: utf-8 -*-
'''
Created on 16 sept. 2014

@author: Mohamed seghilani
'''
import opencavity.modesolver as oc

sys=oc.CavEigenSys() #creating a oc object
R1=1e13; R2=10*1e3; Lc=8*1e3; npts=64; a=150; # cavity parameters 

sys.build_1D_cav(a, npts, R1, R2, Lc)

A1=1; B1=Lc; C1=0; D1=1;
f=R2/2

#g1=1-Lc/R1; g2=1-Lc/R2;
#A1=2*g1*g2-1; B1=2*g2*Lc; C1=2*g1/Lc; D1=2*g1*g2-1;

sys2=oc.CavEigenSys()
sys2.build_1D_cav_ABCD(a,npts,A1,B1,C1,D1)
T_lens=oc.np.exp((1j*sys.k/(2*f))*sys.x1**2);
sys2.apply_mask1D(T_lens)

theta=12.22*1e-3;
T_axicon=oc.np.exp((+1j*sys.k)*theta*(oc.np.sign(sys.x1))*sys.x1)
sys3=oc.CavEigenSys()
sys3.build_1D_cav_ABCD(a,npts,A1,B1,C1,D1)
sys3.apply_mask1D(T_axicon)
sys3.cascade_subsystem(sys2)
sys.solve_modes()
sys3.solve_modes()

sys.show_mode(0)
sys3.show_mode(0)
sys3.show_mode(0,'phase')

oc.plt.show()