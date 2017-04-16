#!/usr/bin/env python
#-*-coding:utf-8-*-

import csv

from_file = "./Texts/Zuozhuan_Xianyun_Revised_utf8.txt"
to_file = "./Texts/Output(Zuozhuan).txt"
#from_file = './Input.txt'
#to_file = './Output.txt'
data_path = "./Res/Hanziguyinshouce.txt"
punctuation = '，。！？：；…—（）《》〈〉“”‘’’ 　\n'#注意這裏有個半角空格和全角空格，還有一個回車換行符

def del_enclitcs(str_x): #用以刪去字符串中的*%^等符號：把這些符號全部變成空格，堆到字符串最右邊，最後一起刪掉
    str_x = str_x.decode('utf-8')
    enclitics = '%*^'.decode('utf-8') #存儲要刪去的符號
    for i in range(0, len(str_x)):
        while str_x[i] in enclitics: #刪除符號：符號前的部分+符號後的部分+空格
            temp_b = str_x[0:i]
            temp_a = str_x[i+1:len(str_x)]
            str_x = temp_b + temp_a + ' '.decode('utf-8')
    str_x = str_x.strip() #刪去末尾空格
    return str_x.encode('utf-8')

def txt_in_brackets(str_x, x): #用以將str_x中x之後【】當中的字符抽出
    result = ''.decode('utf-8')
    str_x = str_x.decode('utf-8')
    x = x.decode('utf-8')
    for i in range(0, len(str_x)):
        if str_x[i] == '【'.decode('utf-8') and str_x[i-1] == x:
            while str_x[i] != '】'.decode('utf-8') and i < len(str_x)-1: #以防漏打】而出錯
                result = result + str_x[i]
                i = i + 1
            result = result + '】'.decode('utf-8') #把右邊的括號加上，更美觀些
    result = result.encode('utf-8')
    return result

def write_format(row, x): #參數：獲取的原數據庫的一行(row)，及所要查的單字(x)
    '''
    此函數規定了寫入文檔的格式。
    '''
    s_write = ''
    tab_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14] #在以上信息【之後】有個tab，即劃入不同的列中
    omit_list = [5] #該列內容不顯示
    brackets_list = [6] #有【要處理的列，該列後亦加\t
    for i in range(0, len(row)):
        if i in omit_list: #處理要求不顯示的列
            pass
        #elif row[i] == '': #處理數據爲空的列：不顯示——現在則是空內容末亦有\t
            #pass
        elif i in brackets_list:
            s_write = s_write + txt_in_brackets(del_enclitcs(row[i]), x) + '\t'
        elif i in tab_list:
            s_write = s_write + row[i] + '\t'
        else:
            s_write = s_write + row[i] + ' '
    return s_write

def look_up(x, file_path): #參數：輸入單字，數據路徑
    '''
    此函數用來在文檔中搜尋數據，並以一定格式輸出。（參考write_format()）輸出結果爲一個數組。
    '''
    result = [] #存儲查詢的字符串的最終結果
    with open(file_path, 'r') as csvf:
        contents = csv.reader(csvf, delimiter = '\t') #文檔的分隔標誌爲tab鍵
        for row in contents: #對文件的每一行進行循環
            if x == '': #輸入爲空時，什麼也不做。（否則會遍歷整個文檔）
                break
            elif x in punctuation:
                break
            elif x in row[5]: #row[5]是“檢索字頭”一欄
                result.append(write_format(row, x)) #可能會有多音字
        if result == []: #循環完所有的行後沒有查到。若是break的情況，則在write2txt中調整輸出格式。
            result.append('沒有結果。')
    return result

# TODO: 目前\t數不一致的行都用\t補齊了。不過已發現\t數不一致的行也是能正確導入excel的。那麼，\t數不一致的行能夠正確被csv操作嗎？
def write2txt(lookedup_array, input_path, x): #參數：已查到的內容，輸出文檔路徑，所要查的字
    '''
    將查得的內容輸出到文件內。
    '''
    result = 0 #返回執行狀態
    input_content = ''
    with open(input_path, 'a') as f:
        for i in range(0, len(lookedup_array)): #因爲可能有多音字，故用for循環
            if x in ' 　': #空格：直接忽略
                pass
                result = 2
            elif x == '\n': #換行：補足tab後直接輸出
                f.write('\t' * 15 + '\n') #'\t'補足規則：每一行都有15個\t，行末是\n
                result = 3
            elif x in punctuation: #標點：補足tab後直接輸出
                input_content = x + '\t' * 15 + '\n'
                f.write(input_content)
                result = 4
            elif lookedup_array[i] == '沒有結果。':
                input_content = x + '\t' + '沒有結果。' + '\t' * 14 + '\n'
                f.write(input_content)
                result = 0 #表示沒有結果
            elif i < 1: #單音字
                input_content = x + '\t' + lookedup_array[i] + '\n'
                f.write(input_content)
                result = 1
            else: #多音字
                input_content = '〖' + x + str(i+1) + '〗\t' + lookedup_array[i] + '\n'
                f.write(input_content)
                result = 2
    return result

if __name__ == '__main__':
    #print look_up('。', data_path)
    #'''
    num_no_result = 0 #“沒有結果”的計數器
    status_write2txt = 0 #記錄write2txt()函數執行的狀態
    with open(from_file, 'r') as f:
        while 1:
            line = unicode(f.readline(),'utf-8')
            if not line: #讀到行尾，結束讀取
                break
            for x in line:
                x = x.encode('utf-8')
                status_write2txt = write2txt(look_up(x, data_path), to_file, x)
                if status_write2txt == 0:
                    num_no_result += 1

    print "共有%d個字沒有查到。" %num_no_result
    #'''
'''
目前程序的做法爲：讀一個字，寫入一個字。
可以考慮改爲：全部讀取，在內存中標記，再全部寫入。
這樣可能會快一些，並對硬盤的操作少一些。
'''
