file0 = '/home/jy/NLP/SRL/word_dict.txt'
file1 = '/home/jy/NLP/SRL/word_dict_sorted.txt'

all_word_dict = list()
num = 0
with open(file0, 'r', encoding='utf-8') as fr, \
			 open(file1, 'a', encoding='utf-8') as fw:
	while True:
		line = fr.readline()
		if not line:break
		line = line.split()
		
		all_word_dict.append(line[0])
	
	all_word_dict = sorted(all_word_dict)

	for i in all_word_dict:	
		new_line = list()
		new_line.append(str(num))
		new_line.append(i)
		num += 1

		fw.write('\t\t'.join(new_line))
		fw.write('\n')

