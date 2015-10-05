#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import re
import threading

class Get_infor(threading.Thread):
    def __init__(self,url):
        super(Get_infor,self).__init__()
        self.url=url
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
    def run(self):
        self.statue=1
        try:
            html=self.session.get(self.url,headers=self.headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
        except:
            self.statue=0
            return
        soup=BeautifulSoup(html)
        self.title=soup.find('div',attrs={'class':'inst-summary'}).find('h1').get_text().replace(' ','').replace('\n','')
        table=soup.find('div',attrs={'class':'inst-summary'}).find_all('li')
        self.address=''
        self.bednum=''
        self.price=''
        for item in table:
            if item.get_text().replace(' ','')[:1]=='地':
                self.address=item.get_text().replace(' ','')
            if item.get_text().replace(' ','')[:1]=='床':
                self.bednum=item.get_text().replace(' ','')
            if item.get_text().replace(' ','')[:1]=='收':
                self.price=item.get_text().replace(' ','')
        table=soup.find('div',attrs={'class':'base-info'}).find('div',attrs={'class':'cont'}).find_all('li')
        self.area=''
        self.type=''
        self.people=''
        self.tese=''
        for item in table:
            if item.get_text()[:4]=='所在地区':
                self.area=item.get_text().replace('所在地区：','').replace('\n','').replace(' ','').split('-')
            if item.get_text()[:4]=='机构类型':
                self.type=item.get_text().replace('机构类型：','').replace('\n','').replace(' ','')
            if item.get_text()[:4]=='收住对象':
                self.people=item.get_text().replace('收住对象：','').replace('\n','').replace(' ','')
            if item.get_text()[:4]=='特色服务':
                self.tese=item.get_text().replace('特色服务：','').replace('\n','').replace(' ','')

class Get_urls():
    def __init__(self,url):
        self.url=url
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
    def run(self):
        html=self.session.get(self.url,headers=self.headers).text.encode('ISO-8859-1').decode('utf-8','ignore')
        table=BeautifulSoup(html).find('div',attrs={'class':'list-view'}).find('ul').find_all('li')
        urls=[]
        for item in table:
            try:
                urls.append('http://www.yanglao.com.cn'+item.find('a').get('href'))
            except:
                continue
        return urls

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def run(self):
        for page in range(1569):
            if(page<537):
                continue
            get_url=Get_urls('http://www.yanglao.com.cn/resthome_'+str(page+1))
            urls=get_url.run()
            threads=[]
            for url in urls:
                work=Get_infor(url)
                threads.append(work)
            for work in threads:
                work.start()
            for work in threads:
                work.join()
            for work in threads:
                if work.statue==0:
                    continue
                try:
                    self.sheet.write(self.count,0,work.area[0])
                except:
                    self.sheet.write(self.count,0,' ')
                try:
                    self.sheet.write(self.count,1,work.area[1])
                except:
                    self.sheet.write(self.count,1,' ')
                try:
                    self.sheet.write(self.count,2,work.area[2])
                except:
                    self.sheet.write(self.count,2,' ')
                self.sheet.write(self.count,3,work.title)
                self.sheet.write(self.count,4,work.address)
                self.sheet.write(self.count,5,work.type)
                self.sheet.write(self.count,6,work.people)
                self.sheet.write(self.count,7,work.tese)
                self.sheet.write(self.count,8,work.bednum)
                self.sheet.write(self.count,9,work.price)
                self.count+=1
                print(self.count)
            self.f.save('data.xls')
if __name__=='__main__':
    work=Main()
    work.run()
