import ucilib.Sim as Sim
import ucilib.TrapConfiguration as TrapConfig
import numpy as np


t = TrapConfig.TrapConfiguration()
t.Bz = 4.5
#V0 in V/m^2
t.kz = 2.0 * 1.167e6
delta = 0.010
t.kx = -(0.5 + delta) * t.kz
t.ky = -(0.5 - delta) * t.kz
t.theta = 0
t.omega = 2.0 * np.pi * 43.0e3

fundcharge = 1.602176565e-19
ionMass = 8.9465 * 1.673e-27

s = Sim.Sim()
s.ptcls.set_nptcls(400)
s.ptcls.rmax = 2.0e-4
s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
axialFrictionCoeff = 1.0e7
angularFrictionCoeff = 1.0e7
s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff)
s.spin_up()
s.take_steps(1.0e-8, 100000)
np.savetxt('convergenceStudy/initialState_1ms_400ptcls.txt', s.ptcls.ptclList)
s.take_steps(1.0e-9, 100000)
np.savetxt('convergenceStudy/initialState_1_1ms_400ptcls.txt', s.ptcls.ptclList)


