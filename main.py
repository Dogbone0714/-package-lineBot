import requests
import os
import re
import time
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime as dt
from bs4 import BeautifulSoup
from email.mime.image import MIMEImage
from pathlib import Path
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import pygsheets
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
# -----SleepTime-------
SLEEPTIME = 60*60*24    #60*60*24 # 每輪搜尋休眠時間
# ---------------------
flog = False # 判斷是否已尋找到目標用的
t = dt.datetime # 顯示時間用的

#------Line Notify------
def lineNotifyMessage(ID, msg):

    token = 'q3MP3UJKy4sv9mWOAjkueqfJTAre7jAmyH4QPcferhiYMhds1rN9bNa6bwqHg8C4Uw22L4/4u5yyu0nVW4se0N+fcsl94olc23eP5eyUgsPRA+6LIWKrEGfJkuBIvqyG2hzY0gb3IW/qRCfseaemCAdB04t89/1O/w1cDnyilFU=' # 權杖值
    line_bot_api = LineBotApi(token)
    line_bot_api.push_message(ID, TextSendMessage(text=msg))
# -----程式本體----------
def find_name(username,ID):
    s = requests.session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    url = s.get("https://doc.nuu.edu.tw/p/406-1079-13151,r369.php", verify=False)  # 讀二坪收發室網頁
    
    soup = BeautifulSoup(url.text, "html.parser") # 分析
    name = soup.find_all('div', class_="meditor") # 抓出所有 class = meditor 的元素
    name = name[1].text.lstrip()      # 只讀取主要 meditor 陣列，不讀取 footer 的 meditor  # lstrip 去除html元素
    
    for i in range(0,len(username)):
        print(username[i])
        print(ID[i])
        name_count = name.count(username[i]) # 計算名字出現次數
        print(name_count)
        if name_count > 0:
             message = username[i] + '~~尼的包裹已經到了收發室~~~\n記得去取件！' # 要傳送的訊息內容
             lineNotifyMessage(ID[i], message)
            
             print('[%s] 已發現監聽目標！%s 訊息已發出' %(t.now(),username[i]))
                
        else:
            print('\n[%s] 搜尋完畢，並未發現目標(%s)。正在休眠 %s 秒並等待下一輪搜尋……' %(t.now(),username[i], SLEEPTIME))

# ------主流程--------------------
def main():
    #try:
    while True:
        print('[%s] 開始執行監聽' %t.now())
        gc = pygsheets.authorize(service_account_file='focus-reality-141302-a2fb2c5a77fb.json')
        survey_url = 'https://docs.google.com/spreadsheets/d/1vWlaSBQxecmmdj40bPZxotqZD1a154nKwMP_Te51HAw/'
        sh = gc.open_by_url(survey_url)
        ws = sh.worksheet_by_title('ID')
        id_list = []
        name_list = []
        for i in range(2,10):
            val1 = ws.get_value('A' + str(i))
            val2 = ws.get_value('B' + str(i))
            if val1 != '' and val2 != '':
                id_list.append(val1)
                name_list.append(val2)
                print(val1 + val2)
        print(id_list)
        print(name_list)
        find_name(name_list,id_list)

        
        if  flog == True:
            print('[%s] 已發現目標，停止監聽' %t.now())
        break

# ----運行-------
if __name__ == "__main__":
    main()
    message = '~~尼的包裹已經到了收發室~~~\n記得去取件！' # 要傳送的訊息內容
    token = 'q3MP3UJKy4sv9mWOAjkueqfJTAre7jAmyH4QPcferhiYMhds1rN9bNa6bwqHg8C4Uw22L4/4u5yyu0nVW4se0N+fcsl94olc23eP5eyUgsPRA+6LIWKrEGfJkuBIvqyG2hzY0gb3IW/qRCfseaemCAdB04t89/1O/w1cDnyilFU=' # 權杖值
