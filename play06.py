# @Author: J.Y.
# @Date:   2019-12-11T03:11:07+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-12-11T03:16:38+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz

f1 = 'd:/Program_Data/raw_train_dataset_25.train'
f2 = 'd:/Program_Data/raw_train_dataset_29.train'

with open(f1, 'r', encoding='utf-8') as fr, open(f2, 'w', encoding='utf-8') as fw:
    n = 0
    while True:
        line = fr.readline()
        if not line:break
        line = line.split()
        if line == []:
            n += 1
            fw.write('\n')
            continue
        if line[2] == 'ROOT':
            continue
        fw.write('\t'.join(line))
        fw.write('\n')

        # if n == 100:
        #     break







## endl
