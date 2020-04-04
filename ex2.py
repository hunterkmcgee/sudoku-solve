import cv2
import numpy as np
import operator

CONST_IMAGE_PATH = "./test6.jpg"
CONST_COEFF = 0.02
originalImage = cv2.imread(CONST_IMAGE_PATH)
img = cv2.imread(CONST_IMAGE_PATH,0)
img = cv2.medianBlur(img,5)
img = cv2.adaptiveThreshold(img , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
img = cv2.bitwise_not(img,img)
print("thresholding the image")
cv2.imshow("Thresholded", img)
kernel = np.empty((3,3),'uint8')
kernel[0][0] = 0
kernel[0][1] = 1
kernel[0][2] = 0
kernel[1][0] = 1
kernel[1][1] = 1
kernel[1][2] = 1
kernel[2][0] = 0
kernel[2][1] = 1
kernel[2][2] = 0
dilated = cv2.dilate(img,kernel)
cv2.imshow("Dilated", dilated)
print("detecting the grid")

contours, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
polygon = contours[0]  # Largest image

print(polygon)

bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))

coords = [polygon[bottom_right][0], polygon[bottom_left][0], polygon[top_right][0], polygon[top_left][0]]
img2 = img.copy()

for coord in coords:
	img2 = cv2.circle(img2, tuple(int(x) for x in coord), 5, (255, 0, 0), -1)

cv2.imshow("SudokuPuzzle", originalImage)
cv2.imshow("dots", img2)
cv2.waitKey(0)