# -*- coding: utf-8 -*-


file0 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_2_only_SRLexam_word.txt"
file1 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_2_only_SRLexam_word_modification.txt"


num = 0
with open(file0, 'r', encoding='utf-8') as fr,\
open(file1, 'a', encoding='utf-8') as fw:
    switch = 0
    while True:
        line = fr.readline()
        if not line:break
        line = line.split()

        if len(line) == 3:
            if line[2] == 'verb' and switch == 0:
               switch = 1
               a_sent = list()
               verb_line = line
               continue
         
        if switch == 1 and line != []:
            a_sent.append(line)
            continue
        
        if line == []:
            
            for i in a_sent:
               if i[2] == 'AUX' or i[2] == 'ARGM-ADV' :
                   switch = 2
            
            if switch == 2:
                switch = 0
            else:
                fw.write('\t\t'.join(verb_line))
                fw.write('\n')
                for i in a_sent:
                    fw.write('\t\t'.join(i))
                    fw.write('\n')
                num += 1
                switch = 0
                fw.write('\n')
        
        
print(num)