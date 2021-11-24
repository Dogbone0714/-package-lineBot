###############################
#                             #
#        Coded By HHK         #
#                             #
###############################

# 套件
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
# -----SleepTime-------
SLEEPTIME = 60*60*24    #60*60*24 # 每輪搜尋休眠時間
# ---------------------
flog = False # 判斷是否已尋找到目標用的
t = dt.datetime # 顯示時間用的
# -------Mail ---------------
''' def send_mail_for_me():
    # '利用 Gmail 的服務寄發通知信'
    send_gmail_user = 'nuupackage@gmail.com'
    send_gmail_password = 'lruvafvdkrfabbkx'
    rece_gmail_user = 'jameskang0714@gmail.com'
    msg = MIMEText('康康~~尼的包裹已經到了收發室~~~\n記得去取件！')
    msg['Subject'] = '聯大收發室包裹到貨通知'
    msg['From'] = send_gmail_user
    msg['To'] = rece_gmail_user

    # 使用 SSL 加密 連線到 gmail 提供的 smtp
    ssl_version=ssl.PROTOCOL_TLS
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(send_gmail_user, send_gmail_password)
    server.send_message(msg)
    server.quit()'''

#------Line Notify------
def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    massage = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = massage)
    return r.status_code
# -----程式本體----------
def find_name(username):
    url = requests.get(
        "https://doc.nuu.edu.tw/p/406-1079-13151,r369.php")  # 讀二坪收發室網頁
    soup = BeautifulSoup(url.text, "html.parser") # 分析
    name = soup.find_all('div', class_="meditor") # 抓出所有 class = meditor 的元素
    name = name[1].text.lstrip()      # 只讀取主要 meditor 陣列，不讀取 footer 的 meditor  # lstrip 去除html元素
    name_count = name.count(username) # 計算名字出現次數

    if name_count > 0:
        lineNotifyMessage()
        print('[%s] 已發現監聽目標！Mail 已發出' %t.now())
            
    else:
        print('\n[%s] 搜尋完畢，並未發現目標。正在休眠 %s 秒並等待下一輪搜尋……' %(t.now(), SLEEPTIME))
        time.sleep(SLEEPTIME)    
# ------主流程--------------------
def main():
    try:
        while True:
            print('[%s] 開始執行監聽' %t.now())

            find_name(username='康皓雄') # 開始執行搜索

            if  flog == True:
                print('[%s] 已發現目標，停止監聽' %t.now())
                break
            else:
                time.sleep(SLEEPTIME)
    except Exception as e:
        print('[%s] 執行期間錯誤：%s' %(t.now(), e))
# ----運行-------
if __name__ == "__main__":
    main()
    message = '康康~~尼的包裹已經到了收發室~~~\n記得去取件！' # 要傳送的訊息內容
    token = '' # 權杖值

    lineNotifyMessage(token, message)