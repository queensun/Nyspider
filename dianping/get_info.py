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
        infor=BeautifulSoup(html,'lxml').find('div',attrs={'class':'main'}).find('div',attrs={'id':'basic-info'})
        try:
            self.title=infor.find('h1').get_text().replace('\n','').replace(' ','')
        except:
            return
        try:
            self.area=BeautifulSoup(html,'lxml').find('div',attrs={'class':'breadcrumb'}).find_all('a')[2].get_text().replace('\n','').replace(' ','')
        except:
            self.area=''
        try:
            self.address=infor.find('div',attrs={'class':'expand-info address'}).get_text().replace('\n','').replace(' ','')
        except:
            self.address=' '
        try:
            self.tel=infor.find('span',attrs={'itemprop':'tel'}).get_text()
        except:
            self.tel='  '
        table=infor.find('div',attrs={'class':'other J-other Hide'}).find_all('p')
        self.price=''
        self.times=''
        for item in table:
            try:
                if(item.find('span').get_text()=='营业时间：'):
                    self.times=item.get_text().replace('\n','').replace(' ','').replace('修改','')
            except:
                continue
        table=infor.find('div',attrs={'class':'brief-info'}).find_all('span')
        for item in table:
            try:
                if(item.get_text()[:2]=='人均' or item.get_text()[:2]=='费用' or item.get_text()[:2]=='均价'):
                    self.price=item.get_text().replace('\n','').replace(' ','')
            except:
                continue
        if self.price=='':
            self.price='--'
        if self.times=='':
            self.times='--'
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
            'Cookie':'showNav=#nav-tab|0|1; navCtgScroll=0; _hc.v="\"23f85427-5787-47bd-9df4-4e831c7a4cae.1442049973\""; __utma=1.649416466.1442049979.1442049979.1442049979.1; __utmz=1.1442049979.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; cy=1; cye=shanghai; s_ViewType=10; aburl=1; JSESSIONID=95881D627CA4C940D686AD118D776232; PHOENIX_ID=0a0308bc-14fda0ead2e-4e713c',
            'Connection': 'keep-alive'}
    def run(self):
        html=self.session.get(self.url,headers=self.headers).text
        lists=BeautifulSoup(html,'lxml').find('div',attrs={'id':'shop-all-list'}).find_all('li')
        urls=[]
        for item in lists:
            urls.append('http://www.dianping.com'+item.find('a').get('href'))
        return urls

class Main():
    def work(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
        for page in range(50):
            get_url=get_urls('http://www.dianping.com/search/category/1/20/g187r12'+'p'+str(page+1))
            print(page)
            urls=get_url.run()
            for url in urls:
                try:
                    item=get_infor(url)
                    item.work()
                except:
                    continue
                if item.statue==0:
                    continue
                self.sheet.write(self.count,0,'购物')
                self.sheet.write(self.count,1,'超市便利店')
                self.sheet.write(self.count,2,'闵行')
                self.sheet.write(self.count,3,item.area)
                self.sheet.write(self.count,4,item.title)
                self.sheet.write(self.count,5,item.address)
                self.sheet.write(self.count,6,item.tel)
                self.sheet.write(self.count,7,item.price)
                self.sheet.write(self.count,8,item.times)
                self.sheet.write(self.count,9,url)
                self.count+=1
                self.f.save('data.xls')

def test():
    test=get_infor('http://www.dianping.com/shop/1909912')
    test.work()
    print(test.times)
    print(test.price)
if __name__=='__main__':
    work=Main()
    work.work()
