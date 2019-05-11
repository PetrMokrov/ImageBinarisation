from PIL import Image
import numpy as np
import os
import time
import pandas as pd
from tabulate import tabulate

# this function returns the binarized image, using adaptive tresholding technique
def adaptive_treshold(in_image, width, height):
    t = 15
    s = width // 8
    int_img = np.zeros((width, height), dtype = int)
    out_image = np.zeros((width, height), dtype = int)

    for w in range(width):
        sum = 0
        for h in range(height):
            sum = sum + in_image[w, h]
            if w == 0:
                int_img[w, h] = sum
            else:
                int_img[w, h] = int_img[w - 1, h] + sum
    

    for w in range(width):
        for h in range(height):
            # sliding box bounds selection
            x_1 = w - s // 2 if w - s // 2 > 0 else 0
            x_2 = w + s // 2 if w + s // 2 < width else width - 1
            y_1 = h - s // 2 if h - s // 2 > 0 else 0
            y_2 = h + s // 2 if h + s // 2 < height else height - 1
            count = (x_2 - x_1 + 1) * (y_2 - y_1 + 1)
            x_2_y_2_comp = int_img[x_2, y_2]
            x_2_y_1_comp = int_img[x_2, y_1 - 1] if y_1 > 0 else 0
            x_1_y_2_comp = int_img[x_1 - 1, y_2] if x_1 > 0 else 0
            x_1_y_1_comp = int_img[x_1 - 1, y_1 - 1] if x_1 > 0 and y_1 > 0 else 0
            sum = x_2_y_2_comp - x_2_y_1_comp - x_1_y_2_comp + x_1_y_1_comp
            if in_image[w, h] * count  <= sum * (100 - t) / 100:
                out_image[w, h] = 0
            else:
                out_image[w, h] = 255
    
    return out_image

        
def load_image( infilename ) :
    img = Image.open(infilename).convert("L")
    img.load()
    data = np.asarray( img, dtype="int32" )
    return data

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "L" )
    img.save( outfilename )

def input_folder_preprocessing(input_folder):
    if(not os.path.isdir(input_folder)):
        raise RuntimeError("no input folder")

def output_folder_preprocessing(output_folder):
    if(not os.path.isdir(output_folder)):
        try:
            os.mkdir(output_folder)
        except OSError:
            raise RuntimeError("error when creation output folder")

# input and output folders
input_folder = "./raw"
output_folder = "./binarized"

# folders preprocessings
input_folder_preprocessing(input_folder)
output_folder_preprocessing(output_folder)

# dataframe creation for time fixing
times = pd.DataFrame(columns=("name", "pixels", "time"))

for file in os.listdir(input_folder):
    in_file_name = input_folder + "/" + file

    im_matrix = load_image(in_file_name)
    width, height = im_matrix.shape
    st_time = time.clock()
    out_matrix = adaptive_treshold(im_matrix, width, height)
    time_elapsed = time.clock() - st_time

    times.loc[-1] = [file, width*height, time_elapsed]  # adding a row
    times.index = times.index + 1  # shifting index


    out_file_name = output_folder + "/bin_" + file
    save_image(out_matrix, out_file_name)

with open("times.md", 'w') as f:
    f.write(tabulate(times, tablefmt="pipe", headers="keys"))
