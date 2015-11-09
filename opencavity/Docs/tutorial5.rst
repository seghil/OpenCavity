
.. _label-tuto5:

*************************************************************
Tutorial 5 - An advanced cavity example 'Bessel-Gauss' cavity
*************************************************************

Small introduction
==================

In this tutorial we will design and calculate the eigenmodes of an advanced type of laser cavities called Bessel-Gauss cavities. This class of cavities 
support Bessel-Gauss beams which offer some interesting properties, for example an extended depth of field with high intensity sometimes called 
*non-diffracting region* and annular intensity distribution in the far field. These properties make this class of beams very interesting for several 
applications such as biomedical imaging, particle trapping, strong-field applications...etc. Well, I hope that this small introduction motivates you to 
learn more about these cavities. In the tutorial we will take the design studied in this open access paper [Schimpf2012]_ which is a good one (I find) 
to learn more about Bessel-Gauss beams and cavities and can be downloaded `here <http://dx.doi.org/10.1364/OE.20.026852>`_ ), this way we can compare 
the results obtained using **OpenCavity** with those of the paper. Lets start with the scheme of the cavity: 

.. _Bessel-cavity-fig:

.. image:: _static/Bessel_cavity_scheme.png
   :width: 5in
   :align: center

As we can see this cavity contains concave mirror with radius of curvature R2=250mm and a conical reflector with base angle :math:`\alpha=0.5°`. the cavity 
length Lc=78mm. This results in a ring-shaped mode with radius of 1.5mm at the first mirror. For more details about how to calculate the stability of 
such a cavity take a look at the paper. To define this cavity we use general definition using ABCD transfer matrix and a phase mask to introduce the 
conical phase function, using subsystems cascading as shown in :ref:`tuto3-label` as follows:

Cavity design using OpenCavity
==============================

Entering the cavity parameters and transfer matrices of the subsystems

.. ipython::

   In [1]: import opencavity.modesolver as ms
   
   In [1]: from opencavity.propagators import FresnelProp
   
   In [1]: import numpy as np #import numerical Python
   
   In [1]: import matplotlib.pylab as plt # import matplotlib to plot figures 
    
   
   
   In [1]: R1=1e18; R2=250*1e3; Lc=78*1e3; npts=1000; a=2700; # cavity parameters
   
   In [1]: M1=np.array([[1,0 ],[-2/R1, 1]]);   #plane mirror M1 
   
   In [1]: M2=np.array([[1, Lc],[0, 1]]);  #propagation distance Lc
   
   In [1]: M3=np.array([[1, 0],[-2/R2, 1]]); #concave mirror M2
   
   In [1]: M4=np.array([[1, Lc],[0, 1]]); #propagation distance Lc
   
   In [1]: M11=M2.dot(M1); M22=M4.dot(M3); # sub-system 1 & sub-system 2 
   
   In [1]: A11=M11[0,0]; B11=M11[0,1]; C11=M11[1,0]; D11=M11[1,1] # getting the members of subsystem 1 matrix
   
   In [1]: A22=M22[0,0]; B22=M22[0,1]; C22=M22[1,0]; D22=M22[1,1] # getting the members of subsystem 2 matrix
   
Creating the cavity-subsystems

.. ipython::

   In [1]: sys1=ms.CavEigenSys(wavelength=1.04); # working wavelength 1.04 micron
    
   In [1]: sys2=ms.CavEigenSys(wavelength=1.04);
   
   In [1]: sys1.build_1D_cav_ABCD(a,npts,A11,B11,C11,D11) #
   
   In [1]: sys2.build_1D_cav_ABCD(a,npts,A22,B22,C22,D22) # to reinitialize the sub-system 
   
   
Creating the axicon function with base angle =-0.5°, ``sys.k`` is the wave vector, and remember that all the fields are not spaced linearly see (:ref:`vector-spacing-label`)

.. ipython::
   
   In [1]: theta=-0.5*3.14/180;# reflector is equivalent to refractive axicon with 2 x theta
   
   In [1]: T_axicon=ms.np.exp((1j*sys1.k)*2*theta*(ms.np.sign(sys1.x1))*sys1.x1)

Applying the axicon function and solve and show the modes 

