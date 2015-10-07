# coding:utf-8

from bs4 import BeautifulSoup
import requests
import time
import xlwt3
import re
import threading

class Get_ids():
    def __init__(self,url):
        self.session=requests.session()
        self.url=url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
    def run(self):
        html=self.session.get(self.url,headers=self.headers).text
        ID_re='loanId":(\d+)'
        ids=re.findall(re.compile(ID_re),html)
        return ids

class Get_infor(threading.Thread):
    def __init__(self,loanid):
        super(Get_infor,self).__init__()
        self.loanid=loanid
        self.url='http://www.renrendai.com/lend/detailPage.action?loanId='+self.loanid
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}

    def run(self):
        self.num=1
        try:
            html=requests.get(self.url,headers=self.headers).text
            infor_re='"creditInfo":(.*?),"creditPassedTime"'
            data=re.findall(re.compile(infor_re),html)[0]
            self.infor=eval(data)
        except:
            self.num=0

class Main():
    def __init__(self):
        self.f=xlwt3.Workbook(encoding='utf-8')
        self.sheet=self.f.add_sheet('sheet',cell_overwrite_ok=True)
        self.count=1
        head=['实地认证','身份认证','信用报告','工作认证','收入认证','房产认证','购车认证','结婚认证','学历认证','手机实名认证','微博认证','居住地证明']
        self.sheet.write(0,0,'ID')
        num=1
        for i in head:
            self.sheet.write(0,num,i)
            num+=1
        self.f.save('data.xls')
    def run(self):
        startID=input('输入起始ID:')
        endID=input('输入结束ID:')
        startID=int(startID)
        endID=int(endID)
        ids=[]
        threads=[]
        while startID<endID:
            ids.append(startID)
            if len(ids)<10:
                startID+=1
                continue
            for ID in ids:
                work=Get_infor(str(ID))
                threads.append(work)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            for thread in threads:
                if thread.num==0:
                    continue
                self.sheet.write(self.count,0,thread.loanid)

                if thread.infor['fieldAudit']=='VALID':
                    self.sheet.write(self.count,1,'2')
                elif thread.infor['fieldAudit']=='INVALID':
                    self.sheet.write(self.count,1,'0')
                else:
                    self.sheet.write(self.count,1,'1')

                if thread.infor['identification']=='VALID':
                    self.sheet.write(self.count,2,'2')
                elif thread.infor['identification']=='INVALID':
                    self.sheet.write(self.count,2,'0')
                else:
                    self.sheet.write(self.count,2,'1')

                if thread.infor['credit']=='VALID':
                    self.sheet.write(self.count,3,'2')
                elif thread.infor['credit']=='INVALID':
                    self.sheet.write(self.count,3,'0')
                else:
                    self.sheet.write(self.count,3,'1')

                if thread.infor['work']=='VALID':
                    self.sheet.write(self.count,4,'2')
                elif thread.infor['work']=='INVALID':
                    self.sheet.write(self.count,4,'0')
                else:
                    self.sheet.write(self.count,4,'1')

                if thread.infor['incomeDuty']=='VALID':
                    self.sheet.write(self.count,5,'2')
                elif thread.infor['incomeDuty']=='INVALID':
                    self.sheet.write(self.count,5,'0')
                else:
                    self.sheet.write(self.count,5,'1')

                if thread.infor['house']=='VALID':
                    self.sheet.write(self.count,6,'2')
                elif thread.infor['house']=='INVALID':
                    self.sheet.write(self.count,6,'0')
                else:
                    self.sheet.write(self.count,6,'1')

                if thread.infor['car']=='VALID':
                    self.sheet.write(self.count,7,'2')
                elif thread.infor['car']=='INVALID':
                    self.sheet.write(self.count,7,'0')
                else:
                    self.sheet.write(self.count,7,'1')

                if thread.infor['marriage']=='VALID':
                    self.sheet.write(self.count,8,'2')
                elif thread.infor['marriage']=='INVALID':
                    self.sheet.write(self.count,8,'0')
                else:
                    self.sheet.write(self.count,8,'1')

                if thread.infor['graduation']=='VALID':
                    self.sheet.write(self.count,9,'2')
                elif thread.infor['graduation']=='INVALID':
                    self.sheet.write(self.count,9,'0')
                else:
                    self.sheet.write(self.count,9,'1')


                if thread.infor['mobileReceipt']=='VALID':
                    self.sheet.write(self.count,10,'2')
                elif thread.infor['mobileReceipt']=='INVALID':
                    self.sheet.write(self.count,10,'0')
                else:
                    self.sheet.write(self.count,10,'1')

                if thread.infor['kaixin']=='VALID':
                    self.sheet.write(self.count,11,'2')
                elif thread.infor['kaixin']=='INVALID':
                    self.sheet.write(self.count,11,'0')
                else:
                    self.sheet.write(self.count,11,'1')

                if thread.infor['residence']=='VALID':
                    self.sheet.write(self.count,12,'2')
                elif thread.infor['residence']=='INVALID':
                    self.sheet.write(self.count,12,'0')
                else:
                    self.sheet.write(self.count,12,'1')
                self.count+=1
                print(self.count)
            time.sleep(5)
            ids=[]
            threads=[]
            startID+=1
            self.f.save('data.xls')

def test():
    work=Main()

if __name__=='__main__':
    work=Main()
    work.run()
