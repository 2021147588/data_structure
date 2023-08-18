"""
CSI2103: Data Structures
vision_utils.py
Instructor: Seong Jae Hwang

Utility functions for computer vision tasks.

DO NOT MODIFY
"""

import numpy as np
from scipy.signal import convolve2d
from PIL import Image

def energyImage(im):
    """ Computes the energy image which is the gradient magnitude
    based on a simple sobel filter. The resulting energy image
    contains the amount of image intensity change. This is used
    for identifying interesting (high image intensity change) and
    not-interesting (low image intensity change) areas.
    
    input:
        im: 2D image to compute the gradient magnitude
        
    output:
        energy_image: resulting gradient magnitude image
    """
    I = np.dot(im[...,:3], [0.2989, 0.5870, 0.1140])
    filter = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]])
    Ix = convolve2d(I, filter, mode='same')
    Iy = convolve2d(I, np.transpose(filter), mode='same')
    energy_image = np.sqrt(np.power(Ix, 2) + np.power(Iy, 2))
    
    return energy_image


def cumulativeMinimumEnergyMap(im):
    """ Computes the cumulative energy map given an energy image.
    This is computed by simply accumulating the energy it takes to 
    move to the next column. The resulting energy map M is used to
    find the "minimum energy path" (path along the least interesting
    region) of the image from right to left.
    
    input:
        im: 2D image to compute the cumulative energy map
        
    output:
        M: energy map of im based on its energy image
    """
    energy_image = energyImage(im)
    num_rows = energy_image.shape[0]
    num_cols = energy_image.shape[1]
    M = np.matrix(np.ones((num_rows,num_cols)) * np.NINF)
    M[:,0] = np.expand_dims(energy_image[:,0], axis=1)
    
    for j in range(1,num_cols):
        for i in range(num_rows):
            if i > 0:
                if i < num_rows-1:
                    M[i,j] = energy_image[i,j] + np.min(M[i-1:i+2, j-1])
                else:
                    M[i,j] = energy_image[i,j] + np.min(M[i-1:i+1, j-1])
            else:
                M[i,j] = energy_image[i,j] + np.min(M[i:i+2, j-1])
    return M


def contentUnawareResize(im, amount):
    """ Resize the image in a non-content-aware way using a built-in
    function. This is how typical image resizing works which simply
    shrinks all the image contents.
    
    input:
        im: image to resize
        amount: image height will be reduced by this amount
        
    output:
        reduced_image: the new image with the reduced height
    """
    image = Image.fromarray(np.uint8(im*255))
    reduced_image = np.array(image.resize((image.size[0], image.size[1]-amount)))
    return reduced_image