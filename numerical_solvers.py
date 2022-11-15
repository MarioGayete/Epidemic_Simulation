# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

# Importing libraries
import numpy as np
from math import *

# Import functions
from physics import *
from measurements import *
from updating import *


def Newton_bisection_collision_particle(r0, r1, r2, Ax, R_eq2person, step_angle, epsilon = 1e-12, max_it = 1e3):
    # Initialization
    it = 0
    
    # Maximum distance keeping the first particle still
    dist_right = func_distance(r0,r2)
    Ax_right = 0
    r_right = r0
    
    # Minimum distance (the collision)
    dist_left = func_distance (r1,r2)
    Ax_left = func_distance (r0,r1)
    r_left = r1
    
    while True:
        Ax_mid = Ax_right + (2*R_eq2person - dist_right)/ (dist_left - dist_right) * (Ax_left - Ax_right)
        
            
        r_mid = update_local_position(r0, Ax_mid, step_angle)
        dist_mid = func_distance (r_mid,r2)
        if abs(dist_mid - 2*R_eq2person) < epsilon:
            return r_mid, Ax_mid
        
        else:
            if dist_mid > 2*R_eq2person:
                dist_right = dist_mid
                Ax_right = Ax_mid
                r_right = r_mid
            else:
                dist_left = dist_mid
                Ax_left = Ax_mid
                r_left = r_mid

        it += 1
        
        """if it%1000 == 0:
            print('it = ' + str(it) + ' -- Current step = ' + str(Ax_mid) + ' -- Current distance = ' + str(dist_mid) +
                  ' -- Limits = [' + str(dist_right) + ',' + str(dist_left) + ']')"""
        
        if it>max_it:
            r_mid = update_local_position(r0, Ax_mid*0.9, step_angle)
            dist_mid = func_distance (r_mid,r2)
            if dist_mid > 2*R_eq2person:
                return r_mid,Ax_mid*0.9
            else:
                return r0, 0
            
            
    
    