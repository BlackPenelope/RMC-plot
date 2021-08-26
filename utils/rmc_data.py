# -*- coding: utf-8 -*-
import numpy as np
import math
from core.rmc_configuration import RmcConfiguration

def is_float(s):
    """
    str is 'float' change abailable
    """
    try:
        float(s)
    except:
        return False
    return True

def is_int(s):
    """
    str is 'int' change abailable
    """
    try:
        int(s)
    except:
        return False
    return True

class RmcData(object):
    """
    :class RMC dat class
    """
    def __init__(self, cfg):
        self.title = ""
        #self.path = path
        self.rho = 0.0
        self.ntypes = len(cfg.ni)
        self.npar = int(self.ntypes*(self.ntypes+1)/2)
        self.rcut = np.zeros(self.npar)
        self.delta = np.zeros(self.npar)
        self.dr = 0.0
        self.moveout = False
        self.ncoll = 0
        self.iprint = 0
        self.timelim = 0.0
        self.timesav = 0.0

    def read(self, path):
        self.path = path
        try:
            with open(self.path.encode("utf-8"), "r") as f:
                self.title = f.readline()
                items = f.readline().split()
                self.rho = float(items[0])

                v = []
                while self.npar > len(v):
                    items = f.readline().split()
                    for item in items:
                        if is_float(item):
                            v.append(float(item))
                        else:
                            continue

                self.rcut = v

                items = f.readline().split()
                for i in range(self.ntypes):
                    self.rcut[i] = float(items[i])

                items = f.readline().split()
                self.dr = float(items[0])
                
                str = f.readline()
                if '.false.' in str or '.F.' in str:
                    self.moveout = False
                else:
                    self.moveout = True
                
                items = f.readline().split()
                self.ncoll = int(items[0])

                items = f.readline().split()
                self.iprint = int(items[0])

                items = f.readline().split()
                self.timelim = int(items[0])
                self.timesav = int(items[1])

        except IOError:
            raise
        except Exception as e:
            print(e)
            pass
        
if __name__ == '__main__':
    
    cfg = RmcConfiguration()
    cfg.read('./data/sio2_fq.cfg')

    dat = RmcData(cfg)
    dat.read('./data/sio2_fq.dat')
    
