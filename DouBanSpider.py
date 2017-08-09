import ssl
import bs4
import re
import sys
import requests

from urllib import request, error

context = ssl._create_unverified_context()

class DouBanSpider:
    def __init__(self):
        self.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        self.headers = {"User-Agent": self.userAgent}

    # 拿到豆瓣图书的分类标签
    def getBookCategroies(self):
        try:
            url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"
            response = request.urlopen(url, context=context)
            content = response.read().decode("utf-8")
            return content
        except error.HTTPError as identifier:
            print("errorCode: " + identifier.code + "errrorReason: " + identifier.reason)
            return None

    # 找到每个标签的内容
    def getCategroiesContent(self):
        content = self.getBookCategroies()
        if not content:
            print("页面抓取失败...")
            return None
        soup = bs4.BeautifulSoup(content, "lxml")
        categroyMatch = re.compile(r"^/tag/*")
        categroies = []
        for categroy in soup.find_all("a", {"href": categroyMatch}):
            if categroy:
                categroies.append(categroy.string)
        return categroies
    
    #拿到每个标签的链接 
    def getCategroyLink(self):
        categroies = self.getCategroiesContent()
        categroyLinks = []
        for item in categroies:
            link = "https://book.douban.com/tag/" + str(item)
            categroyLinks.append(link)
        return categroyLinks

    def getBookInfo(self):
        bookList = []
        categroies = self.getCategroyLink()
        link = categroies[0]
        try:
            response = requests.get(link)
            soup = bs4.BeautifulSoup(response.text, 'lxml')
            for book in soup.find_all("li", {"class": "subject-item"}):
                bookSoup = bs4.BeautifulSoup(str(book), "lxml")
                bookTitle = bookSoup.h2.a["title"]
                bookAuthor = bookSoup.find("div", {"class": "pub"}).string
                bookComment = bookSoup.find("span", {"class": "pl"}).string
                bookContent = bookSoup.find("p").string
                if bookTitle and bookAuthor and bookComment and bookContent:
                    bookList.append([bookTitle.strip(), bookAuthor.strip(), bookComment.strip(), bookContent.strip()])
            return bookList

        except error.HTTPError as identifier:
            print("errorCode: " + identifier.code + "errrorReason: " + identifier.reason)
            return None

    def saveBookInfo(self): 
        

douBanSpider = DouBanSpider()
print(douBanSpider.getBookInfo())