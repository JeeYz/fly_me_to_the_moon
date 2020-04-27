import os

path_00 = '/home/jy/다운로드'
path_01 = 'C:/Users/jkdsp/OneDrive/Desktop/논문/SRL'

json_file_list = list()

def search(dirname):
	for (path, dir, files) in os.walk(dirname):
		# print(path)
		for filename in files:
			ext = os.path.splitext(filename)[-1]
			if ext == '.json':
				json_file_list.append(path + '/' + filename)
search(path_01)
for i in json_file_list:
	print(i)
