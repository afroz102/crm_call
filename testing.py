

def getKey(item):
    print(item)
    return item[0]


l = [[2, 3], [6, 7], [3, 34], [24, 64], [1, 43]]
x = sorted(l, key=getKey)
print("x: ", x)


X = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
Y = [0,   1,   1,    0,   1,   2,   2,   0,   1]

Z = [x for _, x in sorted(zip(Y, X))]
print("Z: ", Z)

w = [x for _, x in sorted(zip(Y, X), key=lambda pair: pair[0])]
print(w)
