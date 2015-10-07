# coding:utf-8

from bs4 import BeautifulSoup
import requests
import xlwt3
import re
import time

class Get_infor():
    def __init__(self,code):
        self.session=requests.session()
        self.code=code
        self.url_all='http://vol.stock.hexun.com/Data/Stock/Deal/All.ashx?code='+code+'&count=20&page='
        self.url_buy='http://vol.stock.hexun.com/Data/Stock/Deal/Buy.ashx?code='+code+'&count=20&page='
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.f=xlwt3.Workbook()
        self.sheet_all=self.f.add_sheet('all')
        self.sheet_buy=self.f.add_sheet('buy')
        self.buy_count=0
        self.all_count=0
    def run(self):
        html=self.session.get(self.url_all+str(2),headers=self.headers).text.replace('sum','"sum"').replace('list','"list"').replace('(','').replace(')','')
        for num in range(17):
            html=html.replace('data'+str(num),str(num))
        data=eval(html)
        pages=data['sum']//20+1
        print('获取交易明细')
        for page in range(pages):
            try:
                html=self.session.get(self.url_all+str(page+1)+'&callback=hx_json1444183138247644219',headers=self.headers).text.replace('sum','"sum"').replace('list','"list"').replace('(','').replace(')','').replace('hx_json1444183138247644219','')
                for num in range(17):
                    html=html.replace('data'+str(num),str(num))
                data=eval(html)
            except:
                print('something wrong')
                break
            for item in data['list']:
                num=0
                for key in item:
                    self.sheet_all.write(self.all_count,num,BeautifulSoup(item[key],'html.parser').get_text())
                    num+=1
                    if num==11:
                        break
                self.all_count+=1
            print(page)
            time.sleep(1)
            self.f.save(self.code+'.xls')
        print('获取买卖明细')
        for page in range(pages):
            try:
                html=self.session.get(self.url_buy+str(page+1)+'&callback=hx_json1444183138247644219',headers=self.headers).text.replace('sum','"sum"').replace('list','"list"').replace('(','').replace(')','').replace('hx_json1444183138247644219','')
                for num in range(17):
                    html=html.replace('data'+str(num),str(num))
                data=eval(html)
            except:
                print('something wrong')
                break
            for item in data['list']:
                num=0
                for key in item:
                    self.sheet_buy.write(self.buy_count,num,BeautifulSoup(item[key],'html.parser').get_text())
                    num+=1
                    if num==10:
                        break
                self.buy_count+=1
            print(page)
            time.sleep(1)
            self.f.save(self.code+'.xls')

def test():
    code=input('输入股票代码：')
    work=Get_infor(code)
    work.run()
    print('OK')
    time.sleep(20)

if __name__=='__main__':
    test()
