# -*- coding: utf-8 -*-

label_file = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/SRL_label.txt"
wd_file = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/word_dict_sorted.txt"
# file1 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_2_only_SRLexam_word.txt"
file2 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_3_index_of_result_5.txt"
file3 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_4_label_num.txt"
file4 = "C:/Users/jkdsp/OneDrive/Desktop/논문/SRL/result_5_temporary_result.txt"

MAX_lines_num = 9378 - 240 - 93
MAX_words_num = 54

def check_lines():
    num = 0
    fail_sent = list()
    with open(file4, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:break
            line = line.split()
            
            if len(line) != MAX_words_num:
                fail_sent.append(line)
            
            num += 1
            
            
    if MAX_lines_num == num and len(fail_sent) == 0:
        print('%d sentences are loading. loading complete!!' % num)
        
    else:
        f_sent = ' '.join(fail_sent)
        print(f_sent)
        print('Generated files had been failed...')
        

def make_word_dict():
    word_dict = dict()

    
    with open(wd_file, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:break
            line = line.split()
            
            word_dict[line[1]] = int(line[0])
            
    return word_dict


def make_label_tag_dict():
    result = dict()
    
    with open(label_file, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:break
            line = line.split()
            
            result[line[1]] = int(line[0])
    
    return result



def make_result_3_4_file(word_dict, label_tag_dict):
    with open(file4, 'r', encoding='utf-8') as fr,\
    open(file2, 'a', encoding='utf-8') as fw1,\
    open(file3, 'a', encoding='utf-8') as fw2:
        
        while True:
            line = fr.readline()
            if not line:break
            line = line.split()
            
            new_line = list()
            for wrd in line[:-1]:
                new_line.append(str(word_dict[wrd]))
            
            fw1.write('  '.join(new_line))
            fw1.write('\n')
            
            fw2.write(str(label_tag_dict[line[-1]]))
            fw2.write('\n')
            
    return
    



def main():
    
    check_lines()
    
    word_dict = make_word_dict()
    label_tag_dict = make_label_tag_dict()
    make_result_3_4_file(word_dict, label_tag_dict)
    
    
    
    
    
    


if __name__ == '__main__':
    
    
    main()
