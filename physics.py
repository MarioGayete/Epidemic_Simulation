# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

# Importing libraries
import numpy as np
from math import *
import random as random

# Importing functions
from numerical_solvers import *
from measurements import *
from updating import *

def collision(r1, r2, R_eq2person):
    
    distance = func_distance (r1,r2)
    
    if distance < 2*R_eq2person - 1e-6 : # there is collision
        return True
    else:
        return False

def avoid_wall_collision(r0, r1, step_scalar, step_angle, R_eq2person, domain):
    N_ppl = r1.shape[0]
    
    for i_ppl in range(0,N_ppl):
        if r1[i_ppl,0] >= -1e29: # if particles are on quarantine, it is not applied to them
            # Avoid collision in the x-axis
            if r1[i_ppl,0] - R_eq2person < 0: # collision with the left wall
                new_step_scalar = (r0[i_ppl,0] - R_eq2person)/cos(pi - step_angle[i_ppl])
                r1[i_ppl,:] = update_local_position(r0[i_ppl,:], new_step_scalar, step_angle[i_ppl])
                step_scalar[i_ppl] = new_step_scalar
            
            elif r1[i_ppl,0] + R_eq2person > domain: # collision with the right wall
                new_step_scalar = (domain - R_eq2person - r0[i_ppl,0])/cos(step_angle[i_ppl])
                r1[i_ppl,:] = update_local_position(r0[i_ppl,:], new_step_scalar, step_angle[i_ppl])
                step_scalar[i_ppl] = new_step_scalar
            
            # Check errors
            if r1[i_ppl,0] - R_eq2person < -1e-9: # collision with the left wall
               print('Left collision')
               
               #input('......')
            
            if r1[i_ppl,0] + R_eq2person > domain + 1e-9: # collision with the right wall
                print('Right collision')
                input('......')
                
            # Avoid collision in the y-axis
            if r1[i_ppl,1] - R_eq2person < 0: # collision with the bottom wall
                new_step_scalar = (- R_eq2person + r0[i_ppl,1])/sin(2*pi - step_angle[i_ppl])
                r1[i_ppl,:] = update_local_position(r0[i_ppl,:], new_step_scalar, step_angle[i_ppl])
                step_scalar[i_ppl] = new_step_scalar
            
            elif r1[i_ppl,1] + R_eq2person > domain: # collision with the top wall
                new_step_scalar = (domain - R_eq2person - r0[i_ppl,1])/sin(step_angle[i_ppl])
                r1[i_ppl,:] = update_local_position(r0[i_ppl,:], new_step_scalar, step_angle[i_ppl])
                step_scalar[i_ppl] = new_step_scalar
            
            # Check errors
            
            # Avoid collision in the y-axis
            if r1[i_ppl,1] - R_eq2person < -1e-9: # collision with the bottom wall
                print('Bottom collision')
                print(r1[i_ppl,:])
                print(step_scalar[i_ppl])
                print(step_angle[i_ppl])
                input('......')
            
            elif r1[i_ppl,1] + R_eq2person > domain + 1e-9: # collision with the top wall
                print('Top collision')
                print(r1[i_ppl,:])
                print(step_scalar[i_ppl])
                print(step_angle[i_ppl])
                input('......')

    return r1, step_scalar

def avoid_ppl_collision(r0, r1, step_scalar, step_angle, R_eq2person):
    # We reduce the step of each particle to a minimum of step = 0, meaning that it stays on the place
    collision_particles = True
    N_ppl = r1.shape[0]
    while collision_particles == True:
        # We iterate until there are no collisions
        for i_ppl in range(0,N_ppl):
            for j_ppl in range(0,N_ppl):
                if i_ppl != j_ppl:
                    if collision(r1[i_ppl,:], r1[j_ppl,:], R_eq2person) == True:
                        # Check if stay still the collision still exists
                        if collision(r0[i_ppl,:], r1[j_ppl,:], R_eq2person) == False:
                            
                        # If they do not collide, we compute the maximum step allowed for i_ppl
                            r1[i_ppl,:], new_step_scalar = Newton_bisection_collision_particle(r0[i_ppl,:], r1[i_ppl,:], 
                                                                                               r1[j_ppl,:], step_scalar[i_ppl], 
                                                                                               R_eq2person, step_angle[i_ppl])
                        else:
                            # If they collide with the 0 step, then we don't move this particle
                            r1[i_ppl,:] = r0[i_ppl,:]

                        
        # Check if there are still collisions
        collision_particles = False
        for i_ppl in range(0,N_ppl):
            for j_ppl in range(0,N_ppl):
                if i_ppl != j_ppl:
                    if collision(r1[i_ppl,:], r1[j_ppl,:], R_eq2person) == True:
                        collision_particles = True
                        
                    
        
    return r1


def infection_physics(distance, R_spread, Probablitity_spread):
    # Depending on the distance, there is a probability to get infected 
    # The closer, the most likely to get infected
    N_radius = len(R_spread)
    
    for i_R in range(0,N_radius):

        if distance < R_spread[i_R]: # the probability of infection is found
            # pick a random number
            rand_numb = random.random()
            
            # If this random number is from 0 to the spreading likelyhood, then the virus has been spread
            if rand_numb < Probablitity_spread[i_R]:
                return True
            else:
                return False
    
    # If the distance is higher than the maximum spreading distance, the there is no risk of infection
    return False

