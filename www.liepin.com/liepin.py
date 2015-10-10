# coding:utf-8
from bs4 import BeautifulSoup
import requests
import time
import xlwt3
import re
import threading

class get_urls():
    def __init__(self,url,page):
        self.session=requests.session()
        self.url = url
        self.page = page
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def run(self):
        lists = []
        html = requests.get(self.url+'/&curPage='+str(self.page),headers=self.headers).text
        soup = BeautifulSoup(html,'lxml')
        table = soup.find('ul', attrs = {'class' : 'sojob-result-list'})
        list = table.find_all('li')
        for i in list:
            url1 = i.find('a').get('href')
            lists.append(url1)
        return lists

class Get_infor(threading.Thread):
    def __init__(self,url):
        super(Get_infor,self).__init__()
        self.url=url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def run(self):
        html = requests.get(self.url,headers=self.headers).text
        soup = BeautifulSoup(html,'lxml')
        self.statue=1
        try:
            c = soup.find('div',attrs={'class':'main'}).find('div',attrs={'class':'title'})
            self.company=c.find('div',attrs={'class':'title-info '}).find('h3').get_text()
            self.job=c.find('div',attrs={'class':'title-info '}).find('h1').get_text()
            self.city=c.find('p',attrs={'class':'basic-infor'}).find('span').get_text()
            self.experience=c.find('div',attrs={'class':'resume clearfix'}).find_all('span')[1].get_text()
            self.edu=c.find('div',attrs={'class':'resume clearfix'}).find_all('span')[0].get_text()
            self.age=c.find('div',attrs={'class':'resume clearfix'}).find_all('span')[3].get_text()
            self.salary=re.match(r'.*万',c.find('p',attrs={'class':'job-main-title'}).get_text()).group(0)
        except:
            self.statue=0

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook(encoding='utf-8')
        self.sheet=self.f.add_sheet('sheet',cell_overwrite_ok=True)
        self.sheet1=self.f.add_sheet('sheet1',cell_overwrite_ok=True)
        self.count = 1
        head=['公司','职位','职位发布城市','工作经验','学历要求','年龄要求','薪水']
        num=0
        for i in head:
            self.sheet.write(0,num,i)
            self.sheet1.write(0,num,i)
            num += 1
        self.f.save('data.xls')
    def run(self):
        url = input('请输入猎聘网的链接:')
        hang = 1
        hang1 = 1
        counting = 0
        pro_urls=[]
        for page in range(100):
            get_url = get_urls(url,page)
            urls = get_url.run()
            if urls==pro_urls:
                break
            pro_urls=urls
            threadings=[]
            for i in urls:
                work=Get_infor(i)
                threadings.append(work)
            for work in threadings:
                work.start()
            for work in threadings:
                work.join()
            for work in threadings:
                if(work.statue == 1):
                    if(work.age == '年龄不限'):
                        self.sheet1.write(hang1,0,work.company)
                        self.sheet1.write(hang1,1,work.job)
                        self.sheet1.write(hang1,2,work.city)
                        self.sheet1.write(hang1,3,work.experience)
                        self.sheet1.write(hang1,4,work.edu)
                        self.sheet1.write(hang1,5,work.age)
                        self.sheet1.write(hang1,6,work.salary)
                        hang1+=1
                    else:
                        self.sheet.write(hang,0,work.company)
                        self.sheet.write(hang,1,work.job)
                        self.sheet.write(hang,2,work.city)
                        self.sheet.write(hang,3,work.experience)
                        self.sheet.write(hang,4,work.edu)
                        self.sheet.write(hang,5,work.age)
                        self.sheet.write(hang,6,work.salary)
                        hang+=1
                else:
                    continue
                print(counting)
                counting+=1
            self.f.save('data.xls')

if __name__=='__main__':
    work=Main()
    work.run()
