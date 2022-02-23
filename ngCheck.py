import pypinyin

# 得到訊息內每個字的注音開頭
def getBopomofoFirst(msg):
    return pypinyin.lazy_pinyin(msg, style=pypinyin.Style.BOPOMOFO_FIRST) # list

# 檢查是否上頭
# ['ㄋ','ㄍ'] 為 getBopomofoFirst() 的子字串的話就算
def ShangTouCheck(msg):
    msg = msg.lower()
    if ("nig" in msg) or ("nigger" in msg) or ("nigga" in msg) or ("ㄋㄍ" in msg):
        return True

    ng = ['ㄋ', 'ㄍ']
    t = getBopomofoFirst(msg)
    
    t = [obj for obj in t if obj != " "] # 酷寫法 清掉空白

    # print(t)
    return listInNGList(t)

def listInNGList(list1):
    if len(list1) < 2:
        return False

    # 爛演算法 但先這樣吧
    mark = False
    for t in list1:
        if t == 'ㄋ':
            mark = True
        elif t == 'ㄍ' and mark is True:
            return True
        elif mark is True and t != 'ㄍ':
            mark = False
    
    return False

    

    
# print(ShangTouCheck("ㄋㄍ"))
# print(ShangTouCheck("你哥哥"))
# print(ShangTouCheck("你的哥哥"))