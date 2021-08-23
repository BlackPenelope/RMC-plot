import os
import math
from core.rmc_configuration import RmcConfiguration
from utils.rmc_data import RmcData
from utils.calc_histogram import *
import numpy as np
import six

try:
    import histogram.histogram as hist
    has_hist = True
except ImportError:
    has_hist = False

def calc_gr(cfg, dr, coeff):

    ntypes = cfg.nmol_types
    npar = int(ntypes*(ntypes+1)/2)
    nxn = np.zeros(npar)

    ic = 0
    for itype in range(ntypes):
        for jtype in range(itype, ntypes):
            nxn[ic] = cfg.ni[itype]*cfg.ni[jtype]
            if(itype != jtype):
                nxn[ic] = nxn[ic]*2
            ic = ic+1

    d = cfg.d
    volume = cfg.volume
    nr = int(d/dr)+1
    r =[(float(i)*dr) for i in range(nr) ]

    if has_hist == True:
        atoms = []
        for pos in cfg.atoms.positions:
            atoms.append(list(pos))
        metric = []
        for m in cfg.metric:
            metric.append(list(m))

        histogram = hist.calc_histogram(atoms, metric, cfg.ni, cfg.d, dr, cfg.truncated)
    else:
        histogram = calc_histogram(cfg, dr)

    gr = np.zeros_like(histogram, dtype=float)
    gr_tot = np.zeros(nr)

    for ir in range(1, nr):   
        gnorm = (3.0*ir*ir+0.25)*dr*dr*dr*2.0*math.pi/(3.0*volume)
        for ic in range(npar):
            if has_hist== True:
                gr[ir,ic] = histogram[ir][ic]/(gnorm*nxn[ic])
            else:
                gr[ir,ic] = histogram[ir,ic]/(gnorm*nxn[ic])

    for ir in range(nr):
        for ic in range(npar):
            gr_tot[ir] = gr_tot[ir] + coeff[ic]*(gr[ir,ic]-1.0) 

    return r, gr, gr_tot

def calc_sq(cfg, qmin, dq, qmax, gr, dr, coeff):
    """
    calculate S(Q)
    """
    nq = int(math.ceil((qmax-qmin)/dq))+1
    q =[ (qmin+float(i)*dq) for i in range(nq) ]
    nr = gr.shape[0]
    sqr = np.zeros((nr, nq+1), dtype=float)
    #s = np.zeros_like(sqr)

    ntypes = cfg.nmol_types
    npar = int(ntypes*(ntypes+1)/2)
    sq = np.zeros((nq, npar), dtype=float)
    sq_tot = np.zeros(nq)

    n = cfg.nmol
    volume = cfg.volume
    
    for iq in range(nq):
        s = np.zeros(npar)
        for ir in range(1, nr):
            r = float(ir)*dr
            sqr = 4.0*math.pi*float(n)/volume*r*math.sin(r*q[iq])/q[iq]*dr
                
            for ic in range(npar):
                s[ic] = s[ic] + (gr[ir, ic]-1.0)*sqr
            
        sq[iq] = s

    for iq in range(nq):
        for ic in range(npar):
            sq_tot[iq] = sq_tot[iq] + coeff[ic]*sq[iq,ic]

    return q, sq, sq_tot
                
if __name__ == '__main__':

    if six.PY2 == True:
        #dr = raw_input(' r spacing              > ')        
        #qmin = raw_input(' Q min                  > ')
        #dq = raw_input(' Q spacing              > ')
        #qmax = raw_input(' Q max                  > ')
        #in_file = raw_input(' Input file             > ')
        #out_file = raw_input(' Output file            > ')

        dr = 0.05
        qmin = 0.05
        dq = 0.05
        qmax = 15.0
        in_file = './data/sio.cfg'
        out_file = './sio.out'

    elif six.PY3 == True:
        dr = input(' r spacing              > ')        
        qmin = input(' Q min                  > ')
        dq = input(' Q spacing              > ')
        qmax = input(' Q max                  > ')
        in_file = input(' Input file             > ')
        out_file = input(' Output file            > ')

    dr = float(dr)
    qmin = float(qmin)
    dq = float(dq)
    qmax = float(qmax) 
    
    #cfg = RmcConfiguration("./data/sio.cfg")
    cfg = RmcConfiguration(in_file)
    cfg.read()

    ntypes = cfg.nmol_types
    npar = int(ntypes*(ntypes+1)/2)
    coeff = np.zeros(npar)

    n = 0
    for i in range(ntypes):
        for j in range(i, ntypes):
            coeff[n] = raw_input(' Coefficients(%d-%d)      > ' % (i+1, j+1))
            n = n+1

    #dr = 0.05
    #qmin = 0.05
    #qmax = 15.0
    #dq = 0.05

    #root, ext = os.path.splitext(in_file)
    #dat_file = root + '.dat'

    r, gr, gr_tot = calc_gr(cfg, dr, coeff)

    #dat = RmcData(dat_file, cfg, )
    #dat.read()
    
    q, sq, sq_tot = calc_sq(qmin, dq, qmax, gr, dr, coeff)

    fw = open(out_file, 'w')

    fw.write(' Partial g(r)\'s\n')
    fw.write('  r, g(r)\n')
    fw.write(' PLOTS\n')
    fw.write('%12d,%12d\n' % (len(r), npar))
    for i in range(gr.shape[0]):
        fw.write("%16.6f" % r[i])
        for j in range(npar):
            fw.write("%16.6F" % gr[i][j])
        fw.write("\n")
    fw.write(' ENDGROUP\n')

    fw.write(' Partial S(Q)\'s\n')
    fw.write('  Q, S(Q)\n')
    fw.write(' PLOTS\n')
    fw.write('%12d,%12d\n' % (len(q), npar))
    for i in range(len(q)):
        fw.write("%16.6f" % q[i])
        for j in range(npar):
            fw.write("%16.6F" % sq[i][j])
        fw.write("\n")
    fw.write(' ENDGROUP\n')

    fw.write(' Total g(r)\'s\n')
    fw.write(' r, g(r) (RMC), g(r) (Expt)\n')
    fw.write(' CURVES\n')
    fw.write('%12d,%12d\n' % (len(r), 1))
    for i in range(len(r)):
        fw.write("%16.6f" % r[i])
        fw.write("%16.6F" % gr_tot[i])
        fw.write("\n")
    fw.write(' ENDGROUP\n')

