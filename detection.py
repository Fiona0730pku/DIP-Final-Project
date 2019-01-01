import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image

def detection(image):
	#	image is already a numpy array passed from crop
	height, width = image.shape[:2] 

	#	do different thresholding for different purposes
	# 	thresh1: detect 7 numbers
	(_, thresh1) = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY) #7 numbers
	# 	thresh2: detect 21 numbers
	(_, thresh2) = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
	#plt.imshow(image)
	#plt.show()

	# detect 21 numbers

	#left
	flag = 0
	tmp = 0
	threshold = 0
	for i in range(50,500):
		tmp = 0
		for j in reversed(range(height-100,height-10)):
			if thresh2[j][i][0] == 0:
				tmp += 1
				if tmp >= 3:
					left = i-1
					flag = 1
					break
		if i > 53 and flag == 1:
			break
		elif flag == 1:	#最左侧在50更靠左 要变换范围
			for i in range(20,60):
				tmp = 0
				flag2 = 0
				for j in reversed(range(height-100,height-10)):
					if thresh2[j][i][0] == 0:
						tmp += 1
					if tmp >= 3:
						left = i-1
						flag2 = 1
						break
				if flag2 == 1:
					break
			if flag2 == 1:
					break

	#cv2.line(thresh2,(left,0),(left,height-1),(0,255,0),1)

	#down
	flag = 0
	value = 0
	threshold = 0
	for j in range(height-50,height):
		if j < threshold:
			continue
		#print(j)
		flag = 0
		for i in range(50,500):
			if thresh2[j][i][0] == 0:
				flag = 1
				break
		#print(j,flag,i)
		if j <= height-45 and flag == 0:
			threshold = height - 20
			continue
		if flag == 0:
			value = j
			break
	down = value
	#print(down)
	if down == 0:
		down = height - 1
 	#print(height)
	#print(down)
	#cv2.line(thresh2,(0,down),(width-1,down),(0,255,0),1)

	#up
	flag = 0
	value = 0
	for j in reversed(range(down-200,down-10)):
		flag = 0
		for i in range(50,500):
			if thresh2[j][i][0] == 0:
				flag = 1
				break
		if flag == 0:
			value = j
			break
	if value == 0:
		for j in reversed(range(down-200,down-10)):
			flag = 0
			for i in range(50,400):
				if thresh2[j][i][0] == 0:
					flag = 1
					break
			if flag == 0:
				value = j
				break
	up = value
	#cv2.line(thresh2,(0,up),(width-1,up),(0,255,0),1)

	#right
	#the most complicated of 4
	#using the prior information of up & down
	flag = 0
	value = 0
	count = 0
	tmp = 0
	right = 0
	for i in range(400,600):
		flag = 0
		tmp = 0
		for j in range(up,down):
			if thresh2[j][i][0] == 0:
				tmp += 1
				if tmp >= 3:
					flag = 1
					break		
		if flag != 0:
			count = 0
		else:
			count += 1
			if count >= 10:
				right = i-9
				break
	if right == 0: #紧贴底部且有倾斜的黑边不好处理 只能随机猜
		right = 500
	#cv2.line(thresh2,(left,0),(left,height-1),(0,255,0),1)
	#cv2.line(thresh2,(right,0),(right,height-1),(0,255,0),1)
	#cv2.line(thresh2,(0,down),(width-1,down),(0,255,0),1)
	#cv2.line(thresh2,(0,up),(width-1,up),(0,255,0),1)
	#print(left)
	#print(right)
	#plt.imshow(thresh2)
	plt.show()

	#crop1 = image[up:down,left:right]
	#cv2.rectangle(image,(left,up), (right,down), (0,0,255), 3)

	# detect 7 numbers

	#up
	flag = 0
	value = 0
	for j in reversed(range(10,70)):
		flag = 0
		for i in range(30,350):
			if thresh2[j][i][0] == 0:
				flag = 1
				#print((j,i))
				break
		if flag == 0:
			value = j
			break
	up_1 = value
	#print(up_1)

	#down
	flag = 0
	value = 0
	for j in range(up_1+20,up_1+100):
		flag = 0
		for i in range(30,350):
			if thresh2[j][i][0] == 0:
				flag = 1
				break
		if flag == 0:
			value = j
			break
	down_1 = value
	if down_1 == 0:
		down_1 = 100 #2018-5-22-20-7-5.bmp
	cv2.line(thresh1,(0,up_1),(width-1,up_1),(0,255,0),1)
	cv2.line(thresh1,(0,down_1),(width-1,down_1),(0,255,0),1)
	#print(down_1)

	#left
	flag = 0
	left_1 = 0
	for i in range(40,100):
		flag = 0
		for j in range(up_1,down_1):
			if thresh2[j][i][0] == 0:
				left_1 = i-1
				flag = 1
				break
		if flag == 1:
			break			
	cv2.line(thresh1,(left_1,0),(left_1,height-1),(0,255,0),1)
	#print(left_1)

	#right
	#the most complicated of 4
	#using the prior information of up & down
	flag = 0
	value = 0
	count = 0
	right_1 = 0
	for i in range(200,400):
		flag = 0
		noise = 0
		for j in range(up_1,down_1):
			if thresh2[j][i][0] == 0:
				noise += 1
				if noise >= 3:
					flag = 1
					break		
		if flag != 0:
			count = 0
		else:
			count += 1
			if count >= 30:
				right_1 = i-29
				break
	if right_1 == 0:
		right_1 = 400
	#print(right_1)
	#cv2.line(thresh1,(right_1,0),(right_1,height-1),(0,255,0),1)
	#plt.imshow(thresh1)
	#plt.show()

	#crop2 = thresh1[up_1:down_1,left_1:right_1]

	#pass back the coordinate instead of the detected image
	#print([up,down,left,right])
	#print([up_1,down_1,left_1,right_1])
	#plt.imshow(image)
	#plt.show()
	return [up,down,left,right],[up_1,down_1,left_1,right_1]
