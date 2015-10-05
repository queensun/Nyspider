#coding:utf-8

import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import time
import re

class Ame_tv():
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
        self.urls=['http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E6%83%8A%E6%82%9A&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E6%82%AC%E7%96%91&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E5%8C%BB%E5%8A%A1&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E5%BE%8B%E6%94%BF&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E8%B0%8D%E6%88%98&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E7%BD%AA%E6%A1%88&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E5%86%92%E9%99%A9&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E7%BE%8E%E5%9B%BD&category=%E5%8A%A8%E7%94%BB&format=&year=&sort=']
        self.get_urls()

    def get_urls(self):
        if os.path.isfile('ame_urls.db'):
            conn = sqlite3.connect('ame_urls.db')
            cursor=conn.cursor()
        else:
            conn=sqlite3.connect('ame_urls.db')
            cursor=conn.cursor()
            cursor.execute("create table urls(url varchar(40) primary key)")
        ame_urls=[]
        for i in self.urls:
            ame_urls+=self.spider(i)
            print(i)
        for url in ame_urls:
            try:
                cursor.execute("insert into urls(url) values (?)",(url,))
            except:
                continue
        cursor.close()
        conn.commit()
        conn.close()

    def spider(self,url):
        html=self.session.get(url,headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            ur=url.replace('eresourcelist?','eresourcelist?page='+str(page))
            html=self.session.get(ur,headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1
        return urls


class Japan_tv():
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
        self.urls=['http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E6%83%8A%E6%82%9A&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E6%82%AC%E7%96%91&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E5%8C%BB%E5%8A%A1&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E5%BE%8B%E6%94%BF&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E8%B0%8D%E6%88%98&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E7%BD%AA%E6%A1%88&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E5%86%92%E9%99%A9&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E6%97%A5%E6%9C%AC&category=%E5%8A%A8%E7%94%BB&format=&year=&sort=']
        self.get_urls()

    def get_urls(self):
        if os.path.isfile('japan_urls.db'):
            conn = sqlite3.connect('japan_urls.db')
            cursor=conn.cursor()
        else:
            conn=sqlite3.connect('japan_urls.db')
            cursor=conn.cursor()
            cursor.execute("create table urls(url varchar(40) primary key)")
        ame_urls=[]
        for i in self.urls:
            ame_urls+=self.spider(i)
        for url in ame_urls:
            try:
                cursor.execute("insert into urls(url) values (?)",(url,))
            except:
                continue
        cursor.close()
        conn.commit()
        conn.close()

    def spider(self,url):
        html=self.session.get(url,headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            ur=url.replace('eresourcelist?','eresourcelist?page='+str(page))
            html=self.session.get(ur,headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1
        return urls


class Britain_tv():
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
        self.urls=['http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E6%83%8A%E6%82%9A&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E6%82%AC%E7%96%91&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E5%8C%BB%E5%8A%A1&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E5%BE%8B%E6%94%BF&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E8%B0%8D%E6%88%98&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E7%BD%AA%E6%A1%88&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E5%86%92%E9%99%A9&format=&year=&sort=',
                    'http://www.zimuzu.tv/eresourcelist?channel=tv&area=%E8%8B%B1%E5%9B%BD&category=%E5%8A%A8%E7%94%BB&format=&year=&sort=']
        self.get_urls()

    def get_urls(self):
        if os.path.isfile('bri_urls.db'):
            conn = sqlite3.connect('bri_urls.db')
            cursor=conn.cursor()
        else:
            conn=sqlite3.connect('bri_urls.db')
            cursor=conn.cursor()
            cursor.execute("create table urls(url varchar(40) primary key)")
        ame_urls=[]
        for i in self.urls:
            ame_urls+=self.spider(i)
        for url in ame_urls:
            try:
                cursor.execute("insert into urls(url) values (?)",(url,))
            except:
                continue
        cursor.close()
        conn.commit()
        conn.close()

    def spider(self,url):
        html=self.session.get(url,headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            ur=url.replace('eresourcelist?','eresourcelist?page='+str(page))
            html=self.session.get(ur,headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1
        return urls

class Other_tv():
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        self.session=requests.session()
        self.url='http://www.zimuzu.tv/eresourcelist?channel=tv&area='
        self.areas=['%E5%8A%A0%E6%8B%BF%E5%A4%A7','%E8%A5%BF%E7%8F%AD%E7%89%99','%E6%84%8F%E5%A4%A7%E5%88%A9','%E5%BE%B7%E5%9B%BD','%E4%BF%84%E7%BD%97%E6%96%AF','%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A','%E5%85%B6%E4%BB%96']
        self.types=['&category=%E6%83%8A%E6%82%9A&format=&year=&sort=',
                    '&category=%E6%82%AC%E7%96%91&format=&year=&sort=',
                    '&category=%E5%8C%BB%E5%8A%A1&format=&year=&sort=',
                    '&category=%E5%BE%8B%E6%94%BF&format=&year=&sort=',
                    '&category=%E8%B0%8D%E6%88%98&format=&year=&sort=',
                    '&category=%E7%BD%AA%E6%A1%88&format=&year=&sort=',
                    '&category=%E5%86%92%E9%99%A9&format=&year=&sort=',
                    '&category=%E5%8A%A8%E7%94%BB&format=&year=&sort=']
        self.urls=[]
        for i in self.areas:
            for j in self.types:
                self.urls.append(self.url+i+j)
        self.get_urls()

    def get_urls(self):
        if os.path.isfile('other_urls.db'):
            conn = sqlite3.connect('other_urls.db')
            cursor=conn.cursor()
        else:
            conn=sqlite3.connect('other_urls.db')
            cursor=conn.cursor()
            cursor.execute("create table urls(url varchar(40) primary key)")
        ame_urls=[]
        for i in self.urls:
            ame_urls+=self.spider(i)
        for url in ame_urls:
            try:
                cursor.execute("insert into urls(url) values (?)",(url,))
            except:
                continue
        cursor.close()
        conn.commit()
        conn.close()

    def spider(self,url):
        html=self.session.get(url,headers=self.headers).text
        table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
        urls=[]
        for i in table:
            urls.append(i.find('a').get('href'))
        page=2
        while True:
            ur=url.replace('eresourcelist?','eresourcelist?page='+str(page))
            html=self.session.get(ur,headers=self.headers).text
            table=BeautifulSoup(html).find('div',attrs={'class':'resource-showlist'}).find_all('div',attrs={'class':'fl-img'})
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            page+=1
        return urls


class get_tv():
    def __init__(self,url):
        self.url=url
        self.session=requests.session()
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}
        postdata={
        'account':'sq5423',
        'password':'sq@lovewenwen134',
        'remember':1,
        'url_back':'http://www.zimuzu.tv/eresourcelist'
        }
        self.session.post('http://www.zimuzu.tv/User/Login/ajaxLogin',data=postdata,headers=self.headers)


    def get_information(self):
        html=self.session.get(self.url,headers=self.headers).text
        table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'fl-info'})
        table=BeautifulSoup(str(table)).find_all('li')
        self.name=BeautifulSoup(html,'lxml').find('div',attrs={'class':'box score-box'}).find('h2').get_text()[:-2]
        self.picture=BeautifulSoup(html,'lxml').find('div',attrs={'class':'fl-img'}).find('a').get('href')
        self.information=[]
        for i in table:
            if i==table[-1]:
                try:
                    self.information.append('简介：'+i.find('div').get_text())
                except:
                    self.information.append(i.get_text())
                break
            self.information.append(i.get_text())

    def get_urls(self):
        html=self.session.get(self.url.replace('resource','resource/list'),headers=self.headers).text
        self.table=BeautifulSoup(html).find('div',attrs={'class':'media-box'}).find_all('div',attrs={'class':'media-list'})


class get_text():
    def __init__(self):
        self.file_Ame=open('Ame_tv.txt','w',encoding='utf-8')
        self.Ame_names=open('Ame_names.txt','w',encoding='utf-8')
        self.file_Japan=open('Japan_tv.txt','w',encoding='utf-8')
        self.Japan_names=open('Japan_names.txt','w',encoding='utf-8')
        self.file_Bri=open('Br_tv.txt','w',encoding='utf-8')
        self.Bri_names=open('Bri_names.txt','w',encoding='utf-8')
        self.file_Other=open('Other_tv.txt','w',encoding='utf-8')
        self.Other_names=open('Other_names.txt','w',encoding='utf-8')

    def run(self):
        self.count=0
        url_db=['bri_urls.db','ame_urls.db','japan_urls.db','other_urls.db']
        for i in url_db:
            self.work(i)

    def work(self,db):
        if db=='ame_urls.db':
            country=1
        if db=='bri_urls.db':
            country=2
        if db=='japan_urls.db':
            country=3
        if db=='other_urls.db':
            country=4
        conn = sqlite3.connect(db)
        cursor = conn.execute("SELECT url from urls")
        if os.path.isfile('completed.db'):
            com = sqlite3.connect('completed.db')
            com_cursor=com.cursor()
        else:
            com=sqlite3.connect('completed.db')
            com_cursor=com.cursor()
            com_cursor.execute("create table urls(url varchar(40) primary key)")

        for row in cursor:
            time.sleep(2)
            try:
                data=get_tv(row[0])
                data.get_information()
                data.get_urls()
            except:
                continue
            if data.table==[]:
                continue
            else:
                try:
                    com_cursor.execute("insert into urls(url) values (?)",(row[0],))
                except:
                    continue
            try:
                self.write(data,country)
            except:
                continue
            print(self.count)
            self.count+=1

        if db=='ame_urls.db':
            self.file_Ame.close()
            self.Ame_names.close()
        if db=='bri_urls.db':
            self.Bri_names.close()
            self.file_Bri.close()
        if db=='japan_urls.db':
            self.file_Japan.close()
            self.Japan_names.close()
        if db=='other_urls.db':
            self.Other_names.close()
            self.file_Other.close()
        cursor.close()
        conn.commit()
        conn.close()
        com_cursor.close()
        com.commit()
        com.close()

    def write(self,data,country):
        urls=''
        li=data.table[0].find_all('li')
        if li==[]:
            return
        for i in data.table:
            li=i.find_all('li')
            try:
                for j in li:
                    urls+=j.find('a',attrs={'type':'ed2k'}).get('href')+'\n'
                    tr='=========='+'\n'
                urls+=tr
            except:
                continue
        urls='[ed2k]'+urls+'[/ed2k]'
        text='[img]'+data.picture+'[/img]'+'\n'
        for i in data.information:
            text=text+i.replace('\n','')+'\n'
        text+=urls
        name='['+data.name+']'+'[MP4+MKV]'+'[中英]'
        if country==1:
            self.file_Ame.write(text+'\n||\n')
            self.Ame_names.write(name+'\n||\n')
        if country==3:
            self.file_Japan.write(text+'\n||\n')
            self.Japan_names.write(name+'\n||\n')
        if country==2:
            self.file_Bri.write(text+'\n||\n')
            self.Bri_names.write(name+'\n||\n')
        if country==4:
            self.file_Other.write(text+'\n||\n')
            self.Other_names.write(name+'\n||\n')


def Main():
    get_ame=Ame_tv()
    get_japan=Japan_tv()
    get_bri=Britain_tv()
    get_other=Other_tv()
    work=get_text()
    work.run()

if __name__=='__main__':
    #Main()
    work=get_tv('http://www.zimuzu.tv/resource/33681')
    work.get_information()
    print(work.information)
