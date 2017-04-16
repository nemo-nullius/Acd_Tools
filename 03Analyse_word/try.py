import pdb
i = 20
def a(x):
    global i
    if x != 0:
        i = i + 1
        print i
        print x
        pdb.set_trace()
        a(x-1)
    else:
        print i
        print x
        return i

print a(5)
