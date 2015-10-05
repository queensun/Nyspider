# coding:utf-8
from bs4 import BeautifulSoup
import requests
import time

class Ganji():
    def __init__(self):
        self.session=requests.session()
        self.f = open('Ganji.txt', 'w', encoding = 'utf-8')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def work(self):
        self.run('changan', 2)
        self.run('dalingshan', 1)
        self.run('humen', 2)
        self.run('changping', 2)
        self.run('qiaotou', 1)
        self.run('qishi', 1)
        self.run('tangsha', 1)
        self.run('qingxi', 1)
        self.run('fenggang', 2)
        self.run('zhangmutou', 1)
        self.f.close()
    def run(self,name,x):
        for page in range(x):
            lists=self.spider(page,name)
            self.write(lists)
    def write(self,lists):
        for i in lists:
            self.f.write(i.find('dt').find('a').get_text()+' ')
            self.f.write(i.find('dd', attrs = {'class' : 'company'}).find('a').get('title')+' ')
            self.f.write(i.find('dd', attrs = {'class' : 'pay'}).get_text()+'\n\n')
    def spider(self,page,name):
        html=requests.get('http://dg.ganji.com/zpwaimaozhuanyuan/'+name+'/o'+str(page+1)+'/',headers=self.headers).text
        soup = BeautifulSoup(html)
        table = soup.find('div', attrs = {'id' : 'list-job-id'})
        lists = table.find_all('dl', attrs = {'class' : 'list-noimg job-list clearfix'})
        return lists

class Job_58():
    def __init__(self):
        self.f = open('job_58.txt', 'w')
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def work(self):
        self.run('changanqv', 1)
        self.run('dalingshan', 1)
        self.run('changpingshi', 1)
        self.run('tangsha', 1)
        self.run('zhangmutou', 1)
        self.run('fenggang', 1)
        self.run('qiaotouz', 1)
        self.run('qingxi', 1)
        self.run('qishis', 1)
        self.f.close()
    def run(self,name,x):
        for page in range(x):
            lists=self.spider(page,name)
            self.write(lists)
    def write(self,lists):
        for i in lists:
            self.f.write(i.find('dt').find('a').get_text().replace('\n',' '))
            self.f.write(i.find('dd', attrs = {'class' : 'w271'}).get_text().replace('\n',' '))
            self.f.write(i.find('dd', attrs = {'class' : 'w96'}).get_text()+'\n\n')
    def spider(self,page,name):
        html=requests.get('http://dg.58.com/'+name+'/zpshangwumaoyi/pn'+str(page+1)+'/',headers=self.headers).text
        soup = BeautifulSoup(html)
        table = soup.find('div', attrs = {'id' : 'infolist'})
        lists = table.find_all('dl')
        return lists

class Job_5156():
    def __init__(self):
        self.session=requests.session()
        self.f = open('job_5156.txt', 'w')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def final(self):
        lists=['http://s.job5156.com/s/p/result?keywordType=0&keyword=%E5%A4%96%E8%B4%B8&locationList=14010500%2C14010600%2C14011000&posTypeList=&industryList=&updateIn=90&salary=&salaryUnPublic=1&gender=&age=&',
            'http://s.job5156.com/s/p/result?keywordType=0&keyword=%E5%A4%96%E8%B4%B8&locationList=14011100%2C14012000%2C14012100&posTypeList=&industryList=&updateIn=90&degreeFrom=1&degreeTo=8&degreeUnlimit=1&workyearFrom=-1&workyearTo=11&workyearUnlimit=1&salary=&salaryUnPublic=1&propertyList=1&gender=&age=&',
            'http://s.job5156.com/s/p/result?keywordType=0&keyword=%E5%A4%96%E8%B4%B8&locationList=14012400%2C14012700%2C14012800&posTypeList=&industryList=&updateIn=90&degreeFrom=1&degreeTo=8&degreeUnlimit=1&workyearFrom=-1&workyearTo=11&workyearUnlimit=1&salary=&salaryUnPublic=1&propertyList=1&gender=&age=&',
            'http://s.job5156.com/s/p/result?keywordType=0&keyword=%E5%A4%96%E8%B4%B8&locationList=14013000&posTypeList=&industryList=&updateIn=90&degreeFrom=1&degreeTo=8&degreeUnlimit=1&workyearFrom=-1&workyearTo=11&workyearUnlimit=1&salary=&salaryUnPublic=1&propertyList=1&gender=&age=&']
        for i in lists:
            self.run(i+'pn=')
        self.f.close()
    def run(self,hname):
        for page in range(5):
            try:
                lists=self.spider(page,hname)
            except:
                break
            w=self.write(lists)

    def write(self,lists):
        for i in lists:
            self.f.write(i.find('div', attrs = {'class' : 't1'}).find('a').get('title')+' ')
            self.f.write(i.find('div', attrs = {'class' : 't2'}).find('a', attrs = {'class' : 'comName'}).get('title')+' ')
            self.f.write(i.find('div', attrs = {'class' : 't2'}).find('span').get_text().replace('\n', ' ').lstrip() + '\n\n')
    def spider(self,page,hname):
        html=self.session.get(hname,headers=self.headers).text
        soup = BeautifulSoup(html)
        table = soup.find('div', attrs = {'id' : 'js_jobSearch'})
        lists = table.find_all('div', attrs = {'class' : 'postItem'})
        return lists

