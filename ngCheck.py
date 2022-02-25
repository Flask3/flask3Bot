import pypinyin

# 得到訊息內每個字的注音開頭
def getBopomofoFirst(msg):
    return pypinyin.lazy_pinyin(msg, style=pypinyin.Style.BOPOMOFO_FIRST) # list

def getBopomofo(msg):
    return pypinyin.lazy_pinyin(msg, style=pypinyin.Style.BOPOMOFO) # list

# 檢查是否上頭
# ['ㄋ','ㄍ'] 為 getBopomofoFirst() 的子字串的話就算
def ShangTouCheck(msg):
    msg = msg.lower().replace(" ", "") #去除空白
    print("訊息:", msg)
    current_point = 0
    reason = 0

    # 檢查英文
    if "nigger" in msg:
        current_point = 20
        reason = 1
    elif "nigga" in msg:
        current_point = 10 
        reason = 2
    elif ("nig" in msg) or ("n1g") in msg or ("n19") in msg or ("ni9") in msg:
        current_point = 5
        reason = 3
    
    msg_first = getBopomofoFirst(msg)
    msg_raw = getBopomofo(msg)
    
    msg_first = [obj for obj in msg_first if obj != " "] # 酷寫法 清掉空白
    msg_raw = [obj for obj in msg_raw if obj != " "]
    print("聲母:", msg_first)
    print("raw:", msg_raw)
    
    if "黑鬼" in msg:
        current_point = 20
        reason = 10
    elif HeiGuiCheck(msg_raw):
        if current_point < 10:
            current_point = 10
            reason = 8
    elif LightHeiGuiCheck(msg_raw):
        if current_point < 5:
            current_point = 5
            reason = 9        
    elif BigCheck(msg_raw): 
        if current_point < 10: 
            current_point = 10 
            reason = 4
    elif SmallCheck(msg_raw):
        if current_point < 5: 
            current_point = 5
            reason = 5
    elif TinyCheck(msg_first):
        if current_point < 2: 
            current_point = 2 
            reason = 6
    elif ZhuYinCheck(msg_raw):
        if current_point < 2:
            current_point = 2
            reason = 7

    print("分數:", current_point, "理由:", reason)
    return current_point

def HeiGuiCheck(list1):
    if len(list1) < 2:
        return False

    # 爛演算法 但先這樣吧
    mark = False
    for t in list1:
        if t == 'ㄏㄟ':
            mark = True
        elif t == 'ㄍㄨㄟˇ' and mark is True:
            return True
        elif mark is True and t != 'ㄍㄨㄟˇ':
            mark = False
    
    return False

def LightHeiGuiCheck(list1):
    if len(list1) < 2:
        return False

    # 爛演算法 但先這樣吧
    mark = False
    for t in list1:
        if 'ㄏㄟ' in t:
            mark = True
        elif 'ㄍㄨㄟ' in t and mark is True:
            return True
        elif mark is True and 'ㄍㄨㄟ' not in t:
            mark = False
    
    return False

def ZhuYinCheck(list1):
    t = ['ㄋㄍ', 'ㄋㄧˊㄍㄜ', 'ㄋㄧㄍㄜ', 'ㄋㄍㄜ', 'ㄋㄧㄍ', 'ㄋㄧˊㄍ', 
        'ㄏㄟㄍㄨㄟ', 'ㄏㄟㄍㄨㄟˇ', 'ㄏㄍ', 'ㄏㄟㄍ', 'ㄏㄍㄨㄟ', 'ㄏㄍㄨㄟˇ']
    
    return bool(set(t).intersection(list1)) #滿酷的寫法

# 檢查ㄋㄧˊ ㄍㄜ
def BigCheck(list1):
    if len(list1) < 2:
        return False

    # 爛演算法 但先這樣吧
    mark = False
    for t in list1:
        if t == 'ㄋㄧˊ':
            mark = True
        elif t == 'ㄍㄜ' and mark is True:
            return True
        elif mark is True and t != 'ㄍㄜ':
            mark = False
    
    return False    

def SmallCheck(list1):
    if len(list1) < 2:
        return False

    # 爛演算法 但先這樣吧
    mark = False
    for t in list1:
        if 'ㄋㄧ' in t:
            mark = True
        elif 'ㄍㄜ' in t and mark is True:
            return True
        elif mark is True and 'ㄍㄜ' not in t:
            mark = False
    
    return False   

# 檢查ㄋ ㄍ
def TinyCheck(list1):
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



# ShangTouCheck("黑鬼")
# ShangTouCheck("黑軌")
# ShangTouCheck("嘿龜")
# ShangTouCheck("漢光")
# ShangTouCheck("ㄏㄍ")