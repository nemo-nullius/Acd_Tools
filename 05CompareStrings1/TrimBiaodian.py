from sys import argv


punctuation = '，。！？：；…—（）《》〈〉“”‘’’ 　\n\t【】〔〕［］○'#注意這裏有個半角空格和全角空格，還有一個回車換行符

def del_punctuation(str_x): #用以刪去字符串中的标点等符號：把這些符號全部變成空格，堆到字符串最右邊，最後一起刪掉
    '''
    for i in range(0, len(str_x)):
        while str_x[i] in punctuation: #刪除符號：符號前的部分+符號後的部分+空格
            temp_b = str_x[0:i]
            temp_a = str_x[i+1:len(str_x)]
            str_x = temp_b + temp_a + ' '
    str_x = str_x.strip() #刪去末尾空格
    '''
    for p in punctuation:
        str_x = str_x.replace(p, '')
    return str_x

def read_input_file(from_file_path):
    '''
    此函數用以讀入欲比较之文件。將文件所有內容存爲字符串。
    '''
    result = ''
    with open(from_file_path, 'r', encoding = 'utf-8') as f:
        result = f.read() #讀入文檔的全部內容並存爲字符串
    return result

def write_into_file(to_file_path, s):
    with open(to_file_path, 'w', encoding = 'utf-8') as f:
        f.write(s)

if __name__ == '__main__':

    script, input_file_path = argv

    to_file_path = input_file_path + '_Trimmed'

    s = read_input_file(input_file_path)
    s = del_punctuation(s)
    print (s)
    write_into_file(to_file_path, s)
