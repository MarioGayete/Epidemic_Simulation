# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""
def func_distance(r1,r2):
    dim = len(r1)
    
    sum_squares = 0.0
    
    for i in range(0,dim):
        sum_squares += (r2[i] - r1[i])**2
         
    return sum_squares**0.5

def count_status(status):
    count_noninfected = 0
    count_infected = 0
    count_cured = 0
    count_dead = 0
    
    for i in range(0,len(status)):
        if status[i] == 0: # non infected
            count_noninfected += 1
        elif status[i] == 1 or status[i] == 4: # infected with or without simptoms
            count_infected += 1
        elif status[i] == 2: # cured
            count_cured += 1
        elif status[i] == 3: #dead
            count_dead += 1
    
    return count_noninfected, count_infected, count_cured, count_dead
        
