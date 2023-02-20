# -*- codeing = utf-8 -*-
# @Time : 2022/8/13 16:35
# @Author : 吕默存
# @File : app.py
# @Software: PyCharm
import time
import sys
import sys,os
sys.path.append(os.getcwd())
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from backend.infocore import infoextractor

core=infoextractor()
def getinfo(url):
    # core=infoextractor()
    # result=core.infoget('http://static.cninfo.com.cn/finalpage/2023-01-19/1215668073.PDF')
    # print(result)
    #输入为url输出为有关公告的信息
    result=core.infoget(url)
    return result
    # print(result)
    # print(type(result))

app = Flask(__name__)

@app.route('/')
def news_list():

    news_dataframe=pd.read_csv('./cash/infodataframe.csv')
    news_dataframe['time'] = news_dataframe['time'].apply(lambda x: x[:10])
    news_list=[dict(row) for index , row in news_dataframe.iterrows()]
    # print(news_list)
    return render_template('index.html', news_list=news_list)

@app.route('/news', methods=['GET'])
def view_news():
    news_url = request.args.get('url')
    title=request.args.get('title')
    tempresult,tempresult1=getinfo(news_url)
    result=[]
    for i in list(tempresult[0].keys()):
        result.append([i,tempresult[0][i][0]['text']])
    # result={'title':tempresult[0]['公告内容'][0]['text'],'summary':tempresult[1]['result'][0]['value'],'event':tempresult[2]['result'][0]['value']}
    result.append(['内容提要',tempresult1[0]])
    print(result)
    # 在这里获取新闻的详细信息，然后返回一个渲染后的页面
    return render_template('news.html', info=result,title=title)

#getinfo('http://static.cninfo.com.cn/finalpage/2023-01-19/1215668073.PDF')
app.run(host = "127.0.0.1", port = int("1214"))

