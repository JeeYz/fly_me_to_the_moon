g = '"id":'
a = '"morp":'
b = '"word":'
c = '"SRL":'

word_dict = list()
word_dict_pos = list()

switch = 0
while True:
    line = f.readline()
    if not line:break
    line = line.split()

    if line[0] == '"id":' and switch == 0:
        switch = 1
        group_0_word = list()
        group_1_morp = list()
        group_2_word_morp_pos = list()
        group_3_srl = list()
        continue

    if switch == 1:
        if line[0] == a:
            switch = 2
        elif line[0] == b:
            switch = 3
        elif line[0] == c:
            switch = 4
        continue


    if switch == 2:
        group_1_morp.append([line[4][1:-2], line[6][1:-2]])
    elif switch == 3:
        group_0_word.append([line[4][1:-2], line[8][:-1], line[10])
    elif switch == 4:
        if line[5] == '"sense":':
            group_3_srl.append([line[2][:-1], line[4][1:-2], line[6][:-1]])
        else:
            group_3_srl.append([line[2][-1], line[4][1:-2], line[6][1:-2]])


    if line[0] == '],':
        switch == 1
    elif line[0] == '},':
        switch = 0




















##endl
