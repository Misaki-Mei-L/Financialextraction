import datetime

from backend.infocore import infoextractor
from cninfospider import spyder
import schedule
import time

import sys,os
sys.path.append(os.getcwd())
#初始化数据提取核心以及数据爬取模组
cnspyder=spyder()
def getdata():
    today= datetime.date.today()
    start_date=(today-datetime.timedelta(days=9)).strftime('%Y-%m-%d')
    data_str=today.strftime('%Y-%m-%d')
    return f'{start_date}~{data_str}'

def main():
    dateinfo=getdata()
    infodataframe = cnspyder.extractdata(date=dateinfo, cate='风险提示', searchkey='')
    cnspyder.ereasdata()
    #print(infodataframe)
    infodataframe.to_csv('./cash/infodataframe.csv',index=False)

if __name__ == '__main__':


    # cnspyder=spyder()
    # result=cnspyder.extractdata(date='2023-01-19~2023-01-19', cate='增发', searchkey='')
    # print(result)
    # result = cnspyder.extractdata(date='2023-01-19~2023-01-19', cate='业绩预告', searchkey='')
    # print(result)
    # print(cnspyder.data)

    # 每小时运行一次main函数
    main()
    os.system('python ./app/app.py')
    # schedule.every().hour.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)







