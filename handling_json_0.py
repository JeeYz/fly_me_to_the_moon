import json

file0 = 'C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/001.언어분석 통합 말뭉치/말뭉치/E2016.788.01_A_01.json'

file1 = '/home/jy/NLP/SRL/E2016.788.04_Q_01.json'

with open(file1, 'r', encoding='utf-8') as j1:
    json_data = json.load(j1)
    sent = json_data['sentence']

    # print(sent[0]['text'])
    # print(sent[0]['morp'])
    # print(sent[0]['word'])
    # print(sent[0]['SRL'])
    print(sent)
    text = sent[0]['text']
    # print(text)

    morp = sent[0]['morp']
    word = sent[0]['word']
    srl = sent[0]['SRL']

    # for i in morp:
    #     print(i)
    #
    # for i in word:
    #     print(i)

    # for i in srl:
    #     print(i)

    new_morp_line = list()

    for i in morp:
        new_morp_line.append(i['lemma'])

    all_words = list()
    for i in word:
        new_word_line = list()
        new_word_line.append(str(i['id']))
        new_word_line.append(i['text'])
        for j in range(i['begin'], i['end']+1):
            new_word_line.append(new_morp_line[j])
        all_words.append(new_word_line)

    # print(srl)

    all_srl = list()
    for i in srl:
        one_srl = list()
        new_srl_line = list()
        new_srl_line.append(i['word_id'])
        new_srl_line.append(i['verb'])
        new_srl_line.append('verb')
        one_srl.append(new_srl_line)
        for j in i['argument']:
            new_srl_line = list()
            new_srl_line.append(j['word_id'])
            new_srl_line.append(j['text'])
            new_srl_line.append(j['type'])
            one_srl.append(new_srl_line)
        all_srl.append(one_srl)

    ## print result

    print(text)
    print(' '.join(new_morp_line))
    for i in all_words:
        print(i)
    for i in all_srl:
        for j in i:
            print(j)

















## endl
