# @Author: J.Y.
# @Date:   2019-12-10T17:42:06+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-12-10T18:57:46+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz

f1 = 'd:/Program_Data/raw_train_dataset_24.train'
f2 = 'd:/Program_Data/raw_train_dataset_28.train'

# f1 = 'd:/Program_Data/raw_test_dataset_09.test'
# f2 = 'd:/Program_Data/raw_test_dataset_11.test'

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
        if int(line[0]) == 0:
            continue
        fw.write('\t'.join(line))
        fw.write('\n')

        # if n == 100:
        #     break











## endl
