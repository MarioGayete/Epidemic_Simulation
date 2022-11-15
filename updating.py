# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

# Importing libraries
from math import *

def update_local_position(r0, step_scalar, step_angle):
    r1 = r0.copy()
    r1[0] = r0[0] + step_scalar * cos(step_angle)
    r1[1] = r0[1] + step_scalar * sin(step_angle)
    
    return r1
