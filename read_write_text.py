def read_text():
	f = open('annotation.txt','r')
	result = {} # dict
	for line in f.readlines():           
		line = line.strip()
		name = line.split(" ")[0]
		num = line.split(" ")[1]
		result[name] = num
	# range in chronological order in dict
	# 100 images
	f.close()
	return result

def write_text(result):
	f = open('prediction.txt','a')
	for i in range(len(result)):
		f.write(result[i]['name']+' ')
		f.write(result[i]['21']+' ')
		f.write(result[i]['7']+'\n')
	f.close()