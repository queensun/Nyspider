#coding:utf-8

import requests
import xlwt3
from bs4 import BeautifulSoup
import re

class get_infor():
    def __init__(self,url):
        self.url=url
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def work(self):
        html=self.session.get(self.url,headers=self.headers).text
        self.statue=0
        soup=BeautifulSoup(html)
        self.price=soup.find('div',attrs={'class':'comm-cont'}).find('p',attrs={'class':'mag-b2'}).get_text().replace('\n','').replace(' ','')
        table=soup.find('div',attrs={'class':'comm-list clearfix'}).find_all('dl')
        self.infortable=[]
        for i in table:
            lists=i.find_all('dd')
            for item in lists:
                self.infortable.append(item.get_text().replace('\n','').replace(' ',''))
        self.statue=1


class get_urls():
    def __init__(self,url):
        self.url=url
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def run(self):
        html=self.session.get(self.url,headers=self.headers).text
        lists=BeautifulSoup(html,'lxml').find('div',attrs={'class':'pL'}).find('ul').find_all('li')
        urls=[]
        for item in lists:
            urls.append(item.find('a').get('href'))
        return urls

class Main():
    def work(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
        for page in range(338):
            get_url=get_urls('http://shanghai.anjuke.com/community/W0QQp1Z7QQp'+'Z'+str(page+1))
            print(page)
            urls=get_url.run()
            for url in urls:
                item=get_infor(url)
                item.work()
                if item.statue==0:
                    continue
                self.sheet.write(self.count,0,'浦东')
                num=1
                for infor in item.infortable:
                    self.sheet.write(self.count,num,infor)
                    num+=1
                self.sheet.write(self.count,num,item.price)
                num+=1
                self.sheet.write(self.count,num,url)
                self.count+=1
                self.f.save('data.xls')
def test():
    test=get_infor('http://shanghai.anjuke.com/community/view/106')
    test.work()


if __name__=='__main__':
    work=Main()
    work.work()
