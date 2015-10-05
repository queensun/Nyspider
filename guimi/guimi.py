#coding:utf-8

from bs4 import BeautifulSoup
import requests
import time
import re
import jieba
import sys
import jieba.analyse
import xlwt

class Urls_get():
    def __init__(self,url):
        self.url=url
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
        print('Get items')
        self.item_urls=[]
        self.get_urls()

    def get_urls(self):
        html=self.session.get(self.url,headers=self.headers).text
        rel=r'class="txtBg" href="(.*?)" target='
        rel=re.compile(rel)
        lists=re.findall(rel,html)
        for i in lists:
            if(i.endswith('review')):
                continue
            if(i.endswith('product')):
                continue
            self.item_urls.append(i)
        count=2
        while(True):
                time.sleep(1)
                html=self.session.get(self.url+'&page='+str(count),headers=self.headers).text
                lists=re.findall(rel,html)
                if lists:
                    for i in lists:
                        if(i.endswith('review')):
                            continue
                        if(i.endswith('product')):
                            continue
                        self.item_urls.append(i)
                    count+=1
                else:
                    break

class Word_frequency():
    def __init__(self,file_name):
        self.file_name=file_name
        self.analyse()

    def analyse(self):
        content=open(self.file_name,'r').read()
        '''
        text=jieba.analyse.extract_tags(content, topK=50, withWeight=True, allowPOS=('adj'))
        '''
        text=jieba.analyse.textrank(content, topK=50, withWeight=True, allowPOS=('adj'))
        f=xlwt.Workbook()
        sheet=f.add_sheet('sheet')
        count=0
        for i in text:
            sheet.write(count,0,i[0])
            sheet.write(count,1,i[1])
            count+=1
        f.save('fenghua.xls')

class Review_get():
    def __init__(self,urls):
        self.urls=urls
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
        print('Get reviews')
        self.reviews=[]
        self.write_review()

    def write_review(self):
        for i in self.urls:
            self.reviews+=self.spider(i)
        file=open('fenghua.txt','w')
        for i in self.reviews:
            file.write(i+'\n')
        file.close

    def spider(self,url):
        count=1
        review=[]
        while(True):
            time.sleep(0.1)
            html=self.session.get(url+ str(count),headers=self.headers).content
            soup=BeautifulSoup(html).find_all('p',attrs={'class':'com_p'})
            if soup:
                for i in soup:
                    review.append(i.get_text())
                count+=1
            else:
                return review
def Main():
    item_get=Urls_get('http://so.kimiss.com/?keyword=%B7%E4%BB%A8%BB%A4%B7%A2%CB%D8&idx=10')
    urls=item_get.item_urls
    review_get=Review_get(urls)
    Analyse=Word_frequency('fenghua.txt')

if __name__=='__main__':
    Main()
