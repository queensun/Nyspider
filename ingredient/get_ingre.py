#coding:utf-8

import requests
from bs4 import BeautifulSoup
import xlwt3

class Get_ingredient():
    def __init__(self):
        self.session=requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
        self.f=xlwt3.Workbook()
        self.sheet=self.f.add_sheet('sheet')
        self.count=0
    def get_infor(self):
        for page in range(899):
            html=self.session.get('http://www.ewg.org/skindeep/search.php?search_group=ingredients&query=.&order=webscore+INC&&showmore=ingredients&start='+str(page*10),headers=self.headers).text
            ingredients=BeautifulSoup(html).find('table',attrs={'id':'table-browse'}).find_all('tr')
            for item in ingredients[0:]:
                try:
                    name=item.find('td',attrs={'align':'left'}).find('a').get_text()
                except:
                    continue
                score=item.find_all('td',attrs={'align':'center'})[1].find('img').get('src').replace('http://static.ewg.org/skindeep/img/draw_score/score_image','')
                if score[0]==score[2]:
                    score=score[0]
                else:
                    score=str(score[2])+'-'+str(score[0])
                self.sheet.write(self.count,0,score)
                self.sheet.write(self.count,1,name)
                self.count+=1
            self.f.save('ingredient.xls')
            print(page)

if __name__=='__main__':
    work=Get_ingredient()
    work.get_infor()
