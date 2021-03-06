# Quick illustration.
# Sorry for the mess.

from dapper import *
plt.ion()

from dapper.mods.LorenzUV.lorenz95 import LUV
nU, J = LUV.nU, LUV.J

dt = 0.005
K  = int(4/dt)

step_1 = with_rk4(LUV.dxdt,autonom=True)
step_K = with_recursion(step_1,prog='Simulating')

xx = step_K(LUV.x0,K,np.nan,dt)

# Grab parts of state vector
ii, wrapU = setup_wrapping(nU)
jj, wrapV = setup_wrapping(nU*J)

# Animate linear
plt.figure(1)
lhU = plt.plot(ii  ,wrapU(xx[-1,:nU]),'b',lw=3)[0]
lhV = plt.plot(jj/J,wrapV(xx[-1,nU:]),'g',lw=2)[0]
for k in progbar(range(K),'Plotting'):
  lhU.set_ydata(wrapU(xx[k,:nU]))
  lhV.set_ydata(wrapV(xx[k,nU:]))
  plot_pause(0.001)








