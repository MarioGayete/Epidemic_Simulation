# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 20:34:51 2022

@author: Mario-Usuario
"""

# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
from math import *

# Importing functions
from physics import *
from drawing_functions import *
from updating import *

# Check collisions with the wall
N_ppl = 2
domain = 2
R_eq2person = 0.25
r0 = np.zeros((N_ppl,2))
r0[0,:] = [0.25, 0.25]
r0[1,:] = [1.75, 1.75]
max_step = 1
step_scalar = max_step*np.random.rand(N_ppl)
step_angle =2*pi * np.random.rand(N_ppl)

r1 = r0.copy()
r1[0,:] = update_local_position(r0[0,:], step_scalar[0], step_angle[0])

r1_post, step_scalar = avoid_wall_collision(r0, r1, step_scalar, step_angle, R_eq2person, domain)

plt.figure()
draw_line([0,0], [0,domain])
draw_line([0,domain], [domain,domain])
draw_line([domain,domain], [domain,0])
draw_line([domain,0], [0,0])
draw_line(r0[0,:], r1[0,:],  ccolor = 'b')
draw_circle(r0[0,:], R_eq2person)
draw_circle(r1[0,:], R_eq2person, ccolor = 'r')
draw_circle(r1_post[0,:], R_eq2person, ccolor = 'g', clinestyle = '--')

# Check collisions with among particles
step_scalar[0] = 0.5
step_scalar[1] = 0.5
step_angle[0] = pi/4
step_angle[1] = pi/4 + pi

for i in range(0,3):

    for i_ppl in range(0,N_ppl):
        r1[i_ppl,:] = update_local_position(r0[i_ppl,:], step_scalar[i_ppl], step_angle[i_ppl])
        
        # Avoid collision with the walls
        r1, step_scalar = avoid_wall_collision(r0, r1, step_scalar, step_angle, R_eq2person, domain)
        
        # Avoid collisions among people
        r1 = avoid_ppl_collision(r0, r1, step_scalar, step_angle, R_eq2person)
    
    
    
    plt.figure()
    draw_rectangle([0,0], [0,domain], [domain,domain], [domain,0])
    draw_circle(r0[0,:], R_eq2person, ccolor = 'k')
    draw_circle(r0[1,:], R_eq2person, ccolor = 'b')
    draw_circle(r1[0,:], R_eq2person, ccolor = 'r', clinestyle='--')
    draw_circle(r1[1,:], R_eq2person, ccolor = 'g',  clinestyle='--')
    
    for i_ppl in range(0,N_ppl):
        r0[i_ppl,:] = r1[i_ppl,:]


