# We want to use pydicom to convert a list of images from the input folder and store them in the output 
# we also want to convert them to nii.gz images 
# additionally it would be nice if the input images disregard weird data structures and create a .txt for each batch in order to store what was converted 

# for users it would be nice to see a progress bar?

# to avoid clumping in the output folder, the loop should create a new folder for each batch with date and time of conversion 

import pydicom 

data_folder = "input_data/open_batches"


