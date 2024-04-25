

from .msg_wrapper import wikiPage

from sys import api_version
import requests
from bs4 import BeautifulSoup
import wikipediaapi
from opencc import OpenCC



wiki_wiki = wikipediaapi.Wikipedia('zh')
url_head = "https://"

# 維基百科 隨機的page 
# (GET https://zh.wikipedia.org/wiki/Special:%E9%9A%8F%E6%9C%BA%E9%A1%B5%E9%9D%A2)
# 會回傳頁面的title + 第一張圖片的網址

def getRandomPageTitlePhoto():

    # request
    url = requests.get("https://zh.wikipedia.org/wiki/Special:Random")

    # 美麗湯爬蟲 拿標題
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text

    # 處理圖片網址的部分
    img_link = ""
    try:
        img = soup.find(class_="image").find('img').get('src')
        img = img.split('//')[1]

        img_link = url_head + img
        
    except:
        pass
    
    return title, img_link

# 拿title 用Wikipedia API去找page
# return的是該page
def getPage(title):
    return wiki_wiki.page(title)

# 查詢頁面
# 很多都跟RandomPage的code重複，要再清理
def SearchPage(keyword):

    # 用keyword拿Page
    page = getPage(keyword)

    if (page.exists()):

        # 一樣拿title summary去簡轉繁
        title = page.title
        summary = page.summary

        cc = OpenCC('s2twp')    # s2twp 有包含轉換用詞
        title = cc.convert(title)
        summary = cc.convert(summary)

        # 拿url
        url = page.fullurl
        img_url = ""

        # clean-up summary
        if ("== " in summary):
            summary = cleanSummary(summary)

        return msg_wrapper.wikiPage(title, summary, url, img_url)

    else:
        # 用爬的
        try:
            url = requests.get("https://zh.wikipedia.org/w/index.php?search=" + keyword + "&title=Special:%E6%90%9C%E7%B4%A2&profile=advanced&fulltext=1&ns0=1")
            soup = BeautifulSoup(url.content, "html.parser")
            title = soup.find(class_="mw-search-result").find("a").get("title")
        except:
            return "頁面不存在"

        # 有爬到的話就遞迴
        # 遞到最後會炸 就直接return 頁面不存在
        return SearchPage(title)

# SearchPage("5/16")
# SearchPage("nigger")
# SearchPage("哈囉")

# __main__
def RandomWikiPage():
    # 先random出一個page
    # 拿該page的 title 和 圖片url
    title, img_url = getRandomPageTitlePhoto()
    
    # 用API去撈該page
    page = getPage(title)

    if page.exists():

        # summary
        summary = page.summary

        # 簡轉繁
        # 轉換標題、summary
        cc = OpenCC('s2twp')    # s2twp 有包含轉換用詞
        title = cc.convert(title)
        summary = cc.convert(summary)

        # page的網址
        url = page.fullurl

        # hotix
        # 會把大意中的參考資料那些的清掉
        if ("== " in summary):
            summary = cleanSummary(summary)

        # print(title)
        # print(summary)
        # print("url_link:", url)
        # print("img_link:", img_url)
        # print(title, summary, url, img_url)

        return wikiPage(title, summary, url, img_url)
    
    else:
        print("你搜到一個不存在的頁面喔")


# 清理有些summary裡面會有參考資料的部分
def cleanSummary(summary):
    summary = summary.split("== ")
    s = summary[0].strip('\n')
    
    return s
