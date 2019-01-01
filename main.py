import numpy as np
import cv2
import read_write_text
import crop
import detection
import segmentation
import fire
from matplotlib import pyplot as plt

def main():
	ticket = read_write_text.read_text()
	#ticket = {}
	#ticket ["2018-5-22-19-58-42.bmp"] = "65906300010424M039019"
	result = []
	result_element = {}
	for key in ticket:
		print(key)
		# crop image 
		img_rotate = crop.crop(key)

		# detection 21&7 numbers and mark their areas as rectangulars on cropped image
		[up,down,left,right],[up_1,down_1,left_1,right_1] = detection.detection(img_rotate)

		# segment each rectangular into single digits
		# identify each of the digits by putting them as a batch and pass into cnn
		result_21, seg_line_21= segmentation.segmentation(img_rotate[up:down,left:right], 21)
		result_7, seg_line_7= segmentation.segmentation(img_rotate[up_1:down_1,left_1:right_1], 7)

		# draw rectangle after segmentation
		# in case the red lines will affect segmentation
		cv2.rectangle(img_rotate,(left,up), (right,down), (0,0,255), 3)
		cv2.rectangle(img_rotate,(left_1,up_1), (right_1,down_1), (0,0,255), 3)
		for i in range(len(seg_line_21)):
			cv2.line(img_rotate,(left+seg_line_21[i],up),(left+seg_line_21[i],down),(0,0,255),1)
		for i in range(len(seg_line_7)):
			cv2.line(img_rotate,(left_1+seg_line_7[i],up_1),(left_1+seg_line_7[i],down_1),(0,0,255),1)
		cv2.imwrite('segments/'+key,img_rotate)
		str_21 = "".join(result_21)
		str_7 = "".join(result_7)
		result_element = {}
		result_element['name'] = key
		result_element['21'] = str_21
		result_element['7'] = str_7
		result.append(result_element)
		print(key,ticket[key],str_21,str_7)

	read_write_text.write_text(result)

if __name__ == '__main__':
  fire.Fire(main)