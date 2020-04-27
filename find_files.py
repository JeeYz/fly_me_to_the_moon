import os

json_file_list = list()

def search(dirname):
	for (path, dir, files) in os.walk(dirname):
		for filename in files:
			ext = os.path.splitext(filename)[-1]
			if ext == '.json':
				json_file_list.append(filename)	
search('/home/jy/다운로드')
print(json_file_list)
