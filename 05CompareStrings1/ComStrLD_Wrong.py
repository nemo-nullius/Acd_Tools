#-*-encoding:utf-8-*-

# Python 3

def Min(A, B, C): #比较ABC三个数中的最小值
    I = A
    if I > B:
        I = B
    elif I > C:
        I = C

    return I

def LD(StrA, StrB): #使用LD算法，比较StrA与StrB这两个字符串
    L = []
    L = [[0 for x in range(len(StrB)+1)] for y in range(len(StrA)+1)]
    '''
    【二维数组的三种实现办法】
    m=[[0 for x in range(4)] for y in range(3)]
    m=[[0]*4 for i in range(3)]
    m=3*[4*[0]] ←这种办法不好，会有浅拷贝的影响。不要用。
    '''
    for i in range(1, len(StrA)+1):
        L[i][0] = i
    for j in range(1, len(StrB)+1):
        L[0][j] = j

    for i in range(1, len(StrA)+1):
        for j in range(1, len(StrB)+1):
            if StrA[i-1] == StrB[j-1]:
                L[i][j] = L[i-1][j-1]
            else:
                L[i][j] = Min(L[i-1][j-1], L[i-1][j], L[i][j-1]) + 1

    return L

def GoBack(L, i, j): #专门用来回溯的函数
    #print (i, j)
    if i == 0 or j == 0:
        return -1 #至少其中之一已回溯完毕
    k = Min(L[i-1][j-1], L[i][j-1], L[i-1][j])
    #print (k)
    if k == L[i-1][j-1]: #左上角的单元格是最小值
        return 0
    elif k == L[i][j-1]: #上边的单元格是最小值
        return 1
    else: #左边的单元格是最小值
        return 2

def Output(Strs, n): #用来控制【缺字/多字】与【异字】的格式
    '''
    n = -1 缺字
    n =  1 多字
    n =  0 异字
    '''
    s = ''
    if n == -1:
        s = '-'
    elif n == 1:
        s = ')' + Strs + '('
    elif n == 0:
        s = ']' + Strs + '['
    else:
        print ('Error of n!')
    return s

def Compare(L, StrA, StrB): #得出比较后的结果
    sA = '' #存储最后结果：顺序是反的
    sB = ''
    i = len(StrA)
    j = len(StrB)
    while True:
        n = GoBack(L, i, j)
        if n == -1: #当至少其中一个已经回溯完了
            if i != 0: #StrA未回溯完，则StrA剩下的全是【增字】
                for m in range(i-1, -1, -1):
                    sA = sA + Output(StrA[m], 1)
                    sB = sB + Output('', -1)
            elif j != 0: #StrB未回溯完，则StrB剩下的全是【增字】
                for n in range(j-1, -1, -1):
                    sA = sA + Output('', -1)
                    sB = sB + Output(StrB[n], 1)
            break
        elif n == 0: #往左上角回溯：相同/不同
            i = i - 1
            j = j - 1
            if StrA[i] == StrB[j]: #相同
                sA = sA + StrA[i]
                sB = sB + StrB[j]
            else: #【异字】
                sA = sA + Output(StrA[i], 0)
                sB = sB + Output(StrB[j], 0)
        elif n == 1: #往上边回溯：StrB【增字】，StrA【缺字】
            j = j - 1
            sA = sA + Output('', -1)
            sB = sB + Output(StrB[j], 1)
        elif n == 2: #往左边回溯：StrB【缺字】，StrA【增字】
            i = i - 1
            sA = sA + Output(StrA[i], 1)
            sB = sB + Output('', -1)

    return (sA[::-1], sB[::-1])





if __name__ == '__main__':
    Str1 = input('The FIRST String > ')
    Str2 = input('The SECOND String > ')
    print (LD(Str1, Str2))
    print (Compare((LD(Str1, Str2)), Str1, Str2))
