
**********************************
Tutorial 2 - Generalizes 1D cavity
**********************************

In this part we see how to define a general cavity  system  using a more general method: ABCD matrices, this is a more general and powerful way to define multi-elements cavity with different arrangements (V-shaped, bow-tie...etc), and it is the preferable way of defining optical cavities in OpenCavity.

In this tutorial  we show three ways of defining a general optical cavity using the function ``build_1D_cav_ABCD(a,npts,A,B,C,D)``. You may wonder why learn 3 ways when we can just getting things done by learning one method and stick with it?.

The reason is that every one of the three techniques we show here, is best suited for some particular situations, as we will see in next tutorials. These three ways of defining a general cavity design we address here are:

     - Using the global ABCD matrix of the cavity.
     - Using g1,g2 parameters of the cavity.
     - Using phase masks and cascading subsystems 


System definition using ABCD matrices
=====================================

let’s start now and take the same cavity system of the previous tutorial. This simple two-mirrors linear resonator (radius of curvature R1 and R2) 
represented below is equivalent to a periodic sequence made of two thin lenses with focal lengths equal to f1 (=R1/2) and f2 (=R2/2), spaced by a distance Lc.

.. image:: _static/Optical_cavity_lens.png

The T transfer matrix of such a system is 

.. math::
      \begin{bmatrix} A & B \\ C & D \end{bmatrix}=
      \begin{bmatrix} 1 & 0 \\ -2/R1 & 1 \end{bmatrix} 
      \times \begin{bmatrix} 1 & Lc \\ 0 & 1 \end{bmatrix}
      \times \begin{bmatrix} 1 & 0 \\ -2/R2 & 1 \end{bmatrix}
      \times \begin{bmatrix} 1 & Lc \\ 0 & 1 \end{bmatrix}

Defining this system is quite straightforward , all what we have to do for now is calculating the global matrix.


.. ipython::

   In [1]: import opencavity.modesolver as ms; #importing the opencavity module
   
   In [2]: R1=1e13; R2=10*1e3; Lc=8*1e3; npts=120; a=150; # cavity parameters

   In [3]: A1=1; B1=0; C1=-2/R1; D1=1; #concave mirror M1
      
   In [4]: A2=1; B2=Lc; C2=0; D2=1;    #propagation distance Lc
   
   In [5]: A3=1; B3=0; C3=-2/R2; D3=1; #concave mirror M2
   
   In [6]: A4=1; B4=Lc; C4=0; D4=1;    #propagation distance Lc
   

Making the matrices using ``numerical python``:``np`` , note here that we use numerical python from inside imported ``opencavity`` module that we called ``oc``,
this is possible because ``numerical python`` or ``numpy`` is already imported inside ``opencavity``, but importing it again at the beginning of the script will
work too as we did in other tutorials. The same holds for ``matplotlib`` module imported as ``plt`` in ``opencavity``.

.. ipython::

   In [7]: M1=ms.np.array([[A1,B1 ],[C1, D1]]);   
   
   In [8]: M2=ms.np.array([[A2, B2],[C2, D2]]); 
   
   In [9]: M3=ms.np.array([[A3, B3],[C3, D3]]); 
   
   In [4]: M4=ms.np.array([[A4, B4],[C4, D4]]);

Calculating the dot product (matrix of the global system) 

.. ipython::
 
   In [10]: M=M4.dot(M3).dot(M2).dot(M1) # calculating the global matrix (note the inversed order)

Till now we haven't use the OpenCavity package yet and we haven't done any mode calculation, all what we did is some matrix manipulation to create the ABCD matrix of the cavity. Let's get the elements of this matrix and enter them into a *solver* system, we call it *opsys* (for optical system)

.. ipython::
 
   In [11]: A=M[0,0]; B=M[0,1]; C=M[1,0]; D=M[1,1]
   
   In [12]: opsys=ms.CavEigenSys() #creating a oc object
   
   In [13]: opsys.build_1D_cav_ABCD(a,npts,A,B,C,D) # enter the ABCD matrix and build the system-Kerenl

