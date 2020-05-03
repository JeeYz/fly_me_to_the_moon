# -*- coding: utf-8 -*-

import random
random.seed(7)


file0 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_data_index.txt"
file1 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_train_data_index_0.txt"
file2 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_test_data_index_0.txt"

test_num = 1000

all_data = list()

with open(file0, 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line:break
        line = line.split()
        all_data.append(line)
        
random.shuffle(all_data)

with open(file1, 'a', encoding='utf-8') as f1,\
open(file2, 'a', encoding='utf-8') as f2:
    for n,line in enumerate(all_data):
        if n < test_num:
            f2.write('  '.join(line)+'\n')
        else:
            f1.write('  '.join(line)+'\n')
        

