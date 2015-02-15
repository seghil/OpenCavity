'''
Created on 8 juil. 2014

@author: Mike
'''

from beams import*
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

plt.close("all")

H=HGBeam(1,30,30)

z=0.01
x=np.linspace(-100, 100, 200)
y=x
X,Y=np.meshgrid(x,y)
tem00=H.generate_hg(0, 1, X, Y, z)+H.generate_hg(1, 0, X, Y, z)*np.exp(-1j*math.pi/2*0.75)
#tem02=H.generate_hg(0, 2, X, Y, z)
#tem20=H.generate_hg(2, 0, X, Y, z)
#tem11=H.generate_hg(1, 1, X, Y, z)

#tem00=-0.5*tem02+1j/np.sqrt(2)*tem11+0.5*tem20
#tem00=1/np.sqrt(2)*tem02+1/np.sqrt(2)*tem20



plt.set_cmap('hot')
plt.imshow(np.abs(tem00)**2,extent=[-100,100,-100,100])
plt.show()
plt.Figure
plt.imshow(np.angle(tem00),extent=[-100,100,-100,100])
plt.colorbar()

plt.show()

