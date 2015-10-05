#coding:utf-8

import requests
import xlwt
from bs4 import BeautifulSoup
import time
import re
import random

class get_urls():
    def __init__(self,page,keyword):
        self.session=requests.session()
        self.page=page
        self.keyword=keyword
    def get_url(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
        html=self.session.get('http://www.amazon.cn/s/ref=sr_pg_3?rh=i%3Aaps%2Ck%3A'+self.keyword+'&page='+str(self.page)+'&keywords='+self.keyword+'&ie=UTF8&qid=1442030727',headers=headers).text
        table=BeautifulSoup(html).find('div',attrs={'id':'rightContainerATF'})
        rel='<li(.*?)</li>'
        table=re.findall(re.compile(rel),str(table))
        urls=[]
        rel='href="(.*?)"'
        rel=re.compile(rel)
        for item in table:
            url=re.findall(rel,str(item))
            try:
                urls.append(url[0])
            except:
                continue
        return urls

class get_infor():
    def __init__(self,url):
        self.url=url
        self.session=requests.session()
        self.headers = {
            "X-Forwarded-For":str(random.randint(0, 255))+'.'+str(random.randint(0, 255))+'.'+str(random.randint(0, 255))+'.'+str(random.randint(0, 255)),
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
        self.get_info()
    def get_info(self):
        self.statue=0
        while True:
            try:
                html=self.session.get(self.url,headers=self.headers,timeout=5).text
                soup=BeautifulSoup(html)
                self.price=''.join(soup.find('div',attrs={'id':'price'}).find('tr').get_text().replace('\n','').split())
                self.title=soup.find('h1',attrs={'id':'title'}).get_text().replace('\n','')
                try:
                    self.previews=''.join(list(filter(str.isdigit, soup.find('div',attrs={'id':'centerCol'}).find('a',attrs={'id':'cmrs-atf'}).get_text())))
                except:
                    self.previews=0
                self.picture_url=soup.find('div',attrs={'class':'imgTagWrapper'}).find('img').get('data-old-hires')
                self.picture=self.session.get(self.picture_url,headers=self.headers,timeout=5).content
                self.statue=1
                break
            except:
                break

class Main():
    def __init__(self):
        self.f=xlwt.Workbook()
        self.sheet=self.f.add_sheet('sheet',cell_overwrite_ok=True)
        self.count=0
    def work(self):
        keyword=input("输入关键字（英文）：")
        page=input("输入页数：")
        for i in range(int(page)):
            try:
                work=get_urls(i+1,keyword)
                urls=work.get_url()
            except:
                continue
            for url in urls:
                item=get_infor(url)
                if item.statue==0:
                    continue
                with open(str(self.count)+item.picture_url[-4:],'wb') as img:
                    img.write(item.picture)
                img.close()
                self.sheet.write(self.count,0,str(self.count))
                self.sheet.write(self.count,1,item.title)
                self.sheet.write(self.count,2,item.price)
                self.sheet.write(self.count,3,item.previews)
                self.count+=1
                self.f.save('data.xls')
                print(self.count)

if __name__=='__main__':
    work=Main()
    work.work()
