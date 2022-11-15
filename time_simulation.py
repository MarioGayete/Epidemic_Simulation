# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

# Importing libraries
import numpy as np
from math import *
import random as random

# Import functions
from physics import *
from measurements import *

def update_position(r0, r0_prev_forced, step_scalar, step_angle, R_eq2person, domain, movement_vector, 
                    mov_times_social_dist, status,quarantine, time_when_shopping, T_supermarket,
                    t_in_supermarket, supermarket_location, going2supermarket, current_shopping, t, At,
                    collision_ppl = False):
   
    N_ppl = r0.shape[0]
    # Force the quarantine for the infecteds
    r0, r1_prev_forced = forced_quarantine(r0, r0_prev_forced, status, quarantine)
    
    # Forced movement to go to the supermarket
    r0, r1_prev_forced, current_shopping = going2supermarked(r0, r1_prev_forced, time_when_shopping, T_supermarket, 
                         t_in_supermarket, supermarket_location, going2supermarket, current_shopping, t, At, status, quarantine)
    
    r1 = r0.copy()
    
    for i_ppl in range(0,N_ppl):
        if status[i_ppl] != 3 and r1[i_ppl,0] > -1e29: # dead particles do not move
            if movement_vector[i_ppl] == 1:
                r1[i_ppl,:] = update_local_position(r0[i_ppl,:], step_scalar[i_ppl], step_angle[i_ppl])
            else:
                r1[i_ppl,:] = update_local_position(r0[i_ppl,:], mov_times_social_dist* step_scalar[i_ppl], 
                                                    step_angle[i_ppl])
    
    # Avoid collision with the walls
    r1, step_scalar = avoid_wall_collision(r0, r1, step_scalar, step_angle, R_eq2person, domain)
    
    if collision_ppl == True and quarantine == False and current_shopping == False:
        # Avoid collisions among people
        r1 = avoid_ppl_collision(r0, r1, step_scalar, step_angle, R_eq2person)
    
    return r1, r1_prev_forced
    

def spreading_virus(r, status, R_spread, Probablitity_spread, tau, latent_time, time_from_infection, At ):
    N_ppl = r.shape[0]
    
    # Infection and cure
    for i_ppl in range(0,N_ppl):
        # Check if this particle is infected
        # If it is not infected, check if someone could spread the virus into him
        if status[i_ppl] == 0: # Not infected
            for j_ppl in range(0,N_ppl):
                if i_ppl != j_ppl:
                    if status[j_ppl] == 1 or  status[j_ppl] == 4: # Infected  
                        infected = infection_physics(func_distance (r[i_ppl,:],r[j_ppl,:]),
                                                     R_spread, Probablitity_spread)
                        if infected == True:
                            status[i_ppl] = 4 # infected but still latent
                            break # there is no need to keep on the loop, this particles has been infected
        elif status[i_ppl] == 1: # Infected
            # If it is infected, check if the particle has been cured
            if tau < time_from_infection[i_ppl]:
                status[i_ppl] = 2
                time_from_infection[i_ppl] = 0
            else:
                time_from_infection[i_ppl] += At
        elif status[i_ppl] == 2:
        # if cured, at the minute nothing happens but maybe some reinfection can be considered
            non_done = None
        elif status[i_ppl] == 4: # latent infection
            if time_from_infection[i_ppl] > latent_time:
                status[i_ppl] = 1
            time_from_infection[i_ppl] += At
        
    return status

def define_movement(step_scalar, step_angle, max_step, change_movement, N_ppl):
    if change_movement == True or len(step_scalar) == 0:
        # Vector step
        step_scalar = max_step*np.random.rand(N_ppl)
        step_angle = 2*pi * np.random.rand(N_ppl)
    
    else:
        for i in range(0,N_ppl):
            if step_scalar[i] == 0: # this means that the particle is colliding with the wall, 
                                    # so let's fins a new movement
                step_scalar[i] =  max_step*random.random()
                step_angle[i] =  pi + step_angle[i] #2*pi*random.random()
    
    return step_scalar, step_angle

def check_if_dead(status, death_probability):
    N_ppl = len(status)
    for i_ppl in range(0,N_ppl):
        if  status[i_ppl] == 1: # Infected.
            # Check if the particle has died
            if random.random() < death_probability: # the particle has died
                status[i_ppl] = 3
    return status

def forced_quarantine(r, r_prev_forced, status, quarantine):
    if quarantine == True:
        N_ppl = len(status)
        for i_ppl in range(0,N_ppl):
            if  status[i_ppl] == 1: # Infected.
                if  r[i_ppl,0] >= -1e29:
                    r_prev_forced[i_ppl,:] = r[i_ppl,:]
                # Force the position of the particle to quarantine
                r[i_ppl,0] = -1e30
                r[i_ppl,1] = -1e30
            elif status[i_ppl] != 1: # not forced to quarantine
                if  r[i_ppl,0] <= -1e29:
                    r[i_ppl,:] = r_prev_forced[i_ppl,:]
                else:
                    r_prev_forced[i_ppl,:] = r[i_ppl,:]
                
    return  r, r_prev_forced

def going2supermarked(r, r_prev_forced, time_when_shopping, T_supermarket, t_in_supermarket, supermarket_location, 
                      going2supermarket, current_shopping, t, At, status, quarantine):
    
    if going2supermarket == True:
        N_ppl = r.shape[0]
        for i_ppl in range(0,N_ppl):
            if status[i_ppl] == 1 and quarantine == True: # Infected.
                current_shopping[i_ppl] = 0
            else:
                if int((t-time_when_shopping[i_ppl])/T_supermarket) != int((t+At-time_when_shopping[i_ppl])/T_supermarket) or t-time_when_shopping[i_ppl]==0:
                    # It's time to go to the supermarket
                    current_shopping[i_ppl] += At
                    r_prev_forced[i_ppl,:] = r[i_ppl,:]
                    r[i_ppl,:] = supermarket_location
                else:
                    if current_shopping[i_ppl] == 0: # Not shopping
                        r_prev_forced[i_ppl,:] = r[i_ppl,:]
                    else: # currently shopping
                        current_shopping[i_ppl] += At
                        if current_shopping[i_ppl] > t_in_supermarket: #finished shopping
                            current_shopping[i_ppl] = 0
                            r[i_ppl,:] = r_prev_forced[i_ppl,:]
                        else: # continue shopping
                            current_shopping[i_ppl] += At
                            r[i_ppl,:] = supermarket_location
    
    return r, r_prev_forced, current_shopping
                            
                            
    
    
        
                        
                        
            

    
    




                    
                
            
        
            
    
    
    
    
    
    
    