class Job_cn():
    def __init__(self):
        self.session=requests.session()
        self.f = open('job_cn.txt', 'w', encoding = 'utf-8')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def run(self):
        for page in range(4):
            try:
                lists=self.spider(page)
            except:
                continue
            w=self.write(lists)
        self.f.close()
    def write(self,lists):
        for i in lists:
            self.f.write(i.find('h4', attrs = {'class' : 'job_name'}).get_text().replace('\n',' '))
            self.f.write(i.find('div', attrs = {'class' : 'job_info'}).find('a').get('title').replace('\n',' ')+'   ')
            get_id = i.find('a',attrs={'class':'job_check '}).get('data-value')
            html = requests.get('http://www.jobcn.com/search/position_detail.uhtml?ids='+get_id,headers=self.headers).text
            soup = BeautifulSoup(html)
            self.f.write(soup.find('div',attrs={'class':'gl_wk'}).get_text().replace('工作地址：','')+'\n\n')
    def spider(self,page):
        html=requests.get('http://www.jobcn.com/search/result.xhtml?s=search%2Findex&p.sortBy=default&p.jobLocationId=3002&p.jobLocationTown=%C6%F3%CA%AF%D5%F2%3B%C7%C5%CD%B7%D5%F2%3B%D5%C1%C4%BE%CD%B7%D5%F2%3B%B4%F3%C1%EB%C9%BD%D5%F2%3B%C7%E5%CF%AA%D5%F2%3B%CC%C1%CF%C3%D5%F2%3B%BB%A2%C3%C5%D5%F2%3B%B7%EF%B8%DA%D5%F2%3B%B3%A4%B0%B2%D5%F2%3B%B3%A3%C6%BD%D5%F2&p.jobLocationTownId=300209%2C300211%2C300215%2C300216%2C300220%2C300223%2C300224%2C300226%2C300227%2C300230&p.keyword=%CD%E2%C3%B3&p.keywordType=2#P'+str(page+1),headers=self.headers).text
        soup = BeautifulSoup(html)
        table = soup.find('form', attrs = {'id' : 'result_data'})
        lists = table.find_all('div', attrs = {'class' : 'item_box'})
        return lists


class Job_51():
    def __init__(self):
        self.f = open('job_51.txt', 'w', encoding = 'utf-8')
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': 1,
            'Connection': 'keep-alive'}
    def work(self):
        self.run('09', 1)
        self.run('11', 1)
        self.run('20', 1)
        self.run('21', 1)
        self.run('25', 1)
        self.run('28', 1)
        self.run('29', 1)
        self.run('31', 1)
        self.run('32', 1)
        self.f.close()
    def run(self,name,x):
        for page in range(x):
            try:
                lists=self.spider(name,page)
            except:
                continue
            self.write(lists)
    def write(self,lists):
        for i in lists:
            self.f.write(i.find('td', attrs = {'class' : 'td1'}).find('a').get_text().replace('\n',' ')+'  ')
            self.f.write(i.find('td', attrs = {'class' : 'td2'}).find('a').get_text().replace('\n',' ')+'  ')
            self.f.write(i.find('td', attrs = {'class' : 'td3'}).get_text()+'\n\n')
    def spider(self,name,page):
        html=requests.get('http://search.51job.com/list/030800,0308'+name+',0000,00,9,99,%25CD%25E2%25C3%25B3,1,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=01&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&confirmdate=9&fromType=17',headers=self.headers).text.encode('ISO-8859-1').decode('gb2312','ignore')
        soup = BeautifulSoup(html)
        table = soup.find('table', attrs = {'id' : 'resultList'})
        lists = table.find_all('tr', attrs = {'class' : 'tr0'})
        return lists

class Job_get():
    def run(self):
        ganji=Ganji()
        ganji.work()
        print("Ganji OK")
        job_51=Job_51()
        job_51.work()
        print("job_51 OK")
        job_58=Job_58()
        job_58.work()
        print("job_58 OK")
        job_5156=Job_5156()
        job_5156.final()
        print("job_5156 OK")
        job_cn=Job_cn()
        job_cn.run()
        print("job_cn OK")

if __name__=='__main__':
    while True:
        work=Job_get()
        work.run()
        print("sleep...")
        time.sleep(600)
