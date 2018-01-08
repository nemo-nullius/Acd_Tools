import sys
import os
import Lookup2txt_Q as L
import Check_Tongyin as C

def main():
    # Lookup2txt_Q.py
    from_file1 = os.path.abspath(sys.argv[1])
    fileNameInfo = from_file1.split('.')
    fileName = '.'.join(fileNameInfo[0:-1])
    fileClass = fileNameInfo[-1]
    to_file1 = ''.join((fileName, '_TP','.',fileClass))

    result = ''
    i_no_result = 0
    with open(to_file1, 'w') as f:
        result, i_no_result = L.output_all(L.read_input_file(from_file1))
        f.write(result)
    print ("共有%d個字沒有查到。" %i_no_result)

    # Check_Tongyin.py

    from_file2 = to_file1
    fileNameInfo = from_file2.split('.')
    fileName = '.'.join(fileNameInfo[0:-1])
    fileClass = fileNameInfo[-1]
    to_file2 = ''.join((fileName, '_CP','.',fileClass))

    result = C.parsing(C.read_from_file(from_file2))
    for i in range(0, len(result)):
        result[i] = '\t'.join(result[i])
    result = '\n'.join(result)
    #print result
    with open(to_file2, 'w') as f:
        f.write(result)

    os.remove(to_file1)

if __name__ == '__main__':
    main()
