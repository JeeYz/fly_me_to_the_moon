# -*- coding: utf-8 -*-

file0 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_train_x0.txt"
file1 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_train_y0.txt"
file2 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_raw_data_index.txt"


with open(file0, 'r', encoding='utf-8') as f0,\
open(file1, 'r', encoding='utf-8') as f1,\
open(file2, 'a', encoding='utf-8') as f2:
    while True:
        line0, line1 = f0.readline(), f1.readline()
        if not line0:break
        line0, line1 = line0.split(), line1.split()
        
        line0.append(line1[0])
        
        f2.write('  '.join(line0))
        f2.write('\n')





