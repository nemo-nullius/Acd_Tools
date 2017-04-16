import re

def read_input_file(from_file_path):
    '''
    此函數用以讀入欲比较之文件。將文件所有內容存爲【字符串】。
    '''
    result = ''
    with open(from_file_path, 'r', encoding = 'utf-8') as f:
        result = f.read() #讀入文檔的全部內容並存爲字符串
    return result

fileA = "./Maoshi(Wiki)_Trimmed"
fileB = "./Maoshi01(GJK)_Trimmed"

if __name__ == '__main__':
    Str1 = read_input_file(fileA)
    pattern = r'(^.*章，章.*句。\n)|(^.*章，章.*句。故言.*章，章.*句。\n)'
