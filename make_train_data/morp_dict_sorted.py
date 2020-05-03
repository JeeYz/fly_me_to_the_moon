
file0 = '/home/jy/NLP/SRL/morp_dict.txt'
file1 = '/home/jy/NLP/SRL/morp_dict_sorted.txt'

all_morp_dict = list()
num = 0
with open(file0, 'r', encoding='utf-8') as fr, \
			 open(file1, 'a', encoding='utf-8') as fw:
	while True:
		line = fr.readline()
		if not line:break
		line = line.split()
		
		all_morp_dict.append(line[0])
	
	all_morp_dict = sorted(all_morp_dict)

	for i in all_morp_dict:	
		new_line = list()
		new_line.append(str(num))
		new_line.append(i)
		num += 1

		fw.write('\t\t'.join(new_line))
		fw.write('\n')

