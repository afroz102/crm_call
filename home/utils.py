# Improve order and space(In future)
def sortQueryObj(listObj, sortedIndexArr):
    # print(listObj)
    # print(sortedIndexArr)
    newListObj = []
    for index in sortedIndexArr:
        for obj in listObj:
            if int(index) == obj.id:
                newListObj.append(obj)

    # print(newListObj)
    return newListObj
