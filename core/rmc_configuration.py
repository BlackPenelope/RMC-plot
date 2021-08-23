# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:54:58 2021

@author: H. Morita
"""

import numpy as np
import os
import os.path
import sys
import math

class RmcConfiguration(object):
    """
    :class RMC Configuration class 
    """    
    class Atoms(object):
        """
        This class represents a list of atoms and their properties: 
        """
        def __init__(self, *args):
            positions = args[0]
            elements = args[1]
            
            self.positions = np.array(positions, dtype=np.float, copy=False)
            self.number = self.positions.shape[0]
            self.elements = np.array(elements, dtype="|S4", copy=False)
    
    def __init__(self):
        self.header = ""
        self.title = ""
        self.ngen = 0
        self.ntried = 0
        self.nacc = 0
        self.nsaved = 0
        self.nmol = 0
        self.nmol_types = 0
        self.nsites_max = 1
        self.neuler = 0
        self.ni = [] # number of eech atoms
        self.nsites = []
        self.sites = []
        self.truncated = False
        self.vectors = np.identity(3)
        self._metric = None
        self.file_name = ""
        self.atoms = None
        #self.path = path
        #f = open(self.path, "r")
        #f.close()

    @property
    def metric(self):
        if self._metric == None:
            self._metric = np.identity(3)
            for i in range(3):
                for j in range(3):
                    self._metric[i][j] = 0.0
                    for k in range(3):
                        self._metric[i][j] = self._metric[i][j] + \
                            self.vectors[k][i] * self.vectors[k][j]

        return self._metric

    @property
    def volume(self):
        triprod = self.vectors[0][0]*self.vectors[1][1]*self.vectors[2][2] \
                + self.vectors[1][0]*self.vectors[2][1]*self.vectors[0][2] \
                + self.vectors[2][0]*self.vectors[0][1]*self.vectors[1][2] \
                - self.vectors[2][0]*self.vectors[1][1]*self.vectors[0][2] \
                - self.vectors[1][0]*self.vectors[0][1]*self.vectors[2][2] \
                - self.vectors[0][0]*self.vectors[2][1]*self.vectors[1][2]
        self._volume = 8.0*abs(triprod)
        if(self.truncated == True):
            self._volume = self._volume/2.0

        return self._volume
    
    @property
    def d(self):
        triprod = self.vectors[0][0]*self.vectors[1][1]*self.vectors[2][2] \
                + self.vectors[1][0]*self.vectors[2][1]*self.vectors[0][2] \
                + self.vectors[2][0]*self.vectors[0][1]*self.vectors[1][2] \
                - self.vectors[2][0]*self.vectors[1][1]*self.vectors[0][2] \
                - self.vectors[1][0]*self.vectors[0][1]*self.vectors[2][2] \
                - self.vectors[0][0]*self.vectors[2][1]*self.vectors[1][2]

        axb1=self.vectors[1][0]*self.vectors[2][1]-self.vectors[2][0]*self.vectors[1][1]
        axb2=self.vectors[2][0]*self.vectors[0][1]-self.vectors[0][0]*self.vectors[2][1]
        axb3=self.vectors[0][0]*self.vectors[1][1]-self.vectors[1][0]*self.vectors[0][1]
        bxc1=self.vectors[1][1]*self.vectors[2][2]-self.vectors[2][1]*self.vectors[1][2]
        bxc2=self.vectors[2][1]*self.vectors[0][2]-self.vectors[0][1]*self.vectors[2][2]
        bxc3=self.vectors[0][1]*self.vectors[1][2]-self.vectors[1][1]*self.vectors[0][2]
        cxa1=self.vectors[1][2]*self.vectors[2][0]-self.vectors[2][2]*self.vectors[1][0]
        cxa2=self.vectors[2][2]*self.vectors[0][0]-self.vectors[0][2]*self.vectors[2][0]
        cxa3=self.vectors[0][2]*self.vectors[1][0]-self.vectors[1][2]*self.vectors[0][0]
        d1 = triprod/math.sqrt(axb1**2+axb2**2+axb3**2)
        d2 = triprod/math.sqrt(bxc1**2+bxc2**2+bxc3**2)
        d3 = triprod/math.sqrt(cxa1**2+cxa2**2+cxa3**2)
        _d = min(d1,d2,d3)
        
        if (self.truncated):
            
            d1 = 1.5*triprod/math.sqrt( \
                (axb1+bxc1+cxa1)**2+(axb2+bxc2+cxa2)**2+(axb3+bxc3+cxa3)**2)
            d2 = 1.5*triprod/math.sqrt( \
                (axb1-bxc1+cxa1)**2+(axb2-bxc2+cxa2)**2+(axb3-bxc3+cxa3)**2)
            d3 = 1.5*triprod/math.sqrt( \
                (axb1+bxc1-cxa1)**2+(axb2+bxc2-cxa2)**2+(axb3+bxc3-cxa3)**2)
            d4 = 1.5*triprod/math.sqrt( \
                (axb1-bxc1-cxa1)**2+(axb2-bxc2-cxa2)**2+(axb3-bxc3-cxa3)**2)
            _d = math.min(_d,d1,d2,d3,d4)
        
        return _d
    
    def read(self, path):
        
        self.path = path        
        try:
            positions = []
            with open(self.path.encode("utf-8"), "r") as f:
                try:
                    
                    self.header = f.readline()
                    self.title = f.readline()
                                        
                    line=f.readline()
                    items = line.strip()
                    while len(items) == 0:
                        line=f.readline()
                        items = line.strip()

                    #line = f.readline()
                    item = line.split()                    
                    self.ngen = int(item[0])
                    self.ntried = int(item[1])
                    self.nacc = int(item[2])
                    line = f.readline()
                    self.nsaved = int(line.split()[0])
                    f.readline()
                    line = f.readline()
                    self.nmol = int(line.split()[0])
                    line = f.readline()
                    self.nmol_types = int(line.split()[0])
                    line = f.readline()
                    self.nsites_max = int(line.split()[0])
                    line = f.readline()
                    self.neuler = int(line.split()[0])
                    
                    f.readline()
                    line = f.readline()                    

                    if line.split()[0] == 'F':
                        self.truncated = False
                    elif line.split()[0] == 'T':
                        self.truncated = True
                    f.readline()
                    
                    for i in range(3):
                        line = f.readline()
                        xyz = np.fromstring(line, dtype=float, sep=' ') 
                        self.vectors[i] = xyz
                    
                    f.readline()
                    for i in range(self.nmol_types):
                        line = f.readline()
                        self.ni.append(int(line.split()[0]))
                        line = f.readline()
                        n = int(line.split()[0])
                        self.nsites.append(n)
                        s = []
                        for k in range(n):
                            line = f.readline()
                            s.append(np.fromstring(line, dtype=float, sep=' '))
                        self.sites.append(s)
                        f.readline()
                    
                    # positions
                    for i in range(self.nmol):
                        line = f.readline()
                        x, y, z = line.split()
                        position = np.array([float(x), float(y), float(z)])
                        positions.append(position)
                    
                except StopIteration:
                    pass
            self.atoms = RmcConfiguration.Atoms(positions, None)
        except IOError:
            raise
        except Exception as e:
            print(e)
            pass
        
    def write(self, path):
        with open(path, mode='w') as f:
            f.write("(Version 3 format configuration file)\n")
            f.write(self.title)
            f.write('\n\n')            
            f.write(" ")
            f.write("{:>10d}".format(self.ngen))
            f.write("{:>10d}".format(self.ntried))
            f.write("{:>10d}".format(self.nacc))
            f.write(" moves generated, tried, accepted\n")
            f.write(" ")
            f.write("{:>10d}".format(self.nsaved))
            f.write("                     configurations saved\n\n")
            f.write(" ")
            f.write("{:>10d}".format(self.nmol))
            f.write(" molecules (of all types)\n")
            f.write(" ")
            f.write("{:>10d}".format(self.nmol_types))
            f.write(" types of molecule\n")
            f.write(" ")
            f.write("{:>10d}".format(self.nsites_max))
            f.write(" is the largest number of atoms in a molecule\n")
            f.write(" ")
            f.write("{:>10d}".format(self.neuler))
            f.write(" Euler angles are provided\n\n")
            f.write("          ")
            if self.truncated == True:
                f.write('T')
            else:
                f.write('F')
            f.write(" (Box is not truncated octahedral)\n")
            f.write("           ")
            f.write(" Defining vectors are:\n")            
            for i in range(3):
                f.write("           ")
                f.write('{:11.06f}'.format(self.vectors[i][0]))
                f.write('{:11.06f}'.format(self.vectors[i][1]))
                f.write('{:11.06f}\n'.format(self.vectors[i][2]))
            f.write('\n')
            
            for i in range(self.nmol_types):
                f.write("{:>11d}".format(self.ni[i]))
                f.write(" molecules of type")
                f.write("{:>3d}\n".format(i+1))
                f.write("{:>11d}".format(self.nsites[i]))                
                f.write(" atomic sites\n")
                f.write("           ")
                
                for n in range(self.nsites[i]):
                    f.write('{:11.06f}'.format(self.sites[i][n][0]))
                    f.write('{:11.06f}'.format(self.sites[i][n][1]))
                    f.write('{:11.06f}'.format(self.sites[i][n][2]))
                    f.write('\n\n')
                    
            f.write('\n')
            
            for i in range(self.nmol):
                f.write('{:11.07f}'.format(self.atoms.positions[i][0]))
                f.write('{:11.07f}'.format(self.atoms.positions[i][1]))
                f.write('{:11.07f}\n'.format(self.atoms.positions[i][2]))
                    

if __name__ == '__main__':
    config = RmcConfiguration("ran.cfg")
    config.read()
    #print(np.dot(v, config.vectors))
