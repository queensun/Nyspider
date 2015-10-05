#coding:utf-8

import requests
import xlwt
import xlrd
from bs4 import BeautifulSoup
import os
import sqlite3
import time
import re
import random

class get_urls():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            "X-Forwarded-For":'',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def get_url(self):
        f=xlwt.Workbook()
        sheet=f.add_sheet('sheet',cell_overwrite_ok=True)
        num=0
        data=xlrd.open_workbook('urls.xls')
        table=data.sheets()[0]
        for i in range(table.nrows):
            if(i<1389):
                continue
            url=self.spider(table.cell(i,0).value)
            if(url=='null'):
                continue
            self.headers = {
                "X-Forwarded-For":'186.19.12.'+str(random.randint(0, 255)),
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': 1,
                'Connection': 'keep-alive'}
            html=requests.get('http://www.aihuishou.com'+url,headers=self.headers).text
            soup=BeautifulSoup(html)
            sheet.write(num,0,soup.find('div',attrs={'class':'product_name'}).get_text())
            sheet.write(num,1,soup.find('div',attrs={'class':'price'}).get_text())
            num+=1
            print(num)
            f.save('price.xls')
    def spider(self,url):
        count=0
        while(True):
            if(count==20):
                return('null')
            try:
                self.headers = {
                    "X-Forwarded-For":'186.101.12.'+str(random.randint(0, 255)),
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': 1,
                    'Connection': 'keep-alive'}
                html=requests.get(url,headers=self.headers).text
                table=BeautifulSoup(html).find('div',attrs={'class':'step_right'}).find_all('dl')
                num=''
                for i in table:
                    num+=i.find('li').get('data-id')+';'
                num+='2026;2045;2098;2100;2104;2106;2108;2112;2129;2134;2476;2102;'
                '''
                rel='(\d+)'
                id_num=re.findall(re.compile(rel),url)[0]
                '''
                id_num=BeautifulSoup(html).find('div',attrs={'id':'submit'}).get('data-pid')
                postdata={
                'AuctionProductId':id_num,
                'ProductModelId':'',
                'PriceUnits':num
                }
                html=self.session.post('http://www.aihuishou.com/userinquiry/create',data=postdata,headers=self.headers).text
                break
            except:
                count+=1
                continue
        rel=r'RedirectUrl":"(.*?)"'
        count=0
        while True:
            if(count==20):
                return('null')
            try:
                url=re.findall(re.compile(rel),html)[0]
                break
            except:
                self.headers = {
                    "X-Forwarded-For":'189.'+str(random.randint(0, 255))+'.12.'+str(random.randint(0, 255)),
                    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': 1,
                    'Connection': 'keep-alive'}
                html=self.session.post('http://www.aihuishou.com/userinquiry/create',data=postdata,headers=self.headers).text
                count+=1
                continue
        return(url)

def get():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': 1,
        'Connection': 'keep-alive'}
    f=xlwt3.Workbook()
    sheet=f.add_sheet('sheet')
    num=90
    for i in range(55):
        html=requests.get('http://www.aihuishou.com/product/search?cid=1&bid=0&keyword=&pageIndex='+str(i+1),headers=headers).text
        table=BeautifulSoup(html).find('ul',attrs={'class':'products'}).find_all('li')
        urls=[]
        for j in table:
            urls.append('http://www.aihuishou.com'+j.find('a').get('href'))
        for j in urls:
            sheet.write(num,0,j)
            num+=1
        f.save('urls.xls')
        print(i)

if __name__=='__main__':
    work=get_urls()
    work.get_url()
