import regex

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

fileA = "./Maoshi(Wiki)_Trimmed"
fileB = "./Maoshi01(GJK)_Trimmed"

if __name__ == "__main__":
    Str1 = read_input_file_to_list(fileA)
    Str2 = read_input_file(fileB)
    for paragraph in Str1:
        if paragraph != '':
            pattern = '('+ paragraph.replace('\n', '') +')' + r'{s<=' + str(len(paragraph)//5) + '}'
            print ('O++++'+paragraph)
            #print (pattern)
            compiled_pattern = regex.compile(pattern)
            result = compiled_pattern.match(Str2)
            if result:
                print (result.group(1))
            else:
                print ('*****')
