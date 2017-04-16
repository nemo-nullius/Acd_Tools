'''
说明：本程序用以将compared并且合并后的文件中的各种无效的对比去除。
主要是：将(，)这样的东西变成，本身。
'''
punctuation = '。，：《》〈〉·「」—…\n“”？！、（）『』； '#其中有个半角空格

file_from = "./Maoshi(Wiki).Compared"
file_to = './Maoshi(Wiki).Compared.Trimmed'

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

def trim_str(s, punct):
    '''
    s: 所要处理的字符串。
    punct: 所要处理掉的符号。格式为：(punct)
    '''
    for p in punct:
        to_be_replaced = '('+p+')'
        s = s.replace(to_be_replaced, p)
    return s

if __name__ == "__main__":
    write_into_file(file_to, trim_str(read_input_file(file_from), punctuation))
