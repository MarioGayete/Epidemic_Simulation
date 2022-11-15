# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


# Importing functions
from preprocess import *
from time_simulation import *
from drawing_functions import *
from post_process import *
from measurements import *

# Input data
# People parameters
N_people = 500
R_eq2person = 1 # Radius equivalent to a person (each person will be represented as a circle of radius R_eq2person)
area_person = np.pi * R_eq2person**2 # sqaure meter per person
density = 0.1 # people per sqare meter
percent_social_dist = 0 # % approx of people doing social distancing
mov_times_for_social_distancing = 0 # multiplier of the movement when someone is social distant
# Numerical parameters
At = 0.1
vel = 20
max_displ = At*vel
max_t = 30
T_change_movement = 1 # period at which the particles change the movement
# Virus parameters
# The virus will have different probabilities to be spread as a function of the distance. 
# 3 different distances will be considered: contact, medium disntance, and furthest spreading distance
R_spread =  [2*R_eq2person *1.01,2*R_eq2person *1.15,2*R_eq2person *1.25]
Probablitity_spread = [0.2,0.1,0.05]
# Determine time for recovering from virus
tau = 15 # recovery_time
latent_time = 5 # time being infectious before noticing to be infected
death_probability = 0.05*At/tau # probability to die due to the infection
# Movement data
# Supermarket
T_supermarket = 15 # period (inverse of frequency) of going to the groceries store
t_in_supermarket = 0.1 # time spent in the supermarked
going2supermarket = True
# Quarantine
quarantine = True # if it is true, infected people will be separated from the group until being cured



# Counting parameters
count_noninfected = []
count_infected = []
count_cured = []
count_dead = []
R = [] # transmission test for each day
t_vec = []
t_R = []

#  Video generation
video_gen = True

# Generate the folder
output_images_folder = 'output_images/'
output_images_video = 'output_video/'
output_histogram_plot = 'output_plots/'
current_date = datetime.now()
subfolder = str(current_date.year) + str(current_date.month) + str(current_date.day) + '/'
if os.path.isdir(output_images_folder + subfolder) == False:
    os.mkdir(output_images_folder + subfolder)
    
if os.path.isdir(output_images_video) == False:
    os.mkdir(output_images_video)
    
if os.path.isdir(output_histogram_plot) == False:
    os.mkdir(output_histogram_plot)



# Preprocess
domain, r, status, time_from_infection, movement_vector, time_when_shopping, current_shopping, supermarket_location = preprocess(N_people, 
                R_eq2person, area_person, density, percent_social_dist, T_supermarket)
r_prev_forced = r.copy()
# Scramble a bit so it doesn't look like very weel organized
for i in range(0,10):
    step_scalar, step_angle = define_movement([], [], max_displ, True, N_people)
    r, r_prev_forced = update_position(r,r_prev_forced, step_scalar, step_angle, R_eq2person, domain, movement_vector, 
                        mov_times_for_social_distancing, status, quarantine, time_when_shopping, T_supermarket,
                        t_in_supermarket, supermarket_location, going2supermarket, current_shopping, 0, 0)

# Time simulation
t = 0
i_frame = 0
change_movement = True
prev_count_noninfected, prev_count_infected, prev_count_cured = N_people - 1,1,0
final = False
if video_gen == True:
    draw_current_situataion(domain, status, R_eq2person, r, t, output_images_folder + subfolder 
                            + str(i_frame) + '.jpg')
    i_frame += 1

while final == False:
    step_scalar, step_angle = define_movement(step_scalar, step_angle, max_displ, change_movement, N_people)
    # New position of the particles
    r, r_prev_forced = update_position(r, r_prev_forced, step_scalar, step_angle, R_eq2person, domain, movement_vector, 
                        mov_times_for_social_distancing, status, quarantine, time_when_shopping, T_supermarket,
                        t_in_supermarket, supermarket_location, going2supermarket, current_shopping, t, At)
    # Update the infection status
    status = spreading_virus(r, status, R_spread, Probablitity_spread, tau, latent_time, time_from_infection, At )
    status = check_if_dead(status, death_probability)
    # Add the counters
    current_count_noninfected, current_count_infected, current_count_cured, current_count_dead = count_status(status)
    count_noninfected.append(current_count_noninfected)
    count_infected.append(current_count_infected)
    count_cured.append(current_count_cured)
    count_dead.append(current_count_dead)
    # Compute R
    if t%1 == 0:
        if prev_count_infected == 0:
            current_R = 0
        else:
            current_R = current_count_infected / prev_count_infected - 1
        R.append(current_R)
        t_R.append(t)
        prev_count_infected = current_count_infected
    
    # Update the time vector
    t_vec.append(t)
    
    # Check if the movement direction has to be changed
    if len(t_vec) == 1 or int(t_vec[-2]/T_change_movement) != int(t/T_change_movement):
        change_movement = True
    else:
        change_movement = False
    
    
    
    if t % 10 == 0:
        print('Current time = ' + str(t))
    
    t += At
    t = round(t,3)
    
    if video_gen == True:
        draw_current_situataion(domain, status, R_eq2person, r, t, output_images_folder + subfolder 
                                + str(i_frame) + '.jpg')
        i_frame += 1
    
    if t > max_t:
        final = True
        
# Generate the video
if video_gen == True:
    video_generation_from_images(output_images_video +  str(current_date.year) + str(current_date.month) + 
                          str(current_date.day) + 'project.avi', output_images_folder + subfolder, i_frame, At)
    
# Generate the histogram
plot_histogram(t_vec, count_noninfected, count_infected, count_cured, count_dead, output_histogram_plot +
                               str(current_date.year) + str(current_date.month) + str(current_date.day) + '_histogram.jpg')
# Generate the R evolution
plot_R_evolution(t_R, R, output_histogram_plot + 
                               str(current_date.year) + str(current_date.month) + str(current_date.day) + '_R.jpg')