to find and show the modes of the cavity

.. ipython::
 
   In [14]: opsys.solve_modes() # by default find the 30 first modes
   
   @savefig tuto2_plot_mode0_E_1D.png width=4in
   In [15]: opsys.show_mode(0) # the fundamental mode E-field 
   
   @savefig tuto2_plot_mode2_I_1D.png width=4in
   In [15]: opsys.show_mode(2,what='intensity')  
   
   @savefig tuto2_plot_mode0_P_1D.png width=4in
   In [15]: opsys.show_mode(0,what='phase') 

voilà! these figures show the E-field of the fundamental mode and the intensity of the 2nd one. The third figure shows the phase of the fundamental 
mode.

The cleaned code
================
.. literalinclude::  tuto_source/tuto_2_1D_ABCD_2mirrors.py


.. _tuto2-using-g1g2-label

System definition using g1, g2 parameters
=========================================

g1 and g2 parameters are usually used to study the stability of resonators, they are defined as `g1=1-Lc/R1, g2=1-Lc/R2`. the resonator is sable if 0<g1*g2 <1. The global ABCD matrix of a the resonator can be written in terms of g1, g2 as follows: 

.. math:

   - A=2*g1*g2-1 
   - B=2*g2*Lc 
   - C=2*g1/Lc
   - D=2*g1*g2-1

let's try it:

.. ipython::

   In [1]: import opencavity as oc; #importing the opencavity module
   
   In [2]: R1=1e13; R2=10*1e3; Lc=8*1e3; npts=120; a=150; # cavity parameters
   
   In [2]: g1=1-Lc/R1; g2=1-Lc/R2;
   
   In [2]: A=2*g1*g2-1; B=2*g2*Lc; C=2*g1/Lc; D=2*g1*g2-1;
   
   In [2]: opsys=ms.CavEigenSys();  # create a solver object 
   
   In [2]: opsys.build_1D_cav_ABCD(a,npts,A,B,C,D) # build the cavity kernel 

   In [2]: opsys.solve_modes() # solve the modes 

   @savefig tuto2_plot_mode0_E_1D_g1g2.png width=4in
   In [2]: opsys.show_mode(0); ms.plt.grid() # show the first mode
   
   @savefig tuto2_plot_mode0_P_1D_g1g2.png width=4in
   In [2]: opsys.show_mode(0,what='phase') 
   
   In [2]: ms.plt.show()

We obtain the same results! , the advantage of this method is that the code is cleaner and easy to read as we don't manipulate matrices. Thus the written code 
is quite simple, we can clearly distinguish the needed steps to build and solve the cavity:
   
   -  import the module 
   -  create a solver object 
   -  build the cavity kernel 
   -  solve the modes 
   -  show the modes 
    

cascading subsystems
====================
Calculating the global transfer matrix of an optical cavity is a straightforward method to define it and solve the eigenmodes and eigenvalues, however, sometimes it is useful to split a global complex system to several subsystems, do some transformation on them, then cascade these subsystems to make a global one. This may be inevitable when you want to introduce an amplitude or phase function somewhere inside the cavity, such as an aperture. This is covered in more details in the following tutorials, but for now let's see how to define and solve the modes of the same optical cavity by splitting the global system into two subsystems and cascading them.

We take the same matrices of the first example:

.. ipython::

   In [1]: import opencavity as oc
   
   In [2]: R1=1e13; R2=10*1e3; Lc=8*1e3; npts=120; a=150; # cavity parameters

   In [3]: A1=1; B1=0; C1=-2/R1; D1=1; #concave mirror M1
      
   In [4]: A2=1; B2=Lc; C2=0; D2=1;    #propagation distance Lc
   
   In [5]: A3=1; B3=0; C3=-2/R2; D3=1; #concave mirror M2
   
   In [6]: A4=1; B4=Lc; C4=0; D4=1;    #propagation distance Lc
   

