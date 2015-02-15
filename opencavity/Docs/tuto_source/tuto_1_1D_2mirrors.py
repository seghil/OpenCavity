# -*- coding: utf-8 -*-

import opencavity.modesolver as ms

sys=ms.CavEigenSys() #creating a ms object
R1=1e13; R2=10*1e3; Lc=8*1e3; npts=120; a=150; # cavity parameters 

sys.build_1D_cav(a, npts, R1, R2, Lc) # build the system
sys.solve_modes() #solve the modes default n_modes=30

sys.show_mode(0) #plots the E-field of the 1st mode 

sys.show_mode(1,what='intensity') #plots the intensity of the 2nd mode
sys.show_mode(1,what='phase') #plots the phase of the 2nd mode
ms.plt.show()

l,v=sys.get_mode1D(0) #l: eigenvalue; v: eigenmode