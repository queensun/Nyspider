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
        self.session.get('http://www.douban.com',headers=self.headers)
        self.count=0

    def work(self):
        self.get_urls('http://www.douban.com/tag/%E5%89%A7%E6%83%85/movie',0)
        self.get_urls('http://www.douban.com/tag/%E5%8A%A8%E7%94%BB/movie',1)
        self.get_urls('http://www.douban.com/tag/%E7%8A%AF%E7%BD%AA/movie',2)
        self.get_urls('http://www.douban.com/tag/%E6%83%8A%E6%82%9A/movie',3)
        self.get_urls('http://www.douban.com/tag/%E6%82%AC%E7%96%91/movie',4)
        self.get_urls('http://www.douban.com/tag/cult/movie',5)
        self.get_urls('http://www.douban.com/tag/%E6%81%90%E6%80%96/movie',6)
        self.get_urls('http://www.douban.com/tag/%E6%9A%B4%E5%8A%9B/movie',7)
        self.get_urls('http://www.douban.com/tag/%E9%BB%91%E5%B8%AE/movie',8)

    def get_urls(self,url,types):
        dbs=['juqing_urls.db','donghua_urls.db','fanzui_urls.db','jingsong_urls.db','xuanyi_urls.db','cult_urls.db','kongbu_urls.db','baoli_urls.db','heibang_urls_db']
        db=dbs[types]
        if os.path.isfile(db):
            conn = sqlite3.connect(db)
            cursor=conn.cursor()
        else:
            conn=sqlite3.connect(db)
            cursor=conn.cursor()
            cursor.execute("create table urls(url varchar(40) primary key)")
        urls=self.get_url(url)
        for i in urls:
            try:
                cursor.execute("insert into urls(url) values (?)",(i,))
            except:
                continue
        cursor.close()
        conn.commit()
        conn.close()
        print(db+'    OK')

    def get_url(self,url):
        num=0
        urls=[]
        while True:
            time.sleep(2)
            try:
                html=self.session.get(url+'?start='+str(num)).text
            except:
                break
            try:
                table=BeautifulSoup(html).find('div',attrs={'class':'mod movie-list'}).find_all('dl')
            except:
                break
            if table==[]:
                break
            for i in table:
                urls.append(i.find('a').get('href'))
            num+=15
        return urls

    def run(self):
        for i in range(9):
            self.get_text(i)

    def get_text(self,num):
        dbs=['juqing_urls.db','donghua_urls.db','fanzui_urls.db','jingsong_urls.db','xuanyi_urls.db','cult_urls.db']
        conn = sqlite3.connect(dbs[num])
        cursor = conn.execute("SELECT url from urls")
        file_text=open(dbs[num].replace('_urls.db','.txt'),'w',encoding='utf-8')
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

def test():
    work = Douban()
    #work.get_url('http://www.douban.com/tag/%E7%8A%AF%E7%BD%AA/movie')
    print(work.spider('http://movie.douban.com/subject/3592854/?from=tag_all'))

if __name__ == '__main__':
    work = Douban()
    work.work()
    work.run()
