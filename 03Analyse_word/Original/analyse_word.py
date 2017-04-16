#-*-coding:utf-8-*-

biaodian0 = unicode('，。？……!——：；、  ','utf-8') #……与——各占两个unicode
biaodian_shu_b = unicode('《〈', 'utf-8')
biaodian_shu_a = unicode('》〉', 'utf-8')
biaodian_yin_b = unicode('“‘', 'utf-8')
biaodian_yin_a = unicode('”’', 'utf-8')

char_before_str = ''
char_after_str = ''

def char_before_check(content_list, i):
    global char_before_str
    if i == 0:
        char_before_str = ''
        return 'Head'
    elif content_list[i-1] in biaodian0:
        char_before_str = ''
        return 'Head'
    elif content_list[i-1] in biaodian_shu_b:
        char_before_str = char_before_str + content_list[i-1]
        return char_before_check(content_list, i-1) # 前书名号递归
    elif content_list[i-1] in biaodian_yin_b:
        char_before_str = char_before_str + content_list[i-1]
        return char_before_check(content_list, i-1) # 前引号递归
    elif content_list[i-1] in biaodian_shu_a:
        char_before_str = char_before_str + content_list[i-1]
        return char_before_check(content_list, i-1) # 后书名号递归
    elif content_list[i-1] in biaodian_yin_a:
        char_before_str = char_before_str + content_list[i-1]
        return char_before_check(content_list, i-1) # 后引号递归
    else:
        result = char_before_str + content_list[i-1]
        result = result[::-1] #倒序：步长为-1
        char_before_str = ''
        return result

def char_after_check(content_list, i):
    global char_after_str
    if i == len(content_list)-1:
        char_after_str = ''
        return 'End'
    elif content_list[i+1] in biaodian0:
        char_after_str = ''
        return 'End'
    elif content_list[i+1] in biaodian_shu_b:
        char_after_str = char_after_str + content_list[i+1]
        return char_after_check(content_list, i+1) # 后书名号递归
    elif content_list[i+1] in biaodian_yin_b:
        char_after_str = char_after_str + content_list[i+1]
        return char_after_check(content_list, i+1) # 后引号递归
    elif content_list[i+1] in biaodian_shu_a:
        char_after_str = char_after_str + content_list[i+1]
        return char_after_check(content_list, i+1) # 后书名号递归
    elif content_list[i+1] in biaodian_yin_a:
        char_after_str = char_after_str + content_list[i+1]
        return char_after_check(content_list, i+1) # 后引号递归
    else:
        result = char_after_str + content_list[i+1]
        char_after_str = ''
        return result

def add_char(char_list, u_str): #注意：存储的每一个char信息是utf-8
    single_char_dic = {} #存放每一个字的信息
    for i in char_list:
        if i['char'] == u_str:
            i['num'] = i['num'] + 1
            return 'plus'

    single_char_dic = {'char': u_str, 'num': 1}
    char_list.append(single_char_dic)
    return 'add'

x = raw_input('Please input a character to be analysed > ')
#x = '曰'
char_before = []
char_after = []
content_list = []

with open('./Texts/Zuozhuan_Xianyun_Revised_utf8.txt',"r") as f:
    while 1:
        line = unicode(f.readline(),'utf-8')
        #line = f.readline()
        #讀到行尾，結束讀取
        if not line:
            break

        content_list.append(line)
'''
print content_list[0]
print len(content_list)
print len(content_list[0])
print content_list[0][0]
'''
for i in range(0, len(content_list)): #遍历文档的每一行
    for j in range(0, len(content_list[i])): #遍历文档的每一行的每一字
        if content_list[i][j] == x.decode('utf-8'):
            print 'b '+char_before_check(content_list[i], j)
            print 'a '+char_after_check(content_list[i], j)
            print add_char(char_before, char_before_check(content_list[i], j))
            print add_char(char_after, char_after_check(content_list[i], j))

'''
for i in char_before:
    print 'char '+i['char']+', '+'num: '+str(i['num'])

print '-'*20

for i in char_after:
    print 'char '+i['char']+', '+'num: '+str(i['num'])

print '='*20
'''
#据num值从大到小排序
char_before = sorted(char_before, key = lambda k: k['num'], reverse = True)
char_after = sorted(char_after, key = lambda k: k['num'], reverse = True)

for i in char_before:
    print 'char: '+i['char']+', '+'num: '+str(i['num'])

print '-'*20

for i in char_after:
    print 'char: '+i['char']+', '+'num: '+str(i['num'])
