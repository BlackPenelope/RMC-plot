# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 16:50:06 2021

@author: Morita-T1700
"""

from core.rmc_configuration import RmcConfiguration
import numpy as np
import utils.grsq

cfg = RmcConfiguration()
cfg.read('sio.cfg')

dr = 0.05
ntypes = cfg.nmol_types
npar = int(ntypes*(ntypes+1)/2)
coeff = np.zeros(npar)

atom_types = ['Si', 'O']
atom_pair = []

n = 0
for i in range(ntypes):
    for j in range(i, ntypes):
        ic = i*(2*ntypes-i-1)/2 + j
        #draw_pair.append(ic)
        atom_pair.append(atom_types[i] + ' - ' + atom_types[j])
        coeff[n] = 1.0
        n = n + 1

r, gr, gr_tot = utils.grsq.calc_gr(cfg, dr, coeff)

print(gr)

with open('gr.txt', mode='w') as f:
    
    for i in range(len(r)):
        f.write('{:11.06f}'.format(r[i]))
        for j in range(npar):
            f.write('{:11.06f}'.format(gr[i][j]))
        f.write('\n')


