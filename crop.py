import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image

def crop(filename):
	#	img:gray scale
	img = cv2.imread("train_data/"+filename)
	#	crop the white part on the right side away
	crop_img = img[:,:1000]
	#	canny edge detection
	#	get rid of small white points and lines using blurring
	blur = cv2.GaussianBlur(crop_img,(9,9),0)
	canny = cv2.Canny(blur,150,300)
	#	thresholding
	(_, thresh) = cv2.threshold(canny, 140, 255, cv2.THRESH_BINARY) 
	#	hough line detection
	height, width = thresh.shape[:2] 
	lines = cv2.HoughLinesP(thresh,1,np.pi/180,130,minLineLength=10,maxLineGap=50)
	lines1 = lines[:,0,:]

	right = down = -1
	left = up = 2000
	average = 0

	for x1,y1,x2,y2 in lines1[:]:
		cv2.line(thresh,(x1,y1),(x2,y2),(255,255,255),3)
		average += (x1+x2)/2
		if (y1+y2)/2 > down:
			down = (y1+y2)/2
		if (y1+y2)/2 < up:
			up = (y1+y2)/2
		if (x1+x2)/2 > right:
			right = (x1+x2)/2
		if (x1+x2)/2 < left:
			left = (x1+x2)/2
	average /= lines1.shape[0]

	#plt.imshow(thresh)
	#plt.show()

	#	cv2.line needs int parameter
	left = int(left)
	right = int(right)
	up = int(up)
	down = int(down)

	#	crop and rotation
	crop = img[up:down,left:right]
	if average < (left + right)/2:
		rotate = np.rot90(crop)
	else:
		rotate = np.rot90(crop)
		rotate = np.rot90(rotate)
		rotate = np.rot90(rotate)
	rotate = rotate.copy()
	return rotate