Making the matrices using ``numerical python``:``np``.

.. ipython::

   In [7]: M1=ms.np.array([[A1,B1 ],[C1, D1]]);   
   
   In [8]: M2=ms.np.array([[A2, B2],[C2, D2]]); 
   
   In [9]: M3=ms.np.array([[A3, B3],[C3, D3]]); 
   
   In [4]: M4=ms.np.array([[A4, B4],[C4, D4]]);

Calculating the dot product (matrix of 2 subsy-stems) 

.. ipython::
 
   In [10]: M11=M2.dot(M1); # sub-sytem 1
   
   In [10]: M22=M4.dot(M3); # sub-system 2 
   
   In [10]: A11=M11[0,0]; B11=M11[0,1]; C11=M11[1,0]; D11=M11[1,1] # getting the members of subsystem 1 matrix
    
   In [10]: A22=M22[0,0]; B22=M22[0,1]; C22=M22[1,0]; D22=M22[1,1] # getting the members of subsystem 2 matrix

As in the first example, till now we have just manipulated matrices to create two ABCD matrices representing two subsystems of the cavity. Let's create and build these subsystems:

.. ipython::
 
   In [10]: sys1=ms.CavEigenSys(); 
   
   In [10]: sys2=ms.CavEigenSys()
   
   In [10]: sys1.build_1D_cav_ABCD(a,npts,A11,B11,C11,D11)
   
   In [10]: sys2.build_1D_cav_ABCD(a,npts,A22,B22,C22,D22)
   
   In [10]: sys1.cascade_subsystem(sys2) # cascading subsystems, here: Global Kernel= Kernel2*Kernel1)
   
   In [10]: sys1.solve_modes()
   
   @savefig tuto2_plot_mode0_E_1D_sub.png width=4in
   In [15]: sys1.show_mode(0) # the fundamental mode E-field 
   
   @savefig tuto2_plot_mode2_I_1D_sub.png width=4in
   In [15]: sys1.show_mode(2,what='intensity')  
   
   @savefig tuto2_plot_mode0_P_1D_sub.png width=4in
   In [15]: sys1.show_mode(0,what='phase') 

Comparison with the first method
================================

As we can see we the calculated modes looks like the calculated with one general ABCD system, however we can see some slight differences, for example, small ripples  on each side of the mode and on the phase of the beam. This is the effect of the aperture. These effects didn't not appeared with the previous methods. This is explained by the fact that the field is calculated once on the starting plane only (after one round-trip). Therefore, even if at a given location in the system the beam is magnified we don't need larger calculation area as long as the beam is re-focused before the last plane, consequently, the sampling rate and the size of the calculation zone are determined according to the requirements of the first and the last plane only. 
This is a major advantage of the ABCD matrix formalism. However, if for some reason we need to calculate the field at intermediate plane we have to take 
the size of the field at this plane into account. To get rid of the ripples in the example we can merely use a larger aperture size (a=200 for example)

.. ipython::
 
   In [10]: a=200; 
   
   In [10]: sys1.build_1D_cav_ABCD(a,npts,A11,B11,C11,D11)
   
   In [10]: sys2.build_1D_cav_ABCD(a,npts,A22,B22,C22,D22)
   
   In [10]: sys1.cascade_subsystem(sys2) 
   
   In [10]: sys1.solve_modes()
   
   @savefig tuto2_plot_mode0_E_1D_sub2.png width=4in
   In [15]: sys1.show_mode(0) # the fundamental mode E-field 
   
   @savefig tuto2_plot_mode2_I_1D_sub2.png width=4in
   In [15]: sys1.show_mode(2,what='intensity')  
   
   @savefig tuto2_plot_mode0_P_1D_sub2.png width=4in
   In [15]: sys1.show_mode(0,what='phase')
   
This is much better, note that what happens in the phase map outside the mode region does not matter since there is no E-field there. 

 