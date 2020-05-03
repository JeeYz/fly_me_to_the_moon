import os

file01 = 'E2014.119_A_01.json'
file02 = 'result.txt'
file03 = 'result_1.txt'
new_filename = './' + file01
new_w_file_0 = './' + file02
new_w_file_1 = './' + file03

with open(new_filename, 'r', encoding='utf-8') as f1, \
		 open(new_w_file_0, 'a', encoding='utf-8') as f2,\
		 open(new_w_file_1, 'a', encoding='utf-8') as f3:
	switch = 0
	one_sent = list()
	while True:
		line = f1.readline()
		if not line:break
		line = line.split()
		if line == []:continue
#		print(line)
#		if line == []:
#			print(line)
	
		if '"text"' == line[0]:
			line[2] = line[2][1:]
			line[-1] = line[-1][:-2]
			if line[2] == '':
				del line[2]
			print(line[2:])
			new_line = list()
			new_line = ' '.join(line[2:])
			f3.write(new_line)
			f3.write('\n')
			continue

		if '"morp"' in line and switch == 0:
#			print(line)
			switch = 1
			one_sent = list()
			continue
		
		if ']' in line[0] and len(line) == 1 and switch == 1:
#			print(one_sent)
			new_sent = ' '.join(one_sent)
			print(new_sent)
			f2.write(new_sent)
			f2.write('\n')
			switch = 0

		if switch == 1:
#			print(line)
			one_sent.append(line[5][1:-2])
