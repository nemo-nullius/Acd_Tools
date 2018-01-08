#!/usr/bin/env python
#-*-coding:utf-8-*-

import csv
import sys

#from_file = "./Texts/Zuozhuan_Xianyun_Revised_utf8.txt"
#to_file = "./Texts/Output(Zuozhuan)_Q.txt"
#from_file = './Input.txt'
#to_file = './Output_Q.txt'
data_path = "./Res/Hanziguyinshouce.txt"
punctuation = '，。！？：；…—（）《》〈〉“”‘’’ 　\n'#注意這裏有個半角空格和全角空格，還有一個回車換行符

def read_database(database_path):
    '''
    此函數用以將所有《手冊》資料從文件中讀入，並以一定格式作爲list輸出。
    '''
    result = []
    with open(database_path, 'r') as csvf:
        contents = csv.reader(csvf, delimiter = '\t')
        for row in contents: #對文件的每一行進行循環。row本身會返回一個數組。
            result.append(row)
    return result

def read_input_file(from_file_path):
    '''
    此函數用以讀入欲標注古音之文件。將文件所有內容存爲字符串。
    '''
    result = ''
    with open(from_file_path, 'r') as f:
        result = f.read() #讀入文檔的全部內容並存爲字符串
    return result

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

def output(row, x): #參數：所找到的一行數據，所查的字
    '''
    對於所查到的單行內容，此函數控制其顯示方式。
    '''
    result = ''
    tab_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14] #在以上信息【之後】有個tab，即劃入不同的列中
    omit_list = [5] #該列內容不顯示
    brackets_list = [6] #有【要處理的列，該列後亦加\t
    for i in range(0, len(row)):
        if i in omit_list: #處理要求不顯示的列
            pass
        #elif row[i] == '': #處理數據爲空的列：不顯示——現在則是空內容末亦有\t
            #pass
        elif i in brackets_list:
            result = result + txt_in_brackets(del_enclitcs(row[i]), x) + '\t'
        elif i in tab_list:
            result = result + row[i] + '\t'
        else:
            result = result + row[i] + ' '
    return result

def look_up_from_list(x, data_list):
    '''
    此函數用來在指定的上古音list中查詢上古音。結果以list輸出。
    '''
    result = [] #存儲查詢的字符串的最終結果
    for data in data_list: #對《手冊》數據的每一行進行循環
        if x == '': #輸入爲空時，什麼也不做。（否則會遍歷整個文檔）
            break
        elif x in punctuation:
            break
        elif x in data[5]: #row[5]是“檢索字頭”一欄
            result.append(output(data, x)) #可能會有多音字
    if result == []: #循環完所有的行後沒有查到。若是break的情況，則在write2txt中調整輸出格式。
        result.append('沒有結果。')
    return result

def output_format(lookedup_array, x): #參數：已查到的內容，輸出文檔路徑，所要查的字
    '''
    將查得的單字內容以一定格式輸出。
    '''
    status = 0 #返回執行狀態
    result = ''
    #先是沒有結果的情況
    if x in ' 　': #空格：直接忽略
        pass
        status = 3
    elif x == '\n': #換行：補足tab後直接輸出
        result = '\t' * 15 + '\n' #'\t'補足規則：每一行都有15個\t，行末是\n
        status = 4
    elif x in punctuation: #標點：補足tab後直接輸出
        result = x + '\t' * 15 + '\n'
        status = 5
    elif lookedup_array[0] == '沒有結果。':
        result = x + '\t' + '沒有結果。' + '\t' * 14 + '\n'
        status = 0 #表示沒有結果
    else: #有結果的情況
        for i in range(0, len(lookedup_array)): #因爲可能有多音字，故用for循環
            if i < 1: #單音字
                result = x + '\t' + lookedup_array[i] + '\n'
                status = 1
            else: #多音字
                result = result + '〖' + x + str(i+1) + '〗\t' + lookedup_array[i] + '\n' #與前一程序不同，此處不再是一行行輸入文件了。所以前面的【result+】萬萬不可少！
                status = 2
    return result, status

def output_all(str_x):
    '''
    此函數查詢全部的字符串，並以一定的格式輸出結果。結果爲字符串。
    '''
    result = ''
    status = 0#用以記錄單字檢字的結果
    data_list = read_database(data_path)
    result_x = ''#用以記錄每一所查單字的結果
    i_no_result = 0 #記錄“沒有結果”的數量
    for x in str_x.decode('utf-8'): #對字符串中的每一個單字進行查衣裝
        x = x.encode('utf-8')
        result_x, status = output_format(look_up_from_list(x, data_list), x)
        if status == 0:
            i_no_result += 1
        result = result + result_x
    return result, i_no_result

if __name__ == "__main__":
    from_file = sys.argv[1]
    fileNameInfo = from_file.split('.')
    fileName = '.'.join(fileNameInfo[0:-1])
    fileClass = fileNameInfo[-1]
    to_file = ''.join((fileName, '_Result','.',fileClass))

    result = ''
    i_no_result = 0
    with open(to_file, 'w') as f:
        result, i_no_result = output_all(read_input_file(from_file))
        f.write(result)
    print "共有%d個字沒有查到。" %i_no_result
