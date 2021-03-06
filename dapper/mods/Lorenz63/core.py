"""The "Lorenz-63" model: the classic exhibitor of chaos.
Phase-plot looks like a butterfly.
See demo.py for more info.
"""


import numpy as np
from dapper.tools.math import with_rk4, is1d, ens_compatible, integrate_TLM

# Constants
sig = 10.0; rho = 28.0; beta = 8.0/3

@ens_compatible
def dxdt(x):
  "Evolution equation (coupled ODEs) specifying the dynamics."
  d     = np.zeros_like(x)
  x,y,z = x
  d[0]  = sig*(y - x)
  d[1]  = rho*x - y - x*z
  d[2]  = x*y - beta*z
  return d

# Time-step integration.
step = with_rk4(dxdt,autonom=True)

# Time span for plotting. Typically: ≈10 * "system time scale".
Tplot = 4.0

# Example initial state -- usually not important,
# coz system is chaotic, and we average stats after a BurnIn time.
# But it's often convenient to have a point on the attractor, or basin,
# or at least ensure "physicality".
x0 = np.array([1.509, -1.531, 25.46])


################################################
# OPTIONAL (not necessary for EnKF or PartFilt):
################################################
def d2x_dtdx(x):
  """Tangent linear model (TLM): Jacobian of dxdt(x)."""
  x,y,z = x
  A = np.array(
      [[-sig , sig , 0],
      [rho-z , -1  , -x],
      [y     , x   , -beta]])
  return A

def dstep_dx(x,t,dt):
  """Resolvent (propagator) of the TLM: Jacobian of step(x)."""
  return integrate_TLM(d2x_dtdx(x),dt,method='approx')


################################################
# Add some non-default liveplotters
################################################
import dapper.tools.liveplotting as LP
params = dict(labels='xyz', Tplot=1)
def LPs(jj=None,params=params): return [
    (12, 1, LP.correlations   ),
    (14, 1, LP.sliding_marginals(jj, zoomy=0.8, **params)) ,
    (13, 1, LP.phase3d(jj, **params)                     ) ,
    ]
