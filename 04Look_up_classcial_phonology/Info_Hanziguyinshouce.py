#!/usr/bin/env python
#-*-coding:utf-8-*-

'''
已完工。
版本：v1.0
時間：2017/3/18
地點：北京大學65樓
作者：Li Linfang
功能：此程序用以輸出《漢字古音手冊》的相關信息
運行環境：python 2.7.6 + ubuntu 14.04
'''

import csv
data_path = './Res/Hanziguyinshouce_sineFirstLastLine.txt' #儲存漢字古音手冊txt文檔的路徑

num_char = 0 #統計全部字頭數目
num_line = 0




all_str = ''.decode('utf-8') #字符串，用以儲存全部的字頭。爲unicode格式。
with open(data_path, 'rb') as csvf:
    contents = csv.reader(csvf, delimiter = '\t') #文檔的分隔標誌爲tab鍵
    for row in contents:
        num_char = num_char + len(row[5].decode('utf-8'))
        num_line = num_line + 1
        all_str = all_str + row[5].decode('utf-8')

#all_str = '我們要好好學習，天天向上。'.decode('utf-8')
char_array = []
def parse_char(x, char_array):
    for char in char_array:
        if char['char'] == x:
            char['num'] = char['num'] + 1
            return 'plus'
    char_segment = {'char': x, 'num': 1}
    char_array.append(char_segment)
    return 'add'

for char in all_str:
    parse_char(char, char_array)

char_array = sorted(char_array, key = lambda k: k['num'], reverse = True)

with open("./Info_char1.txt", "wb") as f:
    for char in char_array:
        f.write(char['char'].encode('utf-8')+': '+str(char['num'])+'\n')

num_polyphone = 0 #多音字數量
amount_polyphone = 0 #多音字總數（所有多音字出現的情況加起來）
num_monophone = 0 #單音字數量
for char in char_array:
    if char['num'] > 1:
        num_polyphone = num_polyphone + 1
        amount_polyphone = amount_polyphone + char['num']
    elif char['num'] == 1:
        num_monophone = num_monophone + 1

print '《手冊》收錄共%d個古代漢字（含重）。%d個古代漢字（去重）。 ' %(num_char, len(char_array))
print '《手冊》中有%d個多音字，其總數量爲%d。有%d個單音字。'%(num_polyphone, amount_polyphone, num_monophone)
print '《手冊》共列了%d行。' %num_line

'''
#all_str = '我我我我我'.decode('utf-8')

#原用以計算《手冊》所收單字數量（去重）。基本方法如下：
#1.遍歷字符串，去除重字： 重字之前的字符串+重字之後的字符串。
#2.在字符串末尾補0，保持字符串長度不變。
#3.遍歷結束後，去除字符串末尾的0.
#原用以呈現《手冊》所收多音字，及其個數。

duoyinzi = []
def add_duoyin(x, duoyin_array):
    for duoyin in duoyin_array:
        if duoyin['char'] == x:
            duoyin['num'] = duoyin['num'] + 1
            return 'plus'

    duoyin_segment = {'char': x, 'num': 2} #因爲相同時是從兩個字開始，所以從2加起
    duoyin_array.append(duoyin_segment)
    return 'add'

for i in range(0, len(all_str)):
    for j in range(i+1, len(all_str)):
        while all_str[i] != '0'.decode('utf-8') and all_str[j] != '0'.decode('utf-8') and all_str[i] == all_str[j]:
        #【注意】這裏必須用while,不可以用if，否則像‘我我我’這樣的字符串無法正確處理！！！
            add_duoyin(all_str[i], duoyinzi)
            temp_b = all_str[0:j]
            temp_a = all_str[j+1:len(all_str)]
            all_str = temp_b + temp_a + '0'.decode('utf-8')

all_str = all_str.rstrip('0')

#print all_str
print len(all_str) #結果12709.四分多鐘

with open("./Info.txt", "wb") as f:
    for duoyinzi_segment in duoyinzi:
        f.write(duoyinzi_segment['char'].encode('utf-8')+': '+str(duoyinzi_segment['num'])+'\n')

with open('./Info_all_str.txt', 'wb') as f:
    for ch in all_str:
        f.write(ch.encode('utf-8')+'\n')
###
'''
