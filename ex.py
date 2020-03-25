import cv2
import numpy as np
from PIL import Image

## This program loads an image containing a sudoku puzzle
## and applies pre-processing and hough transforms
## to detect the contours (borders) of the puzzle.
## It then draws a green line around the puzzle.

CONST_IMAGE_PATH = "./test_puzzle.jpg"
CONST_COEFF = 0.02
originalImage = cv2.imread(CONST_IMAGE_PATH)
img = cv2.imread(CONST_IMAGE_PATH,0)
img = cv2.medianBlur(img,3)
img = cv2.adaptiveThreshold(img , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
img = cv2.bitwise_not(img,img)
print("thresholding the image")
cv2.imshow("Thresholded", img)
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
cv2.imshow("Dilated", dilated)
print("detecting the grid")
(contours, _) = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key = cv2.contourArea , reverse = True)
screenCnt = None

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

#print(screenCnt)
#print(screenCnt[1][0][1])
#print(maxPerimeter)

cv2.drawContours(originalImage , [screenCnt], -1, (0,255,0), 3)
cv2.imshow("SudokuPuzzle", originalImage)
cv2.waitKey(0)

'''
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

x_range = maxX - minX
y_range = maxY - minY
puzzle_roi= originalImage[minX:maxX, minY: maxY]
roi_img = originalImage.copy()
roi_img[0:x_range, 0:y_range] = originalImage[minY:maxY, minX, maxX]

#print(roi_img)

#Image.fromarray(roi_img).save('roi1.jpg')
'''

## Inspired by this github repo (link below)
## https://github.com/tusharsircar95/SudokuVisionSolver
