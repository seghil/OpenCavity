# -*- coding: utf-8 -*-
'''

@author: M.seghilani
'''

import opencavity.modesolver as ms

R1=1e13; R2=10*1e3; Lc=8*1e3; npts=120; a=150; # cavity parameters 
R1=20e3

A1=1; B1=0; C1=-2/R1; D1=1; #concave mirror M1
A2=1; B2=Lc; C2=0; D2=1;    #propagation 
A3=1; B3=0; C3=-2/R2; D3=1; #concave mirror M2
A4=1; B4=Lc; C4=0; D4=1;    #propagation

M1=ms.np.array([[A1,B1 ],[C1, D1]]); M2=ms.np.array([[A2, B2],[C2, D2]]); 
M3=ms.np.array([[A3, B3],[C3, D3]]); M4=ms.np.array([[A4, B4],[C4, D4]]);
M=M1.dot(M2).dot(M3).dot(M4) # calculating the global matrix

A=M[0,0]; B=M[0,1]; C=M[1,0]; D=M[1,1]

opsys=ms.CavEigenSys(); 
opsys.build_1D_cav_ABCD(a,npts,A,B,C,D)
opsys.solve_modes()

opsys.show_mode(0)
opsys.show_mode(2,what='intensity') 
opsys.show_mode(0,what='phase') 
ms.plt.show()
