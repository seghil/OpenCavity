# -*- coding: utf-8 -*-
'''

@author: M.seghilani
'''

import opencavity.modesolver as ms

R1=1e13; R2=10*1e3; Lc=8*1e3; npts=64; a=80; # cavity parameters 
g1=1-Lc/R1; g2=1-Lc/R2;
A1=2*g1*g2-1; B1=2*g2*Lc; C1=2*g1/Lc; D1=2*g1*g2-1;
sys=ms.CavEigenSys() #creating a ms object
sys.build_2D_cav_ABCD(a, npts, A1,B1,C1,D1)

x1=sys.x1; y1=sys.y1

apert=ms.AmpMask2D(x1,y1) # create a mask object 
apert.add_circle(80)#create an aperture in x1,y1 coordinates with radius=80
apert.show_msk3D()
sys.apply_mask2D(apert)

sys.solve_modes()
sys.show_mode(0)
sys.show_mode(1)
sys.show_mode(2)

# add two crossed lossy lines at the center of the mask
apert.add_rectangle(2, 50,positive='False')
apert.add_rectangle(50, 2,positive='False')
apert.show_msk3D()
sys.apply_mask2D(apert)

sys.solve_modes()
sys.show_mode(0,'intensity')
sys.show_mode(1,'intensity')
sys.show_mode(2,'intensity')


ms.plt.show()
