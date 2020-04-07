from scipy import ndimage, misc
import numpy as np
import os
import cv2


outPath="C:\\Users\\hunte\\git\\puzzle-batch\\deg270\\."
path="C:\\Users\\hunte\\git\\puzzle-batch\\deg0\\."

# iterate through the names of contents of the folder
for image_path in os.listdir(path):

    # create the full input path and read the file
    input_path = os.path.join(path, image_path)
    image_to_rotate = cv2.imread(input_path)
    image_to_rotate = cv2.resize(image_to_rotate, (128,128), interpolation=cv2.INTER_AREA)

    # rotate the image
    rotated = cv2.rotate(image_to_rotate, cv2.ROTATE_180)

    # create full output path, 'example.jpg' 
    # becomes 'rotate_example.jpg', save the file to disk
    trunc_path = image_path[5:]
    fullpath = os.path.join(outPath, 'deg270_'+trunc_path)
    #print(fullpath)
    cv2.imwrite(fullpath, rotated)

print("done.")
