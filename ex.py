import cv2
import numpy as np
import math

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

    kernel = np.empty((3,3),'uint8')
    kernel[0][0] = 0
    kernel[0][1] = 1
    kernel[0][2] = 0
    kernel[1][0] = 1
    kernel[1][1] = 0
    kernel[1][2] = 1
    kernel[2][0] = 0
    kernel[2][1] = 1
    kernel[2][2] = 0
    dilated = cv2.dilate(img,kernel)

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

    cv2.drawContours(originalImage, [screenCnt], -1, (0,255,0), 3)
    corners = np.float32(screenCnt)


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


    cv2.imshow('Region',warp_img)

    
    # CELL SEGMENTATION
    for i in range(9):
        x_aoi = math.ceil(i*(x/9))# + 0.5*(x/9)
        for j in range(9):
            y_aoi = math.ceil(j*(y/9))# + 0.5*(y/9)
            #print(int(y_aoi), int(x_aoi))
            cell = warp_img[y_aoi:y_aoi+math.ceil(y/9), x_aoi:x_aoi+math.ceil(x/9)]
            cell = cv2.resize(cell, (28,28),interpolation=cv2.INTER_AREA)
            print(cell.shape)   #PRINT FOR CELL SIZE
            if (j == 2):       #ONLY PRINT CELLS FROM CERTAIN ROW or COL 
                cv2.imshow('cell'+str(i), cell)    # display cell
            
    cv2.waitKey(0)
#'''

## Inspired by this github repo (link below)
## https://github.com/tusharsircar95/SudokuVisionSolver

extract("./img/4.jpg")