# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:17:38 2022

@author: Mario Gayete Ibáñez
"""

import cv2
import os

def video_generation_from_images(output_filename, input_folder, N_images, At):
    img_array = []
    for i_file in range(0,N_images):
        img = cv2.imread(input_folder + str(i_file) + '.jpg')
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    
    out = cv2.VideoWriter(output_filename,cv2.VideoWriter_fourcc(*'DIVX'), 1/At, size)
     
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    
    return 0
