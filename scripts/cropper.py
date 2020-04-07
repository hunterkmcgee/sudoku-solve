# Extract the area containing sudoku puzzle from given image
import cv2
import numpy as np


cv2.namedWindow("preprocess", cv2.WINDOW_NORMAL * 2)
cv2.namedWindow("lines", cv2.WINDOW_NORMAL * 2)
img_path = "./test3.jpg"

img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.medianBlur(gray, 5)
adapt_type = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
thresh_type = cv2.THRESH_BINARY_INV
bin_img = cv2.adaptiveThreshold(blur, 255, adapt_type, thresh_type, 11, 2)

edges = cv2.Canny(bin_img, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 180)
cv2.imshow("preprocess", bin_img)

for line in lines:
    rho,theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho

    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * a)

    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * a)
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)




cv2.imshow('lines', img)
k = cv2.waitKey(0)
cv2.destroyAllWindows()