# coding:utf-8

import time
import requests
from bs4 import BeautifulSoup
import os
import sqlite3

class Douban():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
        self.count=0
        self.session.get('http://www.douban.com',headers=self.headers)

    def work(self):
        if os.path.isfile('tv_urls.db'):
            conn = sqlite3.connect('tv_urls.db')
            cursor=conn.cursor()
        else:
            conn=sqlite3.connect('tv_urls.db')
            cursor=conn.cursor()
            cursor.execute("create table urls(url varchar(40) primary key)")
        urls=self.get_url('http://movie.douban.com/tag/%E7%94%B5%E8%A7%86%E5%89%A7')
        for i in urls:
            try:
                cursor.execute("insert into urls(url) values (?)",(i,))
            except:
                continue
        cursor.close()
        conn.commit()
        conn.close()
        print('OK')

    def get_url(self,url):
        num=0
        urls=[]
        while True:
            time.sleep(2)
            try:
                html=self.session.get(url+'?start='+str(num)+'&type=T').text
            except:
                break
            try:
                table=BeautifulSoup(html).find('div',attrs={'class':'article'}).find('div',attrs={'class':''}).find_all('table')
            except:
                break
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a',attrs={'class':'nbg'}).get('href'))
            num+=20
        return urls

    def get_text(self):
        conn = sqlite3.connect('tv_urls.db')
        cursor = conn.execute("SELECT url from urls")
        file_text=open('tv.txt','w',encoding='utf-8')
        for row in cursor:
            time.sleep(2)
            try:
                text=self.spider(row[0])
            except:
                continue
            file_text.write(text+'\n\n')
            print(self.count)
            self.count+=1
        cursor.close()
        conn.commit()
        conn.close()
        file_text.close()

    def spider(self, url):
        html = requests.get(url, headers=self.headers).text
        soup = BeautifulSoup(html)
        name=soup.find('span',attrs={'property':'v:itemreviewed'}).get_text()
        picture=soup.find('img',attrs={'rel':'v:image'}).get('src')
        picture='[img]'+picture+'[/img]'
        text=name+'\n'
        text+=picture+'\n'
        info=soup.find('div',attrs={'class':'indent clearfix'}).find('div',attrs={'id':'info'}).get_text()
        text+=info
        intro=soup.find('div',attrs={'class':'related-info'}).get_text()
        text+=intro
        return text

if __name__=='__main__':
    work=Douban()
    work.work()
    work.get_text()
