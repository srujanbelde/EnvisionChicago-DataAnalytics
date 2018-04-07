def jaccard(str1, str2):
    str1 = replacing(str1)
    str2 = replacing(str2)
    if str1 == str2:
        return 1
    chars = jaccard_chars(str1, str2)
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
    words = jaccard_words(setA, setB)
    ji = chars if chars > words else words
    return ji


def jaccard_words(s1, s2):
    count1 = 0
    count2 = 0
    for x in s1 & s2: count1 += 1
    for x in s1 | s2: count2 += 1
    jaccard_index = count1 * 1.0 / count2
    # if jaccard_index > 0:
    #     print(str1, str2, jaccard_index)
    return jaccard_index


def jaccard_chars(s1, s2):
    i = 0
    j = 0
    like = 0
    unlike = 0
    while True:
        if i >= len(s1) or j >= len(s2):
            break
        if s1[i] == " " and s2[j] != " ":
            j += 1
        elif s2[j] == " " and s1[i] != " ":
            i += 1
        elif s1[i] == s2[j]:
            like += 1
            i += 1
            j += 1
        else:
            unlike += 1
            i += 1

    return like/(len(s1) + len(s2) - (2*like) + like)


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
    a = a.replace('and', '&')
    a = a.replace('express', 'exp')
    a = a.replace('pizzeria', 'pizza')
    a = a.replace('academy', 'ady')
    a = a.replace('union station', 'usn')
    a = a.replace('cafe', 'cf')
    a = a.replace('  ', ' ')
    return a


#print(jaccard("kfc express", "panda express"))
#print(jaccard("bacci pizzeria", "bacci's pizza italy"))
