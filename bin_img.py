from scipy import ndimage, misc
import numpy as np
import os
import cv2


outPath="C:\\Users\\hunte\\git\\puzzle-batch\\bin_deg270\\."
path="C:\\Users\\hunte\\git\\puzzle-batch\\deg270\\."

# iterate through the names of contents of the folder
for image_path in os.listdir(path):

    # create the full input path and read the file
    input_path = os.path.join(path, image_path)
    image_to_bin = cv2.imread(input_path,0)
    #binned = cv2.medianBlur(image_to_bin,3)
    binned = cv2.adaptiveThreshold(image_to_bin , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,5,2)
    binned = cv2.bitwise_not(binned,binned)

    # create full output path, 'example.jpg' 
    # becomes 'rotate_example.jpg', save the file to disk
    fullpath = os.path.join(outPath, 'bin'+image_path)
    #print(fullpath)
    cv2.imwrite(fullpath, binned)


print("done.")