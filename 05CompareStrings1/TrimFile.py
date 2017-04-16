#-*-encoding:utf-8-*-=
import unicodedata
import sys

tbl = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))

def remove_punctuation(text): return text.translate(tbl)

def read_input_file(from_file_path):
    '''
    此函數用以讀入文件。將文件所有內容存爲字符串。
    '''
    result = ''
    with open(from_file_path, 'r', encoding = 'utf-8') as f:
        result = f.read() #讀入文檔的全部內容並存爲字符串
    return result

def write_into_file(to_file_path, s):
    with open(to_file_path, 'w', encoding = 'utf-8') as f:
        f.write(s)


#读入要比较之文档之路径
file_inA = './Maoshi(Wiki)0'
#file_inB = './Maoshi01(GJK)'

file_toA = file_inA + '_Trimmed' #比较结果存储路径
#file_toB = file_inB + '_Trimmed'

if __name__ == '__main__':
    write_into_file(file_toA, remove_punctuation(read_input_file(file_inA)))
    #write_into_file(file_toB, remove_punctuation(read_input_file(file_inB)))
