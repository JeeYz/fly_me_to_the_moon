
# position : C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/

# wd_file = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/word_dict_sorted.txt"
file0 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_1.txt"
file1 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_2_only_SRLexam_word.txt"


# with open(file0, 'r', encoding='utf-8') as f:
#     while True:
#         line = f.readline()
#         if not line:break
#         line = line.split()
        
#         print(line)



num = 0

with open(file0, 'r', encoding='utf-8') as fr,\
    open(file1, 'a', encoding='utf-8') as fw:
        
    switch = 0
    while True:
        line = fr.readline()
        if not line: break
        line = line.split()
        
        if line[0] == '___SRL' and line[1] == 'START___':
            switch = 1
            num += 1
            continue
        
        if line[0] == '___SRL' and line[1] == 'END___':
            switch = 0
            fw.write('\n')
            continue                
        
        if switch == 1:
            new_line = list()
            new_line.append(line[0])
            new_line.append(line[1])
            new_line.append(line[-1])
            
            fw.write('\t\t'.join(new_line))
            fw.write('\n')
                
            
print(num)

          




