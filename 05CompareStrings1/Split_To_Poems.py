import re

#读入要比较之文档之路径
file_inA = './Maoshi(Wiki)0'
file_inB = './Maoshi01(GJK)0'

file_toA_chapters = file_inA + '_Chapters' #诗篇名的存储路径
file_toB_chapters = file_inB + '_Chapters'

def read_input_file_to_list(from_file_path):
    '''
    此函數用以讀入欲比较之文件。將文件所有內容存为【数组】。
    '''
    result = ''
    with open(from_file_path, 'r', encoding = 'utf-8') as f:
        result = f.readlines() #讀入文檔的全部內容並存爲数组
    return result

def read_input_file(from_file_path):
    '''
    此函數用以讀入欲比较之文件。將文件所有內容存爲【字符串】。
    '''
    result = ''
    with open(from_file_path, 'r', encoding = 'utf-8') as f:
        result = f.read() #讀入文檔的全部內容並存爲字符串
    return result

def write_into_file(to_file_path, s):
    with open(to_file_path, 'w', encoding = 'utf-8') as f:
        f.write(s)

def pattern_position_in_list(l, p):
    '''
    l: list 存储文章每行内容的list
    p: 用以比较的pattern
    本函数以list的形式，返回每一个符合该pattern的字符串在list中的位置。
    '''
    result = []
    for i in range(0, len(l)):
        #print (l[i])
        mat = re.match(p, l[i])
        if mat:
            #print(l[i])
            result.append(i)
    return result

if __name__ == '__main__':
    contentA = read_input_file_to_list(file_inA) #读入文件，并将内容存为list
    contentB = read_input_file_to_list(file_inB)
    chpA_pos = pattern_position_in_list(contentA, r'(^《.*章，.*章.*\n)|(^《.*一章，.*句。\n)')
    chpB_pos = pattern_position_in_list(contentB, r'(^.{0,5}章.*?句.*?\n)|(昊天有成命一章七句\n)')
    #存储要写入的chapters的内容
    chpsA = ''
    chpsB = ''
    for i in range(0, len(chpA_pos)):
        chpsA = chpsA + str(i+1) + ' ' + ' ' + str(chpA_pos[i]) + ' ' + contentA[chpA_pos[i]] # 后面不需要再 + '\n' 用以换行，因为list的每一字符串末已有换行标识。

    for i in range(0, len(chpB_pos)):
        chpsB = chpsB + str(i+1) + ' ' + ' ' + str(chpB_pos[i]) + ' ' + contentB[chpB_pos[i]]

    write_into_file(file_toA_chapters, chpsA)
    write_into_file(file_toB_chapters, chpsB)

    index_low = 0
    file_poems_A_root = './A_Splitted_Wiki/'

    for i in range(0, len(chpA_pos)):
        index_high = chpA_pos[i]
        str_poem = ''.join(contentA[index_low:index_high+1])
        file_poems_A = file_poems_A_root + str(i+1)
        write_into_file(file_poems_A, str_poem)
        index_low = index_high + 1

    index_low = 0
    file_poems_B_root = './B_Splitted_GJK/'
    for i in range(0, len(chpB_pos)):
        index_high = chpB_pos[i]
        str_poem = ''.join(contentB[index_low:index_high+1])
        file_poems_B = file_poems_B_root + str(i+1)
        write_into_file(file_poems_B, str_poem)
        index_low = index_high + 1
