# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

# Importing libraries
import numpy as np
import random as random


def preprocess(N_people, R_eq2person, area_person, density, percentage_social_dist, T_supermarket):
    # Build the domain
    domain = domain_generation(N_people, area_person, density)
    # Generate the initial coordinates and the initial status
    r, status = position_and_status_initialization(N_people, R_eq2person, domain)
        
    # Build the time from infection matrix to check how much time has past since each particle got infected
    time_from_infection = np.zeros((N_people,1))
    
    # Build the vector indicating which particle moves and which one does not
    movement_vector = social_distancing(percentage_social_dist, N_people)
    
    # Define when everyone is going ot the supermarket
    time_when_shopping, current_shopping = time_to_go_to_supermarket(N_people, T_supermarket)
    supermarket_location = [domain/2, domain/2]
    
    return domain, r, status, time_from_infection, movement_vector, time_when_shopping,current_shopping, supermarket_location

def domain_generation(N_people, area_person, density):
    # Function to generate the dimensions of the domain
    total_area_person = N_people*area_person # total area occupied by all people
    total_area = total_area_person/density # total area generated
    
    length_domain = total_area**0.5 # the domain will be [0,length_domain] x [0,length_domain]
    
    return length_domain

def position_and_status_initialization(N_people, R_eq2person, domain):
    # We initialize the position of each single person 
    # We assume that it is ordenated correctly
    
    float_rows = N_people**0.5
    N_people_row = int(float_rows)
    float_cols = N_people/N_people_row
    if float_cols%2 != 0: # we have an odd number of people, so we need an extra column
        N_people_col = int(float_cols) + 1
    else:
        N_people_col = int(float_cols)
    # We set the positions
    r = np.zeros((N_people,2))
    Ax = domain/N_people_col
    Ay = domain/N_people_row
    
    if Ax < R_eq2person or Ay < R_eq2person:
        print('The density is too high so there is initial collision')
        return None
    
    current_row = 0
    current_col = 0
    
    r[0,0] = Ax/2
    r[0,1] = Ay/2
    current_col += 1
    # First fill row, then fill column
    for i_ppl in range(1,N_people):
        r[i_ppl,0] = Ax/2 + Ax * current_col
        r[i_ppl,1] = Ay/2 + Ay * current_row
        current_col += 1
        if current_col == N_people_col: # check if we have reached the last element of the row
            current_col = 0
            current_row += 1
    
    # Build the status matrix
    # 0 --> healthy 
    # 1 --> infected
    status = np.zeros((N_people,1))
    
    index_case_0 = random.randint(0, N_people-1)
    status[index_case_0] = 4 #infected but not contagious    
    
    
    return r, status

def social_distancing(percentage, N_ppl):
    
    movement_vector = np.zeros(N_ppl)
    # the percentage is for example a 50%
    probability_vector = np.random.rand(N_ppl)
    
    for i in range(0,N_ppl):
        if probability_vector[i] >= percentage/100: # this particle is moving
            movement_vector[i] = 1
    
    return movement_vector
    

def time_to_go_to_supermarket(N_ppl, T_supermarket):
    
    time_when_shopping = np.random.rand(N_ppl)*T_supermarket
    current_shopping = np.zeros(N_ppl)
    return time_when_shopping, current_shopping
        
        
    
    
    
    