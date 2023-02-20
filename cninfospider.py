from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import os
import _sqlite3
import requests
import pandas as pd
from lxml import html
import ssl
from bs4 import BeautifulSoup
import os
import json
from lxml import etree
import csv
import time
from datetime import datetime
import fitz
from PIL import Image
from paddlenlp import Taskflow


class spyder:
    def __init__(self):
        self.data=pd.DataFrame()
    def getHTMLtext(self,url, pageNum=1, date='2023-01-19~2023-01-19', category='category_zf_szsh', searchkey=''):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'Cookie': 'JSESSIONID=5744E2AB53F37D89B404F8BD816DBEED; insert_cookie=45380249; _sp_ses.2141=*; routeId=.uc2; _sp_id.2141=a47ba3dd-0d05-4956-a752-91aac848786a.1673853622.2.1674125485.1673853684.1654d1f7-1a0e-4c1f-acba-923e51264e9c',
                'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search'
            }
            # params={'method': 'DataList'}
            data = {
                'pageNum': str(pageNum),
                'pageSize': '30',
                'column': 'szse',
                'tabName': 'fulltext',
                'plate': '',
                'stock': '',
                'searchkey': searchkey,
                'secid': '',
                'category': category,
                'trade': '',
                'seDate': date,
                'sortName': '',
                'sortType': '',
                'isHLtitle': 'true'
            }

            r = requests.post(url, headers=headers, data=data)
            # print(type(r))
            # print(r.raise_for_status())
            r.encoding = r.apparent_encoding
            # print(r.encoding)
            data = json.loads(r.text)
            # print(data)
            return data
        except:
            return ""

    def getalldata(self,url, date='2023-01-19~2023-01-19', cate='增发', searchkey=''):
        catedict = {'增发': 'category_zf_szsh',
                    '业绩预告': 'category_yjygjxz_szsh',
                    '风险提示':'category_fxts_szsh'}
        informationlist = []
        categoary = catedict[cate]
        fistpagedatadict = self.getHTMLtext(url=url, pageNum=1, date=date, category=categoary, searchkey=searchkey)
        for j in fistpagedatadict['announcements']:
            informationlist.append(j)
        totalnumber = (fistpagedatadict['totalAnnouncement'] // 30) + 1
        if totalnumber == 1:
            return informationlist
        else:
            for i in range(2, totalnumber + 1):
                datadict = self.getHTMLtext(url=url, pageNum=i, date=date, category=categoary)
                for j in datadict['announcements']:
                    informationlist.append(j)
            return informationlist

    def datapraser(self,datalist):
        df = pd.DataFrame()
        for andict in datalist:
            if andict['adjunctType'] == 'PDF':
                stockcode = andict['secCode']
                stockname = andict['secName']
                time = datetime.fromtimestamp(int(andict['announcementTime']) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                announcementTitle = andict['announcementTitle']
                docturl = 'http://static.cninfo.com.cn/' + andict['adjunctUrl']
                df = pd.concat([df, pd.DataFrame({'stockcode': stockcode, 'stockname': stockname, 'time': time,
                                                  'announcementTitle': announcementTitle, 'docturl': docturl},
                                                 index=[0])], ignore_index=True)

        return df
    def extractdata(self,date='2023-01-19~2023-01-19', cate='增发', searchkey=''):
        quaryurl = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
        list1 = self.getalldata(quaryurl, date=date, cate=cate, searchkey=searchkey)
        df = self.datapraser(list1)
        self.data=pd.concat([self.data, df], ignore_index=True)
        return df
    def ereasdata(self):
        self.data=pd.DataFrame()



if __name__ == '__main__':
    # print(extractdata(cate='业绩预告'))
    # extractdata(cate='业绩预告').to_csv('demodata.csv')
    cnspyder=spyder()



    cnspyder.extractdata()
    print(cnspyder.data)






