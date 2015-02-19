.. _tuto9-label:

***************************************
Tutorial 9 - Fresnel propagation module
***************************************
In some of the previous tutorials we used the Fresnel propagation module that comes with OpenCavity, mainly to calculate the output beam for 
1d and 2D cavity systems. And also with Bessel-Gauss cavities to show how the Bessel beams propagate especially in their non-diffracting region. 
In this tutorial  we use the Fresnel propagation module to do beam transforming using a phase function as it is usually realized practically 
using phase-plates and diffractive elements  or spatial light modulators (SLMs) to transform the phase structure of a given beam.
 
First we generate a fundamental Gaussian beam using Hermite-Gauss beams generator (HgBasis function) then we see how to transform it  to a 
donut-shaped one also known as vortex-beam using a phase mask. This beam  has a helical wavefront rather than parallel one as in fundamental 
gaussian beams as we have already seen. 
In the second part of the tutorial we design a Mach-Zehnder interferometer to see the phase singularity of the donut beam, and understand 
better why it is called a vortex. The objective of this tutorial is to become familiar with:

- Beam generator module
- Frenel propagator and use phase masks in addition to paraxial elements 
- Superimpose and move beams on  detectors surface to get interference result. 

First of all let's generate the Gaussian beam we are going to use through this tutorial, for this we use the function ``generate_gh(n,m,x,y,z)`` 
that returns  the E-field of Hermite-Gauss beam of order `n,m` at coordinates (x,y,z). We can use this function in a quite flexible way, for 
example to generate 1D beam profile by giving it an 1D array  along one spatial axis (x ,y or z) and 2 constants for the remaining ones . 
Or by giving it 2D mesh-grids to construct 2D intensity profile HG beams at a given `z`coordinate as in this tutorial.  

the function is located in  ``HgBasis`` class in``beams`` module, this class holds properties common to all the beams of the basis set.
As always we start by importing modules we need.


.. ipython::

   In [1]: from opencavity.beams import HgBasis
   
   In [1]: from opencavity.propagators import FresnelProp
    
   In [1]: import numpy as np
     
   In [1]: import matplotlib.pylab as plt
   
   In [1]: import math

Then we generate a fundamental Gaussian beam (n=m=0) at wavlength =1 and waist =100 (in wavelength unit say microns for example).

.. ipython::

   In [1]: waist=100; waist_x=waist; waist_y=waist; wavelength=1
   
   In [1]: H=HgBasis(wavelength,waist_x,waist_y) #creating the Hermite-Gauss basis with initial waist equals to 100 microns
    
   In [1]: z=0.000000000000000001 #(z=0, small value rather than '0' to prevent division by 0) 
     
   In [1]: import matplotlib.pylab as plt
   
   In [1]: H=HgBasis(1,waist_x,waist_y) #creating the Hermite-Gauss basis with initial waist equals to 100 microns
   
   In [1]: x=np.linspace(-6*waist, 6*waist,80); y=x # two 1D vectors
   
   In [1]: X,Y=np.meshgrid(x,y) # we use numerical python 'np' to generate a 2D meshgrid.
   
   In [1]: tem00=H.generate_hg(0, 0, X, Y, z) # generate TEM00 mode 
   
   @savefig tuto9_plot_HG00_E.png width=4.5in
   In [1]: plt.pcolor(x,y,np.abs(tem00)); plt.set_cmap('hot'); plt.colorbar(); # 2D plot/ colormap /colorbar
   
   @savefig tuto9_plot_HG00_P.png width=4.5in
   In [1]: plt.pcolor(x,y,np.angle(tem00)); # phase map
   
   In [1]:  plt.show()
   
   
Now we want to transform this beam to a donut-shaped one, for this we need a helical phase mask (phase-plate of SLM), this phase mask has the function 
:math:`phase(x,y)=atan(y/x)+\frac{1-sign(x)}{2}`. Obviously one have to manage the special case of `x=0` which gives three cases:

.. math::

     y<0 , \phi=\frac{3 2\pi}{4} \\
     y>0 , \phi=\frac{1 2\pi}{4} \\
     y=0 , \phi=2\pi

In third case (x=y=0) we have a singular point(the phase is not defined) but let's juste take 2 \pi), it is important to note that the mask phase we are making acts as a 
phase plate (add a certain amount to the beam phase) so just as we have seen with lenses its function takes the form :math:`exp(j\times phase(x,y))`. Indeed, in numerical
python ``np`` we can use ``arctan2(y,x)`` an element-wise arc tangent function that choose the quadrant correctly.

.. ipython::

   In [10]:n=x.size  # size of the array 'x'
   
   In [10]:phase=np.ones((n,n))+1j*np.ones((n,n))
   
   In [10]:m=2*np.pi

   In [10]: for kx in range(n):
      ....:    for ky in range (n):
      ....:       phase[kx,ky]=np.exp(1j*m*(np.arctan2(y[ky],x[kx]))/(2*np.pi))


