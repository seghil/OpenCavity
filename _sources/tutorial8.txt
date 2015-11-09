.. _tuto8-label:

*********************************
Tutorial 8 - 2D cavity with masks
*********************************

In this tutorial we learn how to use **OpenCavity** to design 2D cavities with masks as we did for 1D case in :ref:`tuto3-label`. The 
procedure is quite similar, and as 2D masks can be more complicated to generate than 1D ones **OpenCavity** comes with mask generation 
class called `AmpMask2D()` that can be used to create a mask object and modify it, then we can apply this mask object to a given cavity system using the function 
`apply_mask2D()` as we will see. Of course you can just create a mask object using a given phase or amplitude function as we did in 1D case than apply it to the 
system the AmpMask2D() class is here just to simplify the creation of some usual amplitude masks as an aperture for example.  

Lets start by creating the cavity system:

.. ipython::

   In [1]: import opencavity.modesolver as ms; #importing the opencavity module
   
   In [1]: import matplotlib.pylab as plt
   
   In [1]: import numpy as np
   
   In [1]: sys=ms.CavEigenSys() #creating a ms object
   
   In [1]: R1=1e13; R2=10*1e3; Lc=8*1e3; npts=64; a=80; # cavity parameters 
   
   In [1]: g1=1-Lc/R1; g2=1-Lc/R2; # g1 and g2 parameters of the cavity 
   
   In [1]: A1=2*g1*g2-1; B1=2*g2*Lc; C1=2*g1/Lc; D1=2*g1*g2-1; # ABCD elements written using g1,g2 
   
   In [1]: sys.build_2D_cav_ABCD(a, npts, A1,B1,C1,D1) # building the cavity 
   
We use now ``AmpMask2D()`` class to create and show the mask, but before this we need to get the discretized grid of the cavity system in which we build 
the mask, keep in mind that in **OpenCavity** all spatial entities are not linearly spaced, see :ref: `vector-spacing-label` for more details.

.. ipython::

   In [1]: x1=sys.x1; y1=sys.y1
   
   In [1]: apert=ms.AmpMask2D(x1,y1) # create a mask object  
   
   In [1]: apert.add_circle(80) #create an aperture in x1,y1 coordinates with radius=80
   
   @savefig tuto8_plot_mask1_3D.png width=4.5in
   In [1]: apert.show_msk3D() # plot the mask function to check the created distribution
  
  
Now we know what the mask looks like, let's apply it to the cavity system and calculate the modes.
  
.. ipython::
   
   In [1]: sys.apply_mask2D(apert) # apply the mask to the system (1st plane) 
   
   In [1]: sys.solve_modes() 
   
   #show some modes 
   
   In [1]: plt.set_cmap('hot')
   
   @savefig tuto8_plot_tem00_I_2D.png width=3.5in
   In [1]: sys.show_mode(0,what='intensity') 
   
   @savefig tuto8_plot_tem01_I_2D.png width=3.5in
   In [1]: sys.show_mode(1,what='intensity') 
   
   @savefig tuto8_plot_tem10_I_2D.png width=3.5in
   In [1]: sys.show_mode(2,what='intensity') 
   
   @savefig tuto8_plot_tem11_I_2D.png width=3.5in
   In [1]: sys.show_mode(3,what='intensity')
   
   
Lets add some modifications to the amplitude mask and see what impact it has on the eigenmodes

.. ipython::

   In [1]: x1=sys.x1; y1=sys.y1
   
   In [1]: apert.add_rectangle(2, 50,positive='False') # a lossy rectangle (amplitude =0)

   In [1]: apert.add_rectangle(50, 2,positive='False')

   @savefig tuto8_plot_mask2_3D.png width=4.5in
   In [1]: apert.show_msk3D()

This mask is supposed to introduce losses in the dark region of the mode TEM11, so this latter will be the less affected by this mask 
thus we expect it to become the first mode (having the biggest eigenvalue) of this cavity, let's check this.

.. ipython::

   In [1]: sys.apply_mask2D(apert)
   
   In [1]: sys.solve_modes() 

   @savefig tuto8_plot2_tem00_I_2D.png width=3.5in
   In [1]: sys.show_mode(0,what='intensity') 
   
   @savefig tuto8_plot2_tem01_I_2D.png width=3.5in
   In [1]: sys.show_mode(1,what='intensity') 
   
   @savefig tuto8_plot2_tem10_I_2D.png width=3.5in
   In [1]: sys.show_mode(2,what='intensity') 
   

The three first modes of this cavity have zero intensity region that falls in the lossy region of the mask as we expected. let's take 
a look at the eigenvalue:   


.. ipython::

   In [1]: l,tem00=sys.get_mode2D(0);  
   
   In [1]: print 1-np.abs(l)**2 #round trip losses
   
   
The cleaned code
================

.. literalinclude::  tuto_source/tuto_8_2D_mask.py
 


   
   
