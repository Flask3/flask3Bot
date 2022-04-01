from sys import api_version
import requests
from bs4 import BeautifulSoup
import wikipediaapi
from opencc import OpenCC
import msg_wrapper

wiki_wiki = wikipediaapi.Wikipedia('zh')
url_head = "https://"

def getRandomPageTitlePhoto():
    # https://zh.wikipedia.org/wiki/Special:Random
    url = requests.get("https://zh.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text
    img_link = ""
    

    try:
        img = soup.find(class_="image").find('img').get('src')
        img = img.split('//')[1]

        img_link = url_head + img
        
    except:
        pass
    
    
    
    return title, img_link


def getPage(title):
    return wiki_wiki.page(title)

def RandomWikiPage():
    title, img_url = getRandomPageTitlePhoto()
    
    page = getPage(title)

    if page.exists():
        summary = page.summary
        cc = OpenCC('s2twp')
        title = cc.convert(title)
        summary = cc.convert(summary)
        url = page.fullurl

        

        # hotix
        if ("== " in summary):
            summary = cleanSummary(summary)

        print(title)
        print(summary)
        print("url_link:", url)
        print("img_link:", img_url)
        # print(title, summary, url, img_url)
        return msg_wrapper.wikiPage(title, summary, url, img_url)
    
    else:
        print("你搜到一個不存在的頁面喔")

def cleanSummary(summary):
    summary = summary.split("== ")
    s = summary[0].strip('\n')
    
    return s



str = "野光牙寶蓮魚野光牙寶蓮燈魚，為輻鰭魚綱脂鯉目脂鯉亞目脂鯉科的其中一個種。分佈於南美洲奧裏諾科河流域，體長可達3.6公分，棲息在底中層水域，生活習性不明。\n\n\n== 參考文獻 =="

cleanSummary(str)
# for i in range(5):
#     RandomWikiPage()
#     print("==================")