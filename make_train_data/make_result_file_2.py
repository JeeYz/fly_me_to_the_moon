
import os
import json

path_00 = '/home/jy/NLP/SRL/'
path_01 = 'C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/'

file02 = 'result_1.txt'

new_filename = path_00 + file02

json_file_list = list()

def search(dirname):
    for (path, dir, files) in os.walk(dirname):
        # print(path)
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.json':
                json_file_list.append(path + '/' + filename)
search(path_00)

#print(json_file_list[0])

for jf in json_file_list:
	with open(jf, 'r', encoding='utf-8') as j1,\
		open(new_filename, 'a', encoding='utf-8') as fw:
		json_data = json.load(j1)
		sent = json_data['sentence']

#	print(sent)
#	print(sent[0])

#	print(sent[1]['text'])
#	print(sent[0]['word'])
#	print(sent[0]['morp'])
#	print(sent[0]['SRL'])
	
		text = sent[0]['text']
# print(text)
		morp = sent[0]['morp']
		word = sent[0]['word']
		srl = sent[0]['SRL']

#	for i in srl:
#		print(i)

		new_mline = list()

		for i in morp:
			new_mline.append(i['lemma'])
	
		all_words = list()
		for i in word:
			new_word_line = list()
			new_word_line.append(str(i['id']))
			new_word_line.append(i['text'])
			for j in range(i['begin'], i['end']+1):
				new_word_line.append(new_mline[j])
			all_words.append(new_word_line)
	
		all_srl_line = list()
		for i in srl:
#			a_srl_line = list()
#			print(i)
			for arg in i['argument']:
				a_srl_line = list()
				a_line = list()
				for j in all_words[i['word_id']]:
					a_line.append(j)
				a_line.append('verb')
				a_srl_line.append(a_line)
				for index, rest_word in enumerate(all_words):
					a_line = list()
					if arg['word_id'] == index:
						for k in all_words[index]:
							a_line.append(k)
						a_line.append(arg['type'])
						a_srl_line.append(a_line)
					else:
						for k in all_words[index]:
							a_line.append(k)
						a_line.append('-')
						a_srl_line.append(a_line)
	
				all_srl_line.append(a_srl_line)

## print result

		fw.write('___Sentence START___')
		fw.write('\n')
		fw.write(text)
		fw.write('\n')
		fw.write(' '.join(new_mline))
		fw.write('\n')
		for i in all_srl_line:
			fw.write('___SRL START___')
			fw.write('\n')
#			print('i : ', i)
			for j in i:
				fw.write('\t\t'.join(j))
				fw.write('\n')
			fw.write('___SRL END___')
			fw.write('\n')
		fw.write('___Sentence END___')
		fw.write('\n')









	
