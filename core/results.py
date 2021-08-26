# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 12:50:33 2021

@author: Morita-T1700
"""

class Results(object):
    """
    RMC results Class
    
    Attributes
    ----------
    selected : str
        selected element symbol  
    """
    def __init__(self):
        self.path = ''
        self.cfg = None
        self.r = None
        self.gr = None
        self.total_gr = None