#coding:utf-8

import requests
from bs4 import BeautifulSoup

class Get_movie_urls():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

    def jingsong(self):
        html=self.session.get('http://www.zimuzu.tv/eresourcelist?channel=movie&area=&category=%E6%83%8A%E6%82%9A&format=&year=&sort=',headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            html=self.session.get('http://www.zimuzu.tv/eresourcelist?page='+str(page)+'&channel=movie&area=&category=%E6%83%8A%E6%82%9A&format=&year=&sort=',headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1
    def xuanyi(self):
        html=self.session.get('http://www.zimuzu.tv/eresourcelist?channel=movie&area=&category=%E6%82%AC%E7%96%91&format=&year=&sort=',headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            html=self.session.get('http://www.zimuzu.tv/eresourcelist?page='+str(page)+'&channel=movie&area=&category=%E6%82%AC%E7%96%91&format=&year=&sort=',headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1
    def zuian(self):
        html=self.session.get('http://www.zimuzu.tv/eresourcelist?channel=movie&area=&category=%E7%BD%AA%E6%A1%88&format=&year=&sort=',headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            html=self.session.get('http://www.zimuzu.tv/eresourcelist?page='+str(page)+'&channel=movie&area=&category=%E7%BD%AA%E6%A1%88&format=&year=&sort=',headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1

    def maoxian(self):
        html=self.session.get('http://www.zimuzu.tv/eresourcelist?channel=movie&area=&category=%E5%86%92%E9%99%A9&format=&year=&sort=',headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            html=self.session.get('http://www.zimuzu.tv/eresourcelist?page='+str(page)+'&channel=movie&area=&category=%E5%86%92%E9%99%A9&format=&year=&sort=',headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1



if __name__=='__main__':
    work=Get_movie_urls()
    work.jingsong()
