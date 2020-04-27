import os
import json

path_00 = '/home/jy/다운로드'
path_01 = 'C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/'

file02 = 'result_0.txt'
file03 = 'word_dict.txt'
file04 = 'morp_dict.txt'
file05 = 'word_morp_dict.txt'

new_filename = path_01 + file02

json_file_list = list()

def search(dirname):
    for (path, dir, files) in os.walk(dirname):
        # print(path)
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.json':
                json_file_list.append(path + '/' + filename)
search(path_01)

morp_dict = list()
word_dict = list()
word_morp_dict = dict()

for jf in json_file_list:
    with open(jf, 'r', encoding='utf-8') as j1, \
    open(new_filename, 'a', encoding='utf-8') as f2:
        print(jf)
        json_data = json.load(j1)
        sent = json_data['sentence']
        for a_sent in sent:
            # print(sent)
            # print(m)
            # print(jf)
            text = a_sent['text']
            morp = a_sent['morp']
            word = a_sent['word']
            srl = a_sent['SRL']

            new_morp_line = list()

            for i in morp:
                new_morp_line.append(i['lemma'])
                morp_dict.append(i['lemma'])

            all_words = list()
            for i in word:
                new_word_line = list()
                new_word_line.append(str(i['id']))
                new_word_line.append(i['text'])
                word_dict.append(i['text'])

                word_el = list()
                for j in range(i['begin'], i['end']+1):
                    new_word_line.append(new_morp_line[j])
                    word_el.append(new_morp_line[j])
                all_words.append(new_word_line)

                word_morp_dict[i['text']] = word_el

            # print(srl)

            all_srl = list()
            for i in srl:
                one_srl = list()
                new_srl_line = list()
                new_srl_line.append(str(i['word_id']))
                new_srl_line.append(i['verb'])
                new_srl_line.append('verb')
                one_srl.append(new_srl_line)
                for j in i['argument']:
                    new_srl_line = list()
                    new_srl_line.append(str(j['word_id']))
                    new_srl_line.append(j['text'])
                    new_srl_line.append(j['type'])
                    one_srl.append(new_srl_line)
                all_srl.append(one_srl)

            ## print result
            f2.write('## sentence start ##')
            f2.write('\n')
            f2.write(text)
            f2.write('\n')
            f2.write(' '.join(new_morp_line))
            f2.write('\n')
            for i in all_words:
                f2.write('\t\t'.join(i))
                f2.write('\n')
            f2.write('## sementic role labeling ##')
            f2.write('\n')
            for i in all_srl:
                for j in i:
                    f2.write('\t\t'.join(j))
                    f2.write('\n')
            f2.write('## sentence end ##')
            f2.write('\n')


morp_dict = list(set(morp_dict))
word_dict = list(set(word_dict))
word_morp_dict = dict(sorted(word_morp_dict.items()))

print(word_morp_dict)

file_name_1 = path_01 + file05
file_name_2 = path_01 + file03
file_name_3 = path_01 + file04


with open(file_name_1, 'a', encoding='utf-8') as f1:
    for i in word_morp_dict.keys():
        line_1 = list()
        line_1.append(i)
        for j in word_morp_dict[i]:
            for k in j:
                line_1.append(k)
        f1.write('\t'.join(line_1))
        f1.write('\n')

with open(file_name_2, 'a', encoding='utf-8') as f2:
    for i in word_dict:
        f2.write(i)
        f2.write('\n')

with open(file_name_3, 'a', encoding='utf-8') as f3:
    for i in morp_dict:
        f3.write(i)
        f3.write('\n')












##endl
