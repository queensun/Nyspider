#coding:utf-8

import requests
from bs4 import BeautifulSoup
import time
import re
import random
import xlwt3

class Get_ip(object):
    """docstring for Get_ip"""
    def __init__(self):
        super(Get_ip, self).__init__()
        self.url='http://www.xicidaili.com/nn/'
        self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive'}
        self.session=requests.session()
    def run(self):
        html=self.session.get(self.url,headers=self.headers).text
        table=BeautifulSoup(html).find('table',attrs={'id':'ip_list'}).find_all('tr')
        http_ips=[]
        for item in table[1:]:
            lists=item.find_all('td')
            ip={'ip':'','port':''}
            if lists[6].get_text()=='HTTP':
                ip['ip']=lists[2].get_text()
                ip['port']=lists[3].get_text()
                http_ips.append(ip)
        return http_ips

class get_urls():
	def __init__(self,url,page,ip):
		self.page=page
		self.url=url
		self.proxies={
			'http':'http://'+ip['ip']+':'+ip['port']
		}
	def get_url(self):
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			
			'Connection': 'keep-alive'}
		html=requests.get(self.url+'&beginPage='+str(self.page),headers=headers,proxies=self.proxies,timeout=10).text
		soup=BeautifulSoup(html)
		table=soup.find('div',attrs={'id':'sw_mod_mainblock'}).find('ul').find_all('div',attrs={'class':'list-item-left'})
		urls=[]
		for item in table:
			urls.append(item.find('a').get('href'))
		return urls

class get_contact():
	def __init__(self,url,ip):
		#super(get_contact, self).__init__()
		self.proxies={
			'http':'http://'+ip['ip']+':'+ip['port']
		}
		self.url=url
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			
			'Accept-Encoding': 'gzip, deflate'
			}
		self.session=requests.session()
	def run(self):
		try:
			html=self.session.get(self.url,headers=self.headers,proxies=self.proxies,timeout=10).text
			contact_url=BeautifulSoup(html).find('div',attrs={'class':'top-nav-bar-box'}).find('li',attrs={'data-page-name':'contactinfo'}).find('a').get('href')
		except:
			self.statue=0
			print('~~~')
			return
		self.statue=1
		try:
			#time.sleep(random.randint(4, 6))
			html=self.session.get(contact_url,headers=self.headers,proxies=self.proxies,timeout=10).text
			table=BeautifulSoup(html).find('div',attrs={'class':'fd-line'}).find_all('dl')
			self.title=BeautifulSoup(html).find('div',attrs={'class':'contact-info'}).find('h4').get_text()
			self.infor=[]
			for item in table[:-1]:
				self.infor.append(item.get_text().replace('\n','').replace(' ',''))
		except:
			self.statue=0

class Main():
	def __init__(self):
		self.f=xlwt3.Workbook()
		self.sheet=self.f.add_sheet('sheet')
		self.count=0
		work=Get_ip()
		self.ips=work.run()
	def work(self):
		search_url=input('输入链接:')
		for i in range(100):
			url_get=get_urls(search_url,i+1,self.ips[random.randint(0, len(self.ips)-1)])
			try:
				urls=url_get.get_url()
			except:
				continue
			for url in urls:
				#time.sleep(random.randint(6, 9))
				spider=get_contact(url,self.ips[random.randint(0, len(self.ips)-1)])
				spider.run()
				if spider.statue==0:
					continue
				self.sheet.write(self.count,0,spider.title)
				num=1
				for infor in spider.infor:
					self.sheet.write(self.count,num,infor)
					num+=1
				self.count+=1
				print(self.count)
				self.f.save('data.xls')
			#time.sleep(random.randint(5, 8))
def test():
	test=get_urls('http://s.1688.com/company/company_search.htm?keywords=%BE%AB%C3%DC%BB%FA%D0%B5&earseDirect=false&button_click=top&n=y&pageSize=30',1)
	print(test.get_url())

if __name__=='__main__':
	work=Main()
	work.work()
