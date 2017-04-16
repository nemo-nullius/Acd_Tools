'''
本程序用以删除比较后且已删疏后的《经典释文》的内容。
《经典释文》可以以以下pattern表示：○.*?）
但由于○符号亦会在某些诗句前出现，会导致误删，以该程序解决。
思路：
检索每一行，若出现○且○到“）”之间无“（”则可删。即将○到“）”替换为一个“）”。
将删除的内容另存为一个文件。
'''
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

def del_Shiwen(content):
    #有以下三种可能：
    #A. ○……）……    【是】
    #B. ○……（……）  【非】
    #C. ○……       【非】
    #cont_l = list(contents) #将字符串转为list
    cont_seg = content.split('○')
    s_del = '' #记录被删去的内容
    result_str = '' #返回处理后的结果（删去经典释文的结果）
    num_del = 0 #记录被删的次数（即本content中有多少释文被删）
    #Bool_mark = False #记录每一个cont_seg中左括号之前是否出现了右括号或○号。
    for num in range(1, len(cont_seg)): #被split('○')后，cont_seg[0]在之前的串中肯定没有○，所以不要考察。若○为行首，则（1）此类行很少。（2）split('○')的结果是cont_seg[0]为一个空字符串。
        s = cont_seg[num]
        for i in range(0, len(s)):
            if s[i] == '（':
                #Bool_mark = True
                break #遇到（，说明这之后不是经典释文，可以结束了。
            if s[i] == '）': #and Bool_mark == False: #找到了《经典释文》，即可能A
                num_del += 1
                if num_del == 1:
                    s_del = '\n' + content + str(num_del) + '\t○' + s[0:i] + '\n'
                else:
                    s_del = s_del + str(num_del) + '\t○' + s[0:i] + '\n'
                cont_seg[num] = s[i:len(s)] #删去从○到右括号之前的字符
                break #跳出本次for循环。即，《经典释文》在每个○后只会出现一次。后面不要再找了。
        #Bool_mark = False

    result_str = ''.join(cont_seg[:])
    return result_str, s_del


file_in = './0Work/Maoshi(Wiki).Compared.Trimmed.DelShu'
file_out = file_in + '.DelShiwen'
file_out_delcontent = './0Work/Shiwen_deleted'

if __name__ == "__main__":
    #contents = input('> ')
    #print (del_Shiwen(contents))
    result = '' #处理后的结果
    deleted = '' #被删去的内容
    result_per = ''
    deleted_per = ''
    contents = read_input_file_to_list(file_in)
    for paragraph in contents:
        result_per, deleted_per = del_Shiwen(paragraph)
        result = result + result_per
        deleted = deleted + deleted_per
    write_into_file(file_out, result)
    write_into_file(file_out_delcontent, deleted)
