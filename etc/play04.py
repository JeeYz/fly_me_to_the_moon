# @Author: J.Y.
# @Date:   2019-12-10T14:33:42+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-12-10T18:56:25+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz

f1 = 'd:/Program_Data/raw_train_dataset_24.train'
# f2 = 'd:/Program_Data/raw_train_dataset_26.train'
f2 = 'd:/Program_Data/raw_train_dataset_28.train'

with open(f1, 'r', encoding='utf-8') as fr, open(f2, 'w', encoding='utf-8') as fw:
    n = 0
    while True:
        line = fr.readline()
        if not line:break
        line = line.split()
        # print(line)
        if line == []:
            n += 1
            # fw.write('\n')
        fw.write('\t'.join(line))
        fw.write('\n')
        # if n == 100:
        #     break



## endl
