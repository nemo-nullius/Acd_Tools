'''
本程序用以将一系列文件合成一个文件
'''

file_path_root = "./A_Splitted_Wiki_Com/"
file_to = './Maoshi(Wiki).Compared'

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

if __name__ == "__main__":
    contents = ''
    for i in range(0, 305):
        file_path = file_path_root + str(i+1)
        contents = contents + read_input_file(file_path)
    write_into_file(file_to, contents)
