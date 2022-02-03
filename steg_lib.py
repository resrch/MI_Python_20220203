# binary.py

import matplotlib.pyplot as plt
import numpy as np
'''
library of functions used by main for
-   Converting message to binary message
-   Preparing RGB tiff images of uint8 format for message insertion
-   Inserting message into last bit of image bytes
-   Reassembling the coded image (with the hidden message)
-   Reading the hidden binary message within the coded image
-   Writing the message to a text file for the recipient to view.
'''

def convert(message): # converts message string to binary string
    string_message_length = len(message)
    binary_message = ''
    for letter in message:
        binary_letter = format(ord(letter),'08b')
        binary_message = binary_message + binary_letter
    return(binary_message, string_message_length)

def prepare_carrier_segment(image, binary_message, start_loc): 
    rows, cols, colors = image.shape
    im_size = rows*cols*colors
    image_vector = image.reshape(im_size) #turn image into 1D vector
    length_of_binary = len(binary_message)
    stop_loc = start_loc + length_of_binary
    carrier_segment = image_vector[start_loc:stop_loc] #extract the section of the 1D vectorized image
    return(image_vector, carrier_segment, length_of_binary, rows, cols, colors)

def insert_message(carrier_segment, binary_message, length_of_binary):
    # put binary message into carrier and return coded segment
    l = length_of_binary
    coded_image_segment = np.zeros(l, dtype='uint8')
    for x in range(0, l):
        image_element = format(carrier_segment[x],'08b')
        image_element_drop_right = image_element[0:-1]
        coded_element = image_element_drop_right+binary_message[x]
        coded_uint8 = int(coded_element,2)
        coded_image_segment[x] = coded_uint8
    return(coded_image_segment)

def insert_coded_segment(image_vector,coded_image_segment,start_loc):
    # insert the coded image segment into the 1D image vector
    coded_image_vector = image_vector.copy()
    l = len(coded_image_segment)
    for x in range(0, l):
        coded_image_vector[start_loc+x]=coded_image_segment[x]
    return(coded_image_vector)

def get_coded_image(coded_image_vector,rows,cols,colors):
    coded_image=coded_image_vector.reshape(rows,cols,colors)
    return(coded_image)

def get_coded_image_segment(coded_image,start_loc,message_length):
    l = 8*(message_length)
    coded_image_segment = np.zeros(l, dtype='uint8')
    rows, cols, colors = coded_image.shape
    im_size = rows*cols*colors
    coded_image_vector = coded_image.reshape(im_size)
    stop_loc = start_loc+l
    for x in range(0,l):
        coded_image_segment[x] = coded_image_vector[start_loc+x]
    return(coded_image_segment)

def extract_binary_message(coded_image_segment):
    l = len(coded_image_segment)
    binary_message = ''
    for x in range(0,l):
        coded_element = format(coded_image_segment[x],'08b')
        last_bit = coded_element[-1]
        binary_message = binary_message+last_bit
    return(binary_message)

def convert_back(binary_message):
    message = ''
    l = int((len(binary_message))/8)
    for i in range(1,l+1):
        binary_letter = binary_message[(i-1)*8:i*8]
        letter = chr(int(binary_letter,2))
        message = message + letter
    return(message)

