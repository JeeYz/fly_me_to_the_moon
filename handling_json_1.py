import json

file1 = '/home/jy/NLP/SRL/E2016.788.04_Q_01.json'

with open(file1, 'r', encoding='utf-8') as j1:
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
		a_srl_line = list()
		a_line = list()
		for j in all_words[i['word_id']]:
			a_line.append(j)
		a_line.append('verb')
		a_srl_line.append(a_line)
		
		for arg in i['argument']:
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


print(text)
print(' '.join(new_mline))
for i in all_srl_line:
	for j in i:
		print(j)










