#!/usr/bin/env python
#-*-coding:utf-8-*-

'''
已完工。
版本：v1.0
時間：2017/3/18
地點：北京大學65樓
作者：Li Linfang
功能：從生成好的《漢字古音手冊》txt表中（分隔符爲tab，字符爲utf-8），檢索每一字的條目。
    若所檢內容爲多個漢字，則一一檢索並輸出。
    若所檢字在表中沒有，則輸出“沒有結果。”。
    若欲退出，則按兩下回車。
    該txt表的默認路徑是：./Res/Hanziguyinshouce.txt
這是for python3的版本。
運行平台：python3.6 + windows10通過。

'''

import csv

data_path = './Res/Hanziguyinshouce.txt' #儲存漢字古音手冊txt文檔的路徑

'''
#原先用以函數來輸出當數據爲空時的情況
#現在該功能用 elif row[i] == '' : pass 一句代替了
def check_empty(array, i):
    if array[i] == '':
        return '無'
    else:
        return array[i]
'''

def output(row):
    '''
    此函數專門控制對所查到單行內容的顯示方式
    '''
    s_output = ''
    return_list = [4,5,6,8,11,14,15] #在以上信息【之後】有個換行
    omit_list = [5] #該列內容不顯示
    for i in range(0, len(row)):
        if i in omit_list: #處理要求不顯示的列
            pass
        elif row[i] == '': #處理數據爲空的列：不顯示
            pass
        elif i in return_list:
            s_output = s_output + row[i] + ' \n'
        else:
            s_output = s_output + row[i] + ' '
    return s_output

def look_up(str_x, file_path):
    '''
    此函數用來在文檔中搜尋數據
    '''
    result = '' #存儲查詢的字符串的最終結果
    with open(file_path, 'r', encoding = 'utf-8') as csvf:
        contents = csv.reader(csvf, delimiter = '\t') #文檔的分隔標誌爲tab鍵
        for x in str_x:
            #print csvf.tell() #獲得文件指針所在的位置
            csvf.seek(0) #每循環一次，都要把文件指針指向文件首

            not_found = True #指示是否查到

            #contents = csv.reader(csvf, delimiter = '\t') #文檔的分隔標誌爲tab鍵 #此句放在此處和放在for循環外是一致的


            result = result + '\n' + '-' * 10 + ' ' + x + ' ' + '-' * 10 + '\n'
            result_x = '' #存儲所查每一個字的結果
            for row in contents: #對文件的每一行進行循環
                if x == '': #輸入爲空時，什麼也不做。（否則會遍歷整個文檔）
                    pass #其實有下面的Input_or_Exit()函數，此if塊似可不要。但爲保證look_up()足夠robust，依然保留之。
                elif x in row[5]: #row[5]是“檢索字頭”一欄
                    result_x = result_x + '\n' + output(row) #可能會有多音字

            if result_x == '' and x != '': #循環完所有的行後沒有查到
                result_x = '沒有結果。'+'\n'

            result = result + result_x #把單字的結果相加

    return result

def Input_or_Exit():
    x = input('=' * 40 + '\n' + 'Please input a character > ')
    if x == '':
        x = input('Press the ENTER again to exit > ')
        if x == '':
                exit()
        else:
            return x
    else:
        return x

if __name__ == '__main__':
    while True:
        print (look_up(Input_or_Exit(), data_path))
