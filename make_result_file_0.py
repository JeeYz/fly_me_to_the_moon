import os

path_00 = '/home/jy/다운로드'
path_01 = 'C:/Users/jkdsp/OneDrive/Desktop/논문/SRL'

file02 = 'result_0.txt'
file03 = 'result_word.txt'
file04 = 'result_morp.txt'
file05 = 'result_word_morp.txt'

new_filename = path_01 + '/' + file02

json_file_list = list()

def search(dirname):
	for (path, dir, files) in os.walk(dirname):
		# print(path)
		for filename in files:
			ext = os.path.splitext(filename)[-1]
			if ext == '.json':
				json_file_list.append(path + '/' + filename)
search(path_01)
# for i in json_file_list:
# 	print(i)


g = '"id":'
a = '"morp":'
b = '"word":'
c = '"SRL":'

all_dict = dict()

for i in json_file_list:
	with open(i, 'r', encoding='utf-8') as f1, \
	open(new_filename, 'a', encoding='utf-8') as f2:
		switch = 0
		while True:
			line = f1.readline()
			if not line:break
			line = line.split()
			print(line)
			print(i)
			if line == []:
				switch = 0
				continue
			if line[0] == '],':
				switch = 1
				continue
			elif line[0] == '},':
				if switch == 5 or switch == 0:
					switch = 0
				else:
					f2.write('###sentence###')
					f2.write('\n')

					word_line = list()
					for j in group_0_word:
						word_line.append(j[0])

					f2.write(' '.join(word_line))
					f2.write('\n')

					morp_line = list()
					for j in group_1_morp:
						morp_line.append(j[0])

					f2.write(' '.join(morp_line))
					f2.write('\n')

					for j,k in enumerate(group_0_word):
						new_line_0 = list()
						new_line_0.append(str(j))
						new_line_0.append(k[0])

						dict_el = list()
						# print(line)
						# print(group_0_word)
						# print(group_1_morp)
						# print(group_3_srl)
						for l in range(int(k[1]), int(k[2])+1):
							# print(l)
							new_line_0.append(group_1_morp[l][0])
							dict_el.append(group_1_morp[l][0])
							new_line_0.append(group_1_morp[l][1])
						f2.write('\t\t'.join(new_line_0))
						f2.write('\n')
						# print(switch)
						# print(k)
						# print(group_0_word)
						# print(group_1_morp)
						# print(dict_el)
						all_dict[k[0]] = dict_el

					for j in group_3_srl:
						new_line_1 = list()
						# print(j)
						if j[2] == 'verb':
							f2.write('###SRL###')
							f2.write('\n')
							new_line_1.append(j[0])
							new_line_1.append(j[1])
							new_line_1.append('verb')
						else:
							new_line_1.append(j[0])
							new_line_1.append(j[1])
							new_line_1.append(j[2])
						f2.write('\t\t'.join(new_line_1))
						f2.write('\n')

					f2.write('###END_SENT###')
					f2.write('\n')

					switch = 0
					continue

			if line[0] == '"id":' and switch == 0:
				# print('hello, world')
				switch = 1
				group_0_word = list()
				group_1_morp = list()
				group_2_word_morp_pos = list()
				group_3_srl = list()
				continue


			if switch == 1:
				# print(line)
				if line[0] == a:
					switch = 2
				elif line[0] == b:
					switch = 3
				elif line[0] == c:
					if line[-1] == '[],':
						switch = 5
					else:
						switch = 4
				continue


			if switch == 2:
				# print(line)
				group_1_morp.append([line[4][1:-2], line[6][1:-2]])
			elif switch == 3:
				# print(line)
				# print(i)
				group_0_word.append([line[4][1:-2], line[8][:-1], line[10]])
			elif switch == 4:
				if line[5] == '"sense":':
					group_3_srl.append([line[2][:-1], line[4][1:-2], line[3][1:-2]])
				else:
					group_3_srl.append([line[2][:-1], line[4][1:-2], line[6][1:-2]])




file_name_1 = path_01 + '/' + file05
file_name_2 = path_01 + '/' + file03
file_name_3 = path_01 + '/' + file04

words_list = sorted(all_dict.keys())
morps_list = sorted(all_dict.values())
all_dict = dict(sorted(all_dict.items()))

with open(file_name_1, 'a', encoding='utf-8') as f1:
	for i in all_dict:
		line_1 = list()
		line_1.append(i)
		for j in all_dict[i]:
			line_1.append(j)
		f1.write('\t'.join(line_1))
		f1.write('\n')

with open(file_name_2, 'a', encoding='utf-8') as f2:
	for i in words_list:
		f2.write(i)
		f2.wirte('\n')

with open(file_name_3, 'a', encoding='utf-8') as f3:
	for i in morps_list:
		f3.write(i)
		f3.wirte('\n')










##endl
