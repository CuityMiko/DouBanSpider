import ssl
import bs4
import re

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
    


douBanSpider = DouBanSpider()
print(douBanSpider.getCategroiesContent())