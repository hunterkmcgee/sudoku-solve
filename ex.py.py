import os
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import tensorflow as tf
from keras.models import load_model
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

## This program loads an image containing a sudoku puzzle
## and applies pre-processing and hough transforms
## to detect the contours (borders) of the puzzle.
## It then draws a green line around the puzzle.
def extract(image_path):

    CONST_IMAGE_PATH = image_path
    CONST_COEFF = 0.02
    originalImage = cv2.imread(CONST_IMAGE_PATH)
    
    # PREPROCESSING IMAGE
    img = cv2.imread(CONST_IMAGE_PATH,0)
    img = cv2.medianBlur(img,3)
    img = cv2.adaptiveThreshold(img , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    img = cv2.bitwise_not(img,img)
    
    # GENERATE CONTOURS
    (contours, _) = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea , reverse = True)
    screenCnt = None

    # FIND BIGGEST RECTANGLE CONTOUR
    maxPerimeter=300
    count=0
    for contour in contours:
        perimeter = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour, CONST_COEFF*perimeter , True)
        if len(approx) == 4: 
            if perimeter > maxPerimeter: 
                maxPerimeter = perimeter
                screenCnt = approx
        exit

    # DRAW GREEN BOX AROUND PUZZLE
    cv2.imshow('original',originalImage)
    cv2.drawContours(originalImage, [screenCnt], -1, (0,255,0), 3)
    corners = np.float32(screenCnt)
    cv2.imshow('detected',originalImage)


    # GET EXTREME VALUES OF REGION OF INTEREST (ROI)
    minX = maxX = screenCnt[0][0][0]
    minY = maxY = screenCnt[0][0][1]
    for j in range(0, 4):
        if screenCnt[j][0][0] > maxX:
            maxX = screenCnt[j][0][0]
        if screenCnt[j][0][0] < minX:
            minX = screenCnt[j][0][0]
        if screenCnt[j][0][1] > maxY:
            maxY = screenCnt[j][0][1]
        if screenCnt[j][0][1] > maxY:
            minY = screenCnt[j][0][1]


    # CROP REGION OF INTEREST
    x_range = maxX - minX
    y_range = maxY - minY

    roi_img = img.copy()
    roi_img = roi_img[0:y_range, 0:x_range] = img[minY:maxY, minX:maxX]

    result = corners.copy()
    result[:,:,0]-=minX
    result[:,:,1]-=minY
    result = np.squeeze(result)

    # PERSPECTIVE WARP
    y,x = roi_img.shape
    dst_points = np.float32([[0, 0], [0, y], [x,y], [x,0]])
    warp = cv2.getPerspectiveTransform(result, dst_points)
    warp_img = cv2.warpPerspective(roi_img,warp,(x,y))
    warp_img = cv2.resize(warp_img, (x,x), interpolation=cv2.INTER_AREA)


    cv2.imshow('Warped Region',warp_img)

    cells = []
    sums = []
    # CELL SEGMENTATION
    for i in range(9):
        x_aoi = math.ceil(i*(x/9))
        for j in range(9):
            y_aoi = math.ceil(j*(y/9))

            cell = warp_img[y_aoi:y_aoi+math.floor(y/9), x_aoi:x_aoi+math.floor(x/9)]
            cell = cv2.resize(cell, (28,28),interpolation=cv2.INTER_AREA)
            cell = cell.astype('float32')
            cell[0:2,:] = 0
            cell[-3:,:] = 0
            cell[:,0:2] = 0
            cell[:,-3:] = 0

            sum = np.sum(cell[11:-11,11:-11])
            sum /= 49
            sums.append(sum)
            cell = cell.astype('float32').reshape(cell.shape+(1,))
            cell /= 255

            cells.append(cell)
            
    cv2.imshow("cell", cells[40])
    cv2.waitKey(0)


    # FEED EACH CELL THRU CLASSIFIER MODEL
    model = load_model("./models/digit_class.h5")
    
    cells_array = np.asarray(cells)
    classes = model.predict_classes(cells_array)
    
    # REMOVE BLANK SQUARES
    for i in range(9):
        for j in range(9):
            if sums[j + i*9] < 2:
                classes[j + i*9] = 0
    
    print(classes)
    

#'''

## Inspired by this github repo (link below)
## https://github.com/tusharsircar95/SudokuVisionSolver

extract("./img/10.jpg")