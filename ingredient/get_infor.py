#coding:utf-8

import requests
import xlwt3
from bs4 import BeautifulSoup
import re
import xlrd
import threading
import random
import time

class Get_ip():
    def __init__(self,num):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.url='http://vxer.daili666api.com/ip/?tid=559950660678689&num='+str(num)+'&delay=3&category=2'
        self.session=requests.session()
    def get(self):
        ip=self.session.get(self.url,headers=self.headers).text.replace('\n','')
        return ip

class Get_infor(threading.Thread):
    def __init__(self,score,english_name):
        super(Get_infor, self).__init__()
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
        self.score=score
        self.english_name=english_name

    def run(self):
        self.statue=1
        try:
            html=self.session.get('http://www.cosdna.com/chs/stuff.php?q='+self.english_name,headers=self.headers).text
        except:
            self.statue=0
            return
        try:
            url=BeautifulSoup(html).find('div',attrs={'class':'StuffResult'}).find('tr').find('a').get('href')
            self.infor('http://www.cosdna.com/chs/'+url)
        except:
            try:
                self.infor('http://www.cosdna.com/chs/stuff.php?q='+self.english_name)
            except:
                self.statue=0

    def infor(self,url):
        html=self.session.get(url,headers=self.headers).text
        infor_table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'StuffDetail'})
        try:
            self.chinese_name=infor_table.find('div',attrs={'class':'Stuff_DetailC'}).get_text()
        except:
            self.statue=0
            return
        rel='r/>(.*?)<b'
        rel=re.compile(rel)
        try:
            self.function=re.findall(rel,str(infor_table))[0]
        except:
            self.function=''

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def run(self):
        names=xlrd.open_workbook('ingredient.xls')
        table=names.sheets()[0]
        threads=[]
        for i in range(table.nrows):
            get_infor=Get_infor(table.cell(i,0).value,table.cell(i,1).value)
            threads.append(get_infor)
            if len(threads)<30 and i<9505:
                continue
            for work in threads:
                work.start()
            for work in threads:
                work.join()
            for work in threads:
                if work.statue==0:
                    continue
                self.sheet.write(self.count,0,work.score)
                self.sheet.write(self.count,1,work.english_name)
                self.sheet.write(self.count,2,work.chinese_name)
                self.sheet.write(self.count,3,work.function)
                self.count+=1
                print(self.count)
                self.f.save('data.xls')
            threads=[]

if __name__=='__main__':
    work=Main()
    work.run()
