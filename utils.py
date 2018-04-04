def jaccard(str1, str2):
    str1 = replacing(str1)
    str2 = replacing(str2)
    lista = str1.split()
    listb = str2.split()
    try:
        if lista[0].isdigit() and listb[0].isdigit():
            if abs(int(lista[0]) - int(listb[0])) > 10:
                return False
    except IndexError:
        return 0
    setA = set(lista)
    setB = set(listb)
    count1 = 0
    count2 = 0
    for x in setA & setB: count1 += 1
    for x in setA | setB: count2 += 1
    jaccard_index = count1 * 1.0 / count2
    # if jaccard_index > 0:
    #     print(str1, str2, jaccard_index)
    return jaccard_index


def address_refine(str1):
    ad = str1.split()
    s = ""
    try:
        for x in ["st", "dr", "ave", "pl", "pky", "blvd"]:
            if x in ad[2].lower().strip():
                for n in range(0, 3):
                    s += ad[n] + " "
            elif x in ad[3].lower().strip():
                for n in range(0, 4):
                    s += ad[n] + " "
    except IndexError:
        return str1

    return s


def replacing(a):
    a = a.lower()
    a = a.replace('avenue', 'ave')
    a = a.replace('street', 'st')
    a = a.replace('boulevard', 'blvd')
    a = a.replace('parkway', 'pky')
    a = a.replace('place', 'pl')
    a = a.replace('drive', 'dr')
    a = a.replace('\'', '')
    return a


#print(jaccard("kfc express", "panda express"))