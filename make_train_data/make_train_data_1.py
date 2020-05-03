# -*- coding: utf-8 -*-

label_file = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_label.txt"
wd_file = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/word_dict_sorted.txt"
file1 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_2_only_SRLexam_word_modification.txt"
# file2 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_3_index_of_result_2.txt"
# file3 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_4_label_num.txt"
file4 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_5_temporary_result.txt"

# word_dict = dict()
MAX_word_num = 51

# with open(wd_file, 'r', encoding='utf-8') as f:
#     while True:
#         line = f.readline()
#         if not line:break
#         line = line.split()
        
#         word_dict[line[1]] = int(line[0])
        
# # print(word_dict)


with open(file1, 'r', encoding='utf-8') as f1,\
    open(file4, 'a', encoding='utf-8')as f2:
    switch = 0
    num = 0
    while True:
        line = f1.readline()
        if not line:break
        line = line.split()
        
        if len(line) == 3:
            if line[2] == 'verb' and switch == 0:
               num += 1
               switch = 1
               verb_0 = line[1]
               sent_0 = list()
               label_word = str()
               continue
        
        if switch == 1 and len(line) == 3:
            if line[2] == '-' or line[2] == 'AUX':
                sent_0.append(line[1])
            else:
                sent_0.append(line[1])
                label_word = line[1]
                label_tag = line[2]
            continue
        
        
        if line == []:
            
            line_0 = list()
            
            for i in range(MAX_word_num):
                if len(sent_0) > i:
                    line_0.append(sent_0[i])
                else:
                    line_0.append('PADPAD_##')
            
            line_0.append(label_word)
            line_0.append(verb_0)
            line_0.append(label_tag)
            
            f2.write('  '.join(line_0))
            f2.write('\n')
            
            switch = 0
            continue




