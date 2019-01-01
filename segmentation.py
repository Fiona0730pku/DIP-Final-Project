import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
import test_10
import test_62

def crop_piece(region):
	height,width = region.shape[:2]
	up = 0
	count = 0
	for i in reversed(range(0,(int)(height/2))):
		flag = 0
		for j in range(0,width):
			if region[i,j,0] == 0:
				flag = 1
				break
		if flag == 0:
			count = count + 1
		else:
			count = 0
		if count > 3:
			up = i+3
			break
	down = height - 1
	count = 0
	for i in range((int)(height/2),height):
			flag = 0
			for j in range(0,width):
				if region[i,j,0] == 0:
					flag = 1
					break
			if flag == 0:
				count = count + 1
			else:
				count = 0
			if count > 3:
				down = i-3
				break
	#plt.imshow(region)
	#print(height,width)
	#print(up,down)
	#plt.show()
	#pass back the coordinate instead of the detected image
	return [up,down]

def segmentation(region, numbers):
	thresh_value = 0
	if numbers == 7:
		thresh_value = 150
	elif numbers == 21:
		thresh_value = 50
	(_, thresh) = cv2.threshold(region, thresh_value, 255, cv2.THRESH_BINARY)
	kernel = np.ones((3,3),np.uint8)
	# white background and black character
	# erode is actullu dilate
	erode = cv2.erode(thresh,kernel,iterations = 1)
	dilate = cv2.dilate(erode,kernel,iterations = 1)

	#if numbers == 7:
		#plt.imshow(dilate)
		#plt.show()

	# 投影算法
	height, width = region.shape[:2]
	value = [0]*width
	#calculate horizontal pixels  
	tmp = 0   
	for y in range(0, width): 
		tmp = 0 
		for x in range(0, height): 
			if dilate[x,y,0] == 0:
				tmp += 1
		value[y] = tmp
	#segment according to horizontal pixels
	seg = [[0 for col in range(2)] for row in range(width)]
	inline = 1  
	start = 0  #record the starting point of every character
	j = 0  
	#print(value)
	for i in range(0,width):  
		if inline == 1 and value[i] >= 5 :  #从空白区进入文字区  
			start = i  #记录起始行分割点  
			#print (i)  
			inline = 0  
		elif value[i] < 5 and inline == 0 :  #从文字区进入空白区  
			inline = 1  
			seg[j][0] = start  #保存行分割位置  
			seg[j][1] = i  
			j = j + 1  
	seg[j][0] = start
	seg[j][1] = width-1

	result = []
	before = 0

	kernel2 = np.ones((2,2),np.uint8)

	seg_line = []
	if numbers == 7:
		for p in range(0,j+1):	
			if p != j:
				tmp = (int)((seg[p][1]+seg[p+1][0])/2)
				seg_line.append(tmp)
			else: tmp = (int)(seg[j][1]) 
			#print(before,tmp)
			[tmp_up, tmp_down] = crop_piece(thresh[:,before:tmp])
			final = thresh[:,before:tmp][tmp_up:tmp_down,:]	
			final = cv2.resize(final,(20,20))
			final = cv2.copyMakeBorder(final,4,4,4,4,cv2.BORDER_CONSTANT,value=[255,255,255]) 
			#final = cv2.erode(final,kernel2,iterations = 1)
			#plt.imshow(final)
			#plt.show()
			final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
			final = final.ravel()
			final = final[np.newaxis,:]
			if p == 0:
				# 7个字符中只有第1个是字母
				result_alphabet = test_62.test(final)
			elif p == 1:
				result = final
			else:
				result = np.concatenate((result, final), axis=0)
			before = tmp
		result_num = test_10.test(result)
		return result_alphabet + result_num, seg_line

	else: # numbers == 21
		for p in range(0,j+1):	
			if p != j:
				tmp = (int)((seg[p][1]+seg[p+1][0])/2)
				seg_line.append(tmp)
			else: tmp = (int)(seg[j][1]) 
			[tmp_up, tmp_down] = crop_piece(thresh[:,before:tmp])
			final = thresh[:,before:tmp][tmp_up:tmp_down,:]
			final = cv2.resize(final,(20,20))
			final = cv2.copyMakeBorder(final,4,4,4,4,cv2.BORDER_CONSTANT,value=[255,255,255]) 
			#final = cv2.erode(final,kernel2,iterations = 1)
			final = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
			final = final.ravel()
			final = final[np.newaxis,:]
			have_alphabet = 0
			if p == 0:
				result = final
			elif p != 14:
				result = np.concatenate((result, final), axis=0)
			else:
				result_alphabet = test_62.test(final)
				have_alphabet = 1
			before = tmp
		result_num = test_10.test(result)
		if have_alphabet == 1:
			result_num.insert(14,result_alphabet[0])
		return result_num, seg_line

