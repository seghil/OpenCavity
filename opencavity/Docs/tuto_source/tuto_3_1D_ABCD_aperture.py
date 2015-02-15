# -*- coding: utf-8 -*-
'''

@author: M.seghilani
'''
import opencavity.modesolver as ms 
   
   
R1=1e13; R2=10*1e3; Lc=8*1e3; npts=100; a=200; # cavity parameters; R1 very large = plane mirror
A1=1; B1=0; C1=-2/R1; D1=1; #concave mirror M1
A2=1; B2=Lc; C2=0; D2=1;    #propagation distance Lc
   
A3=1; B3=0; C3=-2/R2; D3=1; #concave mirror M2
A4=1; B4=Lc; C4=0; D4=1;    #propagation distance Lc
M1=ms.np.array([[A1,B1 ],[C1, D1]]); M2=ms.np.array([[A2, B2],[C2, D2]]); 
M3=ms.np.array([[A3, B3],[C3, D3]]); M4=ms.np.array([[A4, B4],[C4, D4]]);

M11=M2.dot(M1); M22=M4.dot(M3); # sub-system 2 
A11=M11[0,0]; B11=M11[0,1]; C11=M11[1,0]; D11=M11[1,1] # getting the members of subsystem 1 matrix
A22=M22[0,0]; B22=M22[0,1]; C22=M22[1,0]; D22=M22[1,1] # getting the members of subsystem 2 matrix
   
# enter transfer matrices to create a system
   
sys1=ms.CavEigenSys();  
sys2=ms.CavEigenSys();
  
sys1.build_1D_cav_ABCD(a,npts,A11,B11,C11,D11) #
sys2.build_1D_cav_ABCD(a,npts,A22,B22,C22,D22) # to reinitialize the sub-system 
   
# just a small loop to create an aperture (amplitude =0 (no transmission) if radius >50 )
aperture= ms.np.ones(npts)
   
for k in range(npts):
    if ms.np.abs(sys1.x1[k])>50:
        aperture[k]=0
      
ms.plt.clf()   # clear figure
ms.plt.plot(sys1.x1,aperture); # plots the aperture function
sys1.apply_mask1D(aperture); # apply the aperture to the subsystem 1 =on the mirror 1
#sys2.apply_mask1D(aperture); # apply the aperture to the subsystem 2 =on the mirror 2
sys1.cascade_subsystem(sys2)

sys1.solve_modes()
sys1.show_mode(0,what='intensity')
sys1.show_mode(1,what='intensity')
 
l0,v0=sys1.get_mode1D(0) #l: eigenvalue; v: eigenmode
l1,v1=sys1.get_mode1D(1) 
print(1-ms.np.abs(l0)**2,1-ms.np.abs(l1)**2)