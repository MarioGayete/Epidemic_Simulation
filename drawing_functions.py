# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

# Importing libraries
import numpy as np
import matplotlib.pyplot as plt
from math import *

def draw_line(p1,p2, ccolor = 'k',  clinestyle = '-'):
    plt.plot([p1[0],p2[0]], [p1[1],p2[1]], color = ccolor, linestyle = clinestyle)
    
    return 0

def draw_circle(center, R, ccolor = 'k', clinestyle = '-'):
    angle = np.linspace(0, 2*pi, 1000)
    points = np.zeros((len(angle),2))
    
    for i in range(0,len(angle)):
        points[i,0] = center[0] + R * cos(angle[i])
        points[i,1] = center[1] + R * sin(angle[i])
    
    plt.plot(points[:,0], points[:,1] , color = ccolor, linestyle = clinestyle)
    
    return 0

def draw_rectangle(p1,p2,p3,p4, ccolor = 'k',  clinestyle = '-'):
    draw_line(p1, p2, ccolor = ccolor, clinestyle = clinestyle)
    draw_line(p2, p3, ccolor = ccolor, clinestyle = clinestyle)
    draw_line(p3, p4, ccolor = ccolor, clinestyle = clinestyle)
    draw_line(p4, p1, ccolor = ccolor, clinestyle = clinestyle)
    
    return 0

def draw_current_situataion(domain, status, R_eq2person, r, t, filename):
    #color_vec = ['b','r','g','k']
    plt.figure()
    draw_rectangle([0,0], [0,domain], [domain,domain], [domain,0])
    # New position and status
    for i in range(0,r.shape[0]):
        ccolor = color_status(status[i])
        #if i < len(color_vec):
        #    ccolor = color_vec[i]
        draw_circle([r[i,0],r[i,1]], R_eq2person, ccolor = ccolor)
    plt.title('t = ' + str(t))
    plt.xlim(-domain*0.05, domain * 1.05)
    plt.ylim(-domain*0.05, domain * 1.05)
    plt.savefig(filename)
    plt.close()
    return 0

def color_status(cstatus):
    if cstatus == 0: # not infected
        ccolor = 'g'
    elif cstatus == 1: #infected
        ccolor = 'r'
    elif cstatus == 2: #cured
        ccolor = 'b'
    elif cstatus == 3: #dead
        ccolor = 'k'
    elif cstatus == 4: # infected without simptoms
        ccolor = 'orange'
    return ccolor

def plot_histogram(t_vec, count_noninfected, count_infected, count_cured, count_dead, output_filename):
    
    def sum_vecs(v1,v2):
        v3 = []
        for i in range(0,len(v1)):
            v3.append(v1[i]+v2[i])
        return v3
    
    fig, ax = plt.subplots()
    plt.fill_between(t_vec, 0, sum_vecs(count_dead,sum_vecs(count_cured,sum_vecs(count_infected,count_noninfected))), 
                     color = color_status(3), label = 'Dead')
    plt.fill_between(t_vec, 0, sum_vecs(count_cured,sum_vecs(count_infected,count_noninfected)), color = color_status(2),
                     label = 'Cured')
    plt.fill_between(t_vec, 0, sum_vecs(count_infected,count_noninfected), color = color_status(1), label = 'Infected')
    plt.fill_between(t_vec, 0, count_noninfected, color = color_status(0), label = 'Non-Infected')
    plt.xlim(0,t_vec[-1])
    plt.ylim(0,count_cured[0] + count_infected[0] + count_noninfected[0])
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of people')
    plt.savefig(output_filename)
    plt.close()
    return 0

def plot_R_evolution(t, R,output_filename ):
    fig, ax = plt.subplots()
    plt.plot(t,R, 'r')
    
    plt.xlim(0,t[-1])
    plt.ylim(0, max(R)*1.25)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('R')
    plt.savefig(output_filename)
    plt.close()
    return 0
    
    

    
    
    
    
    
    
    
    
    
    
    