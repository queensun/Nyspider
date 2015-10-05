#coding:utf-8

import requests
import xlwt3
from bs4 import BeautifulSoup
import re
import threading
import json
import random
import time

class Get_urls():
    def __init__(self,url):
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.url=url
    def run(self):
        html=self.session.get(self.url,headers=self.headers).text
        data=json.loads(html)
        data=data['data']['searchResult']['judgements']
        ids=[]
        for item in data:
            ids.append(item['id'])
        return ids

class Get_infor():
    def __init__(self,ID):
        self.url='http://www.itslaw.com/api/v1/detail?timestamp=1443233970966&judgementId='+ID
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    def run(self):
        html=self.session.get(self.url,headers=self.headers).text
        data=json.loads(html)
        data=data['data']['fullJudgement']
        self.title=data['title']
        self.court=data['court']
        try:
            self.judgementDate=data['judgementDate']
        except:
            self.judgementDate=data['publishDate']
        try:
            self.caseNumber=data['caseNumber']
        except:
            self.caseNumber=''
        try:
            self.caseType=data['caseType']
        except:
            self.caseType=''
        try:
            self.judgementType=data['judgementType']
        except:
            self.judgementType=''
        try:
            self.trialRound=''
            if data['trialRound']=='1':
                self.trialRound='一审'
            if data['trialRound']=='2':
                self.trialRound='二审'
            if data['trialRound']=='3':
                self.trialRound='再审'
        except:
            self.trialRound=''
        self.texts=[]
        for item in data['paragraphs']:
            try:
                infor=item['typeText']+':\n'
            except:
                infor=''
            for i in item['subParagraphs']:
                try:
                    infor+=i['text']+'\n'
                except:
                    infor+=''
            self.texts.append(infor)

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def run(self):
        for page in range(91):
            if page*20<1100:
                continue
            ids=Get_urls('http://www.itslaw.com/api/v1/caseFiles?startIndex='+str(page*20)+'&countPerPage=20&sortType=1&conditions=searchWord%2B%E5%AE%89%E5%85%A8%E7%94%9F%E4%BA%A7%E7%9B%91%E7%9D%A3%E7%AE%A1%E7%90%86%E5%B1%80%2B1&conditions=caseType%2B3%2B1').run()
            for num in ids:
                work=Get_infor(num)
                work.run()
                self.sheet.write(self.count,0,work.title)
                self.sheet.write(self.count,1,work.court)
                self.sheet.write(self.count,2,work.judgementDate)
                self.sheet.write(self.count,3,work.caseNumber)
                self.sheet.write(self.count,4,work.caseType)
                self.sheet.write(self.count,5,work.judgementType)
                self.sheet.write(self.count,6,work.trialRound)
                num=7
                for i in work.texts:
                    self.sheet.write(self.count,num,i)
                    num+=1
                self.count+=1
                self.f.save('data2.xls')
                print(self.count)
if __name__=='__main__':
    work=Main()
    work.run()