.. ipython::
   
   In [1]: sys1.apply_mask1D(T_axicon)
   
   In [1]: sys1.cascade_subsystem(sys2)

   In [1]: sys1.solve_modes()
   
   @savefig tuto5_plot_tem00_I_1D.png width=4in
   In [1]: sys1.show_mode(0,what='intensity')
   
   @savefig tuto5_plot_tem00_P_1D.png width=4in
   In [1]: sys1.show_mode(0,what='phase') 
  
   In [1]: l,tem00=sys1.get_mode1D(0) 
   
   In [1]: print 1-np.abs(l)**2 #round trip losses
   
The first thing we can notice is that the mode contains two lobes, this is because it has a ring-shaped intensity distribution. And the second thing is the conical component in the 
phase. The obtained mode is identical to the result of paper *(Fig 6-a)* and the lobe spacing is the one we expected :1.5mm (1500 micron in the figure). 
Lets see the high order modes to complete the results of the *(Fig 6)*.
  
.. ipython::
   
   @savefig tuto5_plot_tem02_I_1D.png width=4in
   In [1]: sys1.show_mode(2,what='intensity')
   
   @savefig tuto5_plot_tem04_P_1D.png width=4in
   In [1]: sys1.show_mode(4,what='intensity') 

To see the high intensity region of these beams we use the `FresnelProp()` module presented in :ref:`tuto4-label`, but this time we use a new function 
`propsys.yz_prop_chart(z_min,z_max,n_step,x)` that calculates the propagated beam in ``n_step`` successive planes from ``z_min`` to ``z_max`` and ``x`` is the planes 
abscissa.  
However in this cavity arrangement the mode has already ring-shape at the first plane and is diverging, thus the high intensity region is behind the beam 
so to see it we enter negative propagation distance (to follow the paper), obviously this does not have physical meaning in real word but mathematically it means that we merely 
invert the time axis, or to consider a beam propagating from the right to the left. 

.. ipython::

   In [1]: propsys=FresnelProp() # create a propagator object 
   
   In [1]: propsys.set_start_beam(tem00, sys1.x1) 

   In [1]: d=-172.0e3
   
   In [1]: M=ms.np.array([[1,d ],[0, 1]]);
   
   In [1]: propsys.set_ABCD(M) 

   In [1]: propsys.yz_prop_chart(-250e3,-100e3,100,sys1.x1/2) # z_min=-250, z_max=-100, n_planes=100
   
   In [1]: plt.set_cmap('hot')
   
   @savefig tuto5_plot_tem01_yz_1D.png width=4in
   In [1]: propsys.show_prop_yz()
   
   # propagate the second mode
   In [1]: l,tem02=sys1.get_mode1D(2)
   
   In [1]: propsys.set_start_beam(tem02, sys1.x1) 
   
   In [1]: propsys.yz_prop_chart(-250e3,-100e3,100,sys1.x1/2)
   
   @savefig tuto5_plot_tem02_yz_1D.png width=4in
   In [1]: propsys.show_prop_yz()
   
   # propagate the third mode
   In [1]: l,tem03=sys1.get_mode1D(4)
   
   In [1]: propsys.set_start_beam(tem03, sys1.x1) 
   
   In [1]: propsys.yz_prop_chart(-250e3,-100e3,100,sys1.x1/2)
   
    @savefig tuto5_plot_tem03_yz_1D.png width=4in
   In [1]: propsys.show_prop_yz()
  
NB: As we are using Fresnel propagation method we can not calculate the propagation over small distances because this will break the paraxial condition 
(small angles from the propagation axis) see (to add in the first part 'before starting'). What we observe is that the high intensity region is behind 
the conical mirror, after that the beam takes an annular shape and diverges as it propagates. 
In the next tutorial we will change the cavity design to have the high intensity region after the concave mirror.

The cleaned code
================

.. literalinclude::  tuto_source/tuto_5_bessel_gauss.py



 
.. rubric:: Bibliography

.. [Schimpf2012] Schimpf, D. N., Schulte, J., Putnam, W. P., & Franz, X. K. (2012). Generalizing higher-order Bessel-Gauss beams: analytical description and demonstration. Optics Express, 18(24), 24429–24443.
