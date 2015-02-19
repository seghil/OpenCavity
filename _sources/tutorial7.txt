.. _tuto7-label:

*************************************
Tutorial 7 - General 2D cavity design
*************************************

In the previous tutorials we have seen how to define and calculate the modes of a given 1D optical cavity using ABCD transfer matrix definition. Now we 
see how to do the same thing but to design and calculate the modes of 2D optical cavity. The system definition procedure is quite similar as shown below.

.. ipython::


   In [1]: import opencavity.modesolver as oc; #importing the opencavity module
   
   In [2]: import matplotlib.pylab as plt
   
   In [2]: R1=1e13; R2=10*1e3; Lc=8*1e3; npts=64; a=100; # cavity parameters

   In [7]: M1=ms.np.array([[1,0 ],[-2/R1, 1]]);   #concave mirror M1 
   
   In [8]: M2=ms.np.array([[1, Lc],[0, 1]]);  #propagation distance Lc
   
   In [9]: M3=ms.np.array([[1, 0],[-2/R2, 1]]); #concave mirror M2
   
   In [4]: M4=ms.np.array([[1, Lc],[0, 1]]); #propagation distance Lc
   
   In [10]: M=M4.dot(M3).dot(M2).dot(M1) # calculating the global matrix (note the inversed order)
 
   In [11]: A=M[0,0]; B=M[0,1]; C=M[1,0]; D=M[1,1]
   
   In [12]: opsys=ms.CavEigenSys() #creating a oc object
   
so far we are doing exactly the same thing as in previous tutorials, the change comes next: instead of using ``opsys.build_1D_cav_ABCD(a,npts,A,B,C,D)`` 
we use ``opsys.build_2D_cav_ABCD(a,npts,A,B,C,D)``

.. ipython::


   In [1]: opsys=ms.CavEigenSys() #creating a oc object
   
   In [1]: opsys.build_2D_cav_ABCD(a, npts, A,B,C,D)
   
   In [1]: opsys.solve_modes()  
   
   
Now to see the first 4 modes Amplitude or intensity and phase profiles:
   
   
-  Fundamental mode (TEM00) amplitude and phase profile:
.. ipython::

   In [1]: plt.set_cmap('hot')
   
   @savefig tuto7_plot_tem00_E_2D.png width=3.5in
   In [1]: opsys.show_mode(0)
   
   @savefig tuto7_plot_tem00_P_2D.png width=3.5in
   In [1]: opsys.show_mode(0,what='phase')
   
-  TEM01 mode:

.. ipython::
   
   @savefig tuto7_plot_tem01_I_2D.png width=3.5in
   In [1]: opsys.show_mode(1,what='intensity')
   
   @savefig tuto7_plot_tem01_P_2D.png width=3.5in
   In [1]: opsys.show_mode(1,what='phase')

-  TEM10 mode:

.. ipython::  
 
   @savefig tuto7_plot_tem02_I_2D.png width=3.5in
   In [1]: opsys.show_mode(2,what='intensity')
   
   @savefig tuto7_plot_tem02_P_2D.png width=3.5in
   In [1]: opsys.show_mode(2,what='phase')

-  And finally TEM11 mode:

.. ipython::   

   @savefig tuto7_plot_tem03_I_2D.png width=3.5in
   In [1]: opsys.show_mode(3,what='intensity')
   
   @savefig tuto7_plot_tem03_P_2D.png width=3.5in
   In [1]: opsys.show_mode(3,what='phase')
   
To get the the round trip losses (1-abs(eigenvalue)^2):

.. ipython::   

   In [1]: l,v=opsys.get_mode2D(0);# l: eigenvalue, v: eigenvector (the mode)

   In [1]: (1-ms.np.abs(l)**2)*100 # in percent
   
   In [1]: l,v=opsys.get_mode2D(2);

   In [1]: (1-ms.np.abs(l)**2)*100 
     
Using 2D cavity design offers more flexibility to simulate some effects, for example aberrations in laser mirrors, tilt, astigmatism...etc. It also allows 
to design cavities with advanced phase/ amplitude masks. However you should be aware that the calculation method is memory-intensive because to build 
the cavity kernel matrix each point in the final plane of the system need to do a double integration over all the starting plane, As explained earlier this 
integration is transformed to a matrix product, thus in this tutorial for example we used 64 points which means that the starting plane contains 64x64 
points, and the last plane 64x64, and for each point of the first we need to create a matrix of 64x64 we end up with a matrix-kernel of 64^4 = 16777216 
complex elements, which needs 32 byte each, so the matrix kernel needs 537 Mb, and using a grid of 90x90 need 2.1 Gb of memory so if you want to design 
a 2D system with very high resolution check that your available memory resources allow that. This said, a computer with 2Gb memory for example allows to accurately 
simulate most of cavities design as we will see in the next tutorials.  


The cleaned code
================

.. literalinclude::  tuto_source/tuto_7_2D_ABCD.py



Calculating the output mode
===========================

In a similar way to tutorial 4 in this part we propagate the fundamental mode taking the output mirror into account to get the mode shape outside the 
cavity. Let's the same system as in tutorial 4 

.. image:: _static/Optical_cavity_output.png

As written earlier the ABCD matrix of this optical system is given by:

.. math::
      \begin{bmatrix} A & B \\ C & D \end{bmatrix}=
      \begin{bmatrix} 1 & d2 \\ 0 & 1 \end{bmatrix} 
      \times \begin{bmatrix} 1 & 1 \\ 0 & n1/n0 \end{bmatrix}
      \times \begin{bmatrix} 1 & d1 \\ 0 & 1 \end{bmatrix}
      \times \begin{bmatrix} 1 & 0 \\ \frac{(n0-n1)}{R2*n1} & n0/n1 \end{bmatrix}
      \times \begin{bmatrix} 1 & Lc \\ 0 & 1 \end{bmatrix}

  
Entering these matrices and calculate the global one:  

.. ipython::

   In [1]: M00=ms.np.array([[1,Lc ],[0, 1]]);
   
   In [1]: M01=ms.np.array([[1,0 ],[(1-1.5)/(-R2*1.5), 1/1.5]]);# -R2  (<0 because it is a concave interface)
   
   In [1]: M02=ms.np.array([[1,5e3 ],[0, 1]]);
   
   In [1]: M03=ms.np.array([[1,1 ],[0, 1.5/1]]);
   
   In [1]: M04=ms.np.array([[1,50e3 ],[0, 1]]);
   
   In [1]: M_out=M04.dot(M03.dot(M02.dot(M01.dot(M00))));
   


The difference from tutorial 4 is using ``propagate2D_ABCD()`` instead of ``propagate1D_ABCD()`` to propagate the beam.

.. ipython::

   In [1]: from opencavity.propagators import FresnelProp 
   
   In [1]: propsys=FresnelProp() #create propagator object 
   
   In [1]: l,tem00=opsys.get_mode2D(0) # get the fundamental mode of the cavity 
   
   In [1]: propsys.set_start_beam(tem00, opsys.x1) # set the beam to propagate
   
   In [1]: propsys.set_ABCD(M_out) # taking M2 into account
   
   In [1]: propsys.propagate2D_ABCD(x2=10*opsys.x1) # calculate the propagation from initial plane to a plane 10 times larger (the beam is wider) 
    
   @savefig tuto7_plot_propagate_tem00_2D_I.png width=4in
   In [1]: propsys.show_result_beam(what='intensity') # show propagation result
   
   @savefig tuto7_plot_propagate_tem00_2D_P.png width=4in
   In [1]: propsys.show_result_beam(what='phase') 