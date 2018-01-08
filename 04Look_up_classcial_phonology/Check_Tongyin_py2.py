#!/usr/bin/env python
#-*-coding:utf-8-*-
#Python3

import csv
import re

end_sentence = '。！？：；… 　\n'#注意這裏有個半角空格和全角空格，還有一個回車換行符

def read_from_file(file_path):
    '''
    從指定路徑讀已標好音的文件，並把其中的內容作爲雙重list返回。
    '''
    result = []
    with open(file_path, 'r') as csvf:
        contents = csv.reader(csvf, delimiter = '\t') #文檔的分隔標誌爲tab鍵
        for row in contents: #對文件的每一行進行循環。row本身會返回一個數組。
            row.append('') #每一行新填一列，用來儲存用音狀況
            result.append(row)
    return result

def parsing(contents_list):
    index_low = 0 #記錄前一次句號之後的位置。其實，只要記錄前一次的句號位置在哪就行了。當前位置遇到句號，當前位置就是i == index_high
    contents_parsed = []
    for i in range(0, len(contents_list)):
        if contents_list[i][0] in end_sentence:
            contents_parsed = contents_list[index_low:i] #其實contents_list[index_high]並未包含在內
            contents_parsed = check_tongyin(contents_parsed)
            contents_list[index_low:i] = contents_parsed[:]
            contents_parsed = []
            index_low = i + 1
    return contents_list

def check_character(x1, x2):
    '''
    返回兩個字(x1,x2)之間是什麼關係。
    0:不同的字。(參差。參〖差1〗。〖參1〗差。)
    1:同一個字。(參參。〖參1〗〖參1〗)
    2:多音字。(參〖參1〗。〖參1〗〖參2〗)
    '''
    result = 0 #判斷是否爲不同的字，同字，或同一字的多音字

    matchObj_i = re.match(r'〖.'.decode('utf-8'), x1.decode('utf-8'))#也許用個前後斷言不會看起來這麼山寨，但不知是否會增加時間
    matchObj_j = re.match(r'〖.'.decode('utf-8'), x2.decode('utf-8'))

    if matchObj_i == None and matchObj_j == None: #沒有〖符號
        if x1 == x2: #參，參
            result = 1 #同一個字
        else: #參，差
            result = 0 #不同的字
    elif matchObj_i == None and matchObj_j != None: #參〖參1〗。差〖參1〗
        match_i = unicode('〖'+x1, 'utf-8')
        match_j = matchObj_j.group()
        if match_i == match_j:
            result = 2 #多音字
        else:
            result = 0 #不同的字
    elif matchObj_i != None and matchObj_j == None: #〖參1〗參。〖參1〗差
        match_i = matchObj_i.group()
        match_j = unicode('〖'+x2, 'utf-8')
        if match_i == match_j:
            result = 2 #多音字
        else:
            result = 0 #不同的字
    elif matchObj_i != None and matchObj_j != None: #〖參1〗〖參2〗。〖參1〗〖參1〗。〖參1〗〖差2〗.
        match_i = matchObj_i.group()
        match_j = matchObj_j.group()
        if match_i == match_j: #可能是多音字，可能是同一個字（比如〖參2〗〖參2〗）
            if x1 == x2:
                result = 1 #同一個字 〖參1〗〖參1〗
            else:
                result = 2 #多音字關係 〖參1〗〖參2〗
        else:
            result = 0 #不同的字
    return result

def check_same_character(list_character, list_index):
    '''
    用來檢查某一list中，其某幾項（用list_index這個list儲存）是否相同.(相同：同一字，或互爲多音字關係)
    '''
    for i in range(0, len(list_index)-1):
        #【注意】這裏list_character[list_index[i]][0]後面有個[0]，故只適用於本程序。若要轉爲它程序所用，需要將[0]去除，且要注意字符串的編碼。
        if check_character(list_character[list_index[i]][0],list_character[list_index[i+1]][0]) == 0: #表示該二維數組中，每一個子數組的第[0]個位置
            return False #一旦發現有不同的字，就立即返回False。
    return True #全系同一字或同音字，返回True.

def check_tongyin(parsed_list):
    '''
    從得到的list中判斷同音狀況
    注意有古音信息的是如下列：
    H:上古音(row[7])
    I:上古音擬音(row[8])
    K:中古音地位(row[10])
    判斷條件：(HK相等)或I相等
    在read_from_file()函數中已新建音Q列，這裏把結果標在該列(row[16])
    '''
    t = 1 #用來記錄同音的小組數的。以作爲一句中不同同音小組的標記。
    temp_tongyin_index_list = [] #記錄每一輸的同音小組
    #原理：拿一個list記錄每一輸的“去比較者”及查找到的同音字。
    #再檢查該list，若其長度爲1（只有“去比較者”）則pass；若全部爲（同一個字）或（同一個字的多音字），則pass。
    #只有長度大於1，且【不都是】（同一個字或同一個字的多音字）時（注意，這裏不是“都不是”），才予以標注。
    #【舉例】
    #AAAAAAAAA：不標注。
    #AAA〖A2〗AA：不標注。
    #AB〖A2〗A:標注。
    #一輸檢查完後，則所有與“去比較者”【同音且不同形】的字皆已標出。以後遇到已標過的字，就可以直接pass了。
    for i in range(0, len(parsed_list)): #去比較者
        if parsed_list[i][8] + parsed_list[i][7] + parsed_list[i][10] == '': #無注音的行直接pass
            pass
        elif parsed_list[i][16] != '': #如果去比較者已被比較過，直接pass
            pass
        else:
            temp_tongyin_index_list.append(i) #先把被比較者的index記入
            for j in range(i + 1, len(parsed_list)): #被比較者
                if parsed_list[j][8] + parsed_list[j][7] + parsed_list[j][10] == '': #該行爲空，不予比較
                    pass
                elif parsed_list[j][16] != '': #如果被比較者已被比較過，直接pass
                    pass
                elif (parsed_list[i][8] == parsed_list[j][8]) or (parsed_list[i][7] == parsed_list[j][7] and parsed_list[i][10] == parsed_list[j][10]):
                    #b_tongyin = True
                    temp_tongyin_index_list.append(j)
                    #print parsed_list[i][0], parsed_list[j][0]
            #一輪比較結束後
            #print temp_tongyin_index_list
            if len(temp_tongyin_index_list) == 1: #沒有同音字
                pass
            elif check_same_character(parsed_list, temp_tongyin_index_list): #若全係同字或同音字，則忽略
                #print temp_tongyin_index_list
                pass
            #elif check_character(parsed_list[i][0], parsed_list[j][0]) != 0:
                #pass
            else: #同音而又【不全】相同的情況。如：“父夫父”這樣一組，或“〖父2〗〖夫2〗〖父2〗”這樣一組。
                for k in temp_tongyin_index_list:
                    parsed_list[k][16] = str(t)
                    #print parsed_list[k][0]
                t += 1 #這裏應在for循環之外。全部都標記完後才能+1
            temp_tongyin_index_list = []

    return parsed_list

if __name__ == '__main__':
    #from_file = './Output.txt'
    from_file = "./Texts/20180106Workshop/Xunzi.Quanxue_Result.txt"
    to_file = from_file + "_CheckedTongyin"

    result = parsing(read_from_file(from_file))
    for i in range(0, len(result)):
        result[i] = '\t'.join(result[i])
    result = '\n'.join(result)
    #print result
    with open(to_file, 'w') as f:
        f.write(result)