In third case (x=y=0) we have a singular point(the phase is not defined) but let's juste take 2 \pi), it is important to note that the mask phase we are making acts as a phase plate (add a certain amount to the beam phase) so just alike we have seen with lenses its function takes the form :math: `exp(j\times phase(x,y))`.

We consider the beam we generated is a collimated one (plane wavefront) to transform it we just multiply it by the phase function and propagate it using ``FresnelProp`` following 
the steps we sown in previous tutorials:

- create the paraxial propagation matrix of the propagation system.
- create a propagator object
- set the initial beam and the propagation matrix in the propagator 
- do 1D/2D propagation using ``propagate1D_ABCD(x2)``/``propagate2D_ABCD(x2,y2)`` function.

Where (x2,y2) are vectors defining the propagation plane (result) that one can consider as the detector surface.   

Before starting to that let's take a look at the interferometer.

.. image::  _static/schema_interfero_donut.png
   :width: 6.5in
   :align: center
   
The goal here is to propgate to have to have two different optical paths and therefor two versions of the beam having different radius of 
curvature of the wavefront on the detector.  


.. ipython::

   In [10]: L1=50*1e3; L2=190e3; L3=120e3; L4=140e3;
   
   In [10]: f1=50*1e3; f2=60e3; #converging lens FL1=50mm, FL2=60mm
  
ABCD matrix of interferometer's first arm

.. ipython::

   In [10]: M1=np.array([[1, L1],[0, 1]]); 
   
   In [10]: M2=np.array([[1, 0],[-1/f1, 1]]);
   
   In [10]: M3=np.array([[1, L2],[0, 1]]);
   
   In [10]: M4=np.array([[1, 0],[-1/f2, 1]]);
   
   In [10]: M5=np.array([[1, L3],[0, 1]]);
   
   In [10]: M_arm1=M5.dot(M4).dot(M3).dot(M2).dot(M1) # calculating the global matrix
   
 
ABCD matrix of interferometer's second arm  

.. ipython::

   In [10]: M1=np.array([[1, L1],[0, 1]]); 
   
   In [10]: M6=np.array([[1, L2+L3+2*L4],[0, 1]]);

   In [10]: M_arm2=M6.dot(M2).dot(M1) 
   
Creating the first optical system (arm 1) and propagate the initial beam through it.

.. ipython::

   In [10]: opsys1=FresnelProp() # optical system 1 
    
   In [10]: opsys1.set_start_beam(tem00*phase, x) # note that the initial beam is multiplied by the phase function we created earlier.
   
   In [10]: opsys1.set_ABCD(M_arm1); x2=1*x; y2=1*y; # set the propagation matrix 
   
   In [10]: opsys1.propagate2D_ABCD(1*x) # propagation
   
    @savefig tuto9_plot_arm1_I.png width=4.5in
   In [10]: opsys1.show_result_beam('intensity'); plt.show()

   @savefig tuto9_plot_arm1_P.png width=4.5in
   In [10]: opsys1.show_result_beam('phase'); plt.show()

Creating the first optical system (arm 2) and propagate the initial beam through it.

.. ipython::

   In [10]: opsys2=FresnelProp() # optical system 1 
    
   In [10]: opsys2.set_start_beam(tem00*phase, x) # note that the initial beam is multiplied by the phase function we created earlier.
   
   In [10]: opsys2.set_ABCD(M_arm2); x2=1*x; y2=1*y; # set the propagation matrix 
   
   In [10]: opsys2.propagate2D_ABCD(x2-500,y2-600) # propagation with small decenter (500 and 600 microns)
   
   @savefig tuto9_plot_arm2_I.png width=4.5in
   In [10]: opsys2.show_result_beam('intensity'); plt.show()
   
   @savefig tuto9_plot_arm2_P.png width=4.5in
   In [10]: opsys2.show_result_beam('phase'); plt.show()
   
The optical system is an object holding all informations needed for  the propagation, for example 

     - ``opsys.U1``,``opsys.x1``,``opsys.y1`` are the initial beam E-field and coordinates of its plane. 
     - ``opsys.U2``,``opsys.x2``,``opsys.y2`` are the result beam E-field and coordinates of its plane.
   
You can see the class documentation for more informations, for the time being let's stay with these two members (U1, U2). when the 
function ``opsys.show_result_beam()`` it merely plots the amlitude of ``opsys.U2``. Now we want to see the interference of the two  
beams (arm 1 and arm 2), to do this we have to sum the propagation result of ``opsys1.U2`` and ``opsys2.U2`` 

.. ipython::

   In [10]: inter=0.4*opsys1.U2+opsys2.U2
   
   In [10]: plt.figure()
   
   @savefig tuto9_plot_interference_I.png width=4.5in
   In [10]: plt.pcolor(X,Y,np.abs(inter)**2) # plots the intesnty of the interference. 
   
   In [10]: plt.show()
   
The cleaned code
================

.. literalinclude::  tuto_source/tuto9_beam_transformation.py
    