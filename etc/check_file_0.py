# -*- coding: utf-8 -*-

# file0 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_1.txt"
# file2 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_3_index_of_result_5.txt"
# file3 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_data_index.txt"
file3 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_data_index_1.txt"

max_num = 0
switch = 0

# with open(file0, 'r', encoding='utf-8') as f:
#     while True:
#         line = f.readline()
#         if not line:break
#         line = line.split()
        
#         if line[0] == '___Sentence' and line[1] == 'START___':
#             switch = 1
#             continue
        
#         if switch == 1:
#             t_num = len(line)
#             if t_num > max_num:
#                 max_num = t_num
#             switch = 0
#             continue
        

# print(max_num) # max number of line elements => 50

with open(file3, 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line:break
        line = line.split()
        
        if len(line) != 54:
            print(line)
        
        if '18805' not in line:
            print(line)





