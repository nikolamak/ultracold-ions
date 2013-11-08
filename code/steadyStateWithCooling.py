import ucilib.Sim as Sim
import ucilib.TrapConfiguration as TrapConfig
import numpy as np
import ucilib.CoolingLaserAdvance as coolingLsr

from time import time


def createCrystal():
    t = TrapConfig.TrapConfiguration()
    t.Bz = 4.4584
    #V0 in V/m^2
    t.kz = 2.0 * 1.167e6
    delta = 0.010
    t.kx = -(0.5 + delta) * t.kz
    t.ky = -(0.5 - delta) * t.kz
    t.theta = 0
    t.omega = 2.0 * np.pi * 44.0e3
    fundcharge = 1.602176565e-19
    ionMass = 8.9465 * 1.673e-27
    s = Sim.Sim()
    s.ptcls.set_nptcls(127)
    s.ptcls.rmax = 1.0e-5
    s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
    axialFrictionCoeff = 1.0e7
    angularFrictionCoeff = 1.0e7
    s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff,
        recoilVelocity = 0.01, scatterRate = 1.0e6)
    s.take_steps(1.0e-8,200000)
    s.take_steps(1.0e-9,50000)
    return s

def loadCrystal(filename):
    t = TrapConfig.TrapConfiguration()
    t.Bz = 4.4584
    #V0 in V/m^2
    t.kz = 2.0 * 1.167e6
    delta = 0.01
    t.kx = -(0.5 + delta) * t.kz
    t.ky = -(0.5 - delta) * t.kz
    t.theta = 0
    t.omega = 2.0 * np.pi * 44.0e3
    fundcharge = 1.602176565e-19
    ionMass = 8.9465 * 1.673e-27
    s = Sim.Sim()
    s.ptcls.set_nptcls(127)
    s.ptcls.rmax = 1.0e-4
    s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
    axialFrictionCoeff = None
    angularFrictionCoeff = None
    s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff,
        recoilVelocity = 0.01, scatterRate = 1.0e6)
    s.ptcls.ptclList = np.loadtxt(filename, dtype=np.float32)
    s.t=0.0
    return s


#s = createCrystal()
#np.savetxt("crystal127.dat", s.ptcls.ptclList)

s = loadCrystal('newcrystal127.dat')

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])
phaseInitial = 0.331 * np.pi
s.ptcls.ptclList[:2] = rotate(s.ptcls.ptclList[:2], phaseInitial)
s.ptcls.ptclList[3:5] = rotate(s.ptcls.ptclList[3:5], phaseInitial)

s.accList = s.accList[0:2]
claAlongZ = coolingLsr.CoolingLaserAdvance(s.ctx, s.queue)
claAlongZ.sigma = None
claAlongZ.k0 = np.array([0, 0, -2.0 * np.pi / 313.0e-9], dtype = np.float32)
s.accList.append(claAlongZ)

nSteps = 100
dt = 1.0e-8
t0 = time()
for i in range(nSteps):
    ti = time()
    print "i: ", i, "wall time: ", ti - t0, "sim. time: ", s.t
    np.savetxt("runs/run6_" + str(i) + ".dat", s.ptcls.ptclList)
    s.take_steps(dt, 1000)



# vi: sw=4 ts=4

