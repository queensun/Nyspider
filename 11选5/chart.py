#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3
import os
import time

class Get_infor():
	def __init__(self):
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive'}
		self.urls={'北京11选5': 'http://pub.icaile.com/bj11x5kjjg.php', '新疆11选5': 'http://pub.icaile.com/xj11x5kjjg.php', '湖北11选5': 'http://pub.icaile.com/hb11x5kjjg.php', '江西11选5': 'http://pub.icaile.com/jx11x5kjjg.php', '山西11选5': 'http://pub.icaile.com/sx11x5kjjg.php', '宁夏11选5': 'http://pub.icaile.com/nx11x5kjjg.php', '辽宁11选5': 'http://pub.icaile.com/ln11x5kjjg.php', '贵州11选5': 'http://pub.icaile.com/gz11x5kjjg.php', '云南11选5': 'http://pub.icaile.com/yn11x5kjjg.php', '西藏11选5': 'http://pub.icaile.com/xz11x5kjjg.php', '重庆11选5': 'http://pub.icaile.com/cq11x5kjjg.php', '吉林11选5': 'http://pub.icaile.com/jl11x5kjjg.php', '黑龙江11选5': 'http://pub.icaile.com/hlj11x5kjjg.php', '河南11选5': 'http://pub.icaile.com/hn11x5kjjg.php', '上海11选5': 'http://pub.icaile.com/sh11x5kjjg.php', '广东11选5': 'http://pub.icaile.com/gd11x5kjjg.php', '四川11选5': 'http://pub.icaile.com/sc11x5kjjg.php', '山东11选5': 'http://pub.icaile.com/sd11x5kjjg.php', '安徽11选5': 'http://pub.icaile.com/ah11x5kjjg.php', '浙江11选5': 'http://pub.icaile.com/zj11x5kjjg.php', '江苏11选5': 'http://pub.icaile.com/js11x5kjjg.php', '内蒙古11选5': 'http://pub.icaile.com/nmg11x5kjjg.php', '甘肃11选5': 'http://pub.icaile.com/gs11x5kjjg.php', '福建11选5': 'http://pub.icaile.com/fj11x5kjjg.php', '河北11选5': 'http://pub.icaile.com/heb11x5kjjg.php', '广西11选5': 'http://pub.icaile.com/gx11x5kjjg.php', '天津11选5': 'http://pub.icaile.com/tj11x5kjjg.php', '陕西11选5': 'http://pub.icaile.com/shx11x5kjjg.php'}
	def run(self):
		try:
			os.mkdir('data')
		except:
			print('..')
		for key in self.urls:
			try:
				html=requests.get(self.urls[key],headers=self.headers).text
			except:
				continue
			table=BeautifulSoup(html,'html.parser').find('table',attrs={'class':'today'}).find_all('tr')
			self.f=xlwt3.Workbook()
			self.sheet=self.f.add_sheet('sheet')
			self.count=0
			for item in table:
				try:
					infor=item.find_all('td')
					self.sheet.write(self.count,0,infor[0].get_text())
					num=1
					for i in infor[2].find_all('em'):
						self.sheet.write(self.count,num,i.get_text())
						num+=1
					self.count+=1
				except:
					continue
			self.f.save('data/'+key+'.xls')
def test():
	html=requests.get('http://pub.icaile.com/sd11x5kjjg.php').text
	table=BeautifulSoup(html).find('div',attrs={'class':'left-nav'}).find('ul').find_all('li')
	urls={}
	for i in table:
		urls[i.get_text()]=i.find('a').get('href')
	print(urls)

if __name__=='__main__':
	print('1.直接抓取')
	print('2.定时抓取')
	num=input('输入序号：')
	if(num=='1'):
		work=Get_infor()
		work.run()
		print('OK')
	elif(num=='2'):
		times=input('输入间隔时间（小时）：')
		while True:
			work=Get_infor()
			work.run()
			print('OK')
			time.sleep(float(times)*3600)
