# 載入需要的模組
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import configparser

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi('CevuEwc722zOiBwgCnJS8yYK12kEa0LVUnMQWlyOMkMNl95vRhZ40SNrCt1Dr3H4S8AgNnLWu7hwEB3f2nblSO/YkbhaItdAWFrUpE0b7Zv0aGuk5E8XCuZMV8RM5pNdipH67O87Nrx5xHUrs+HI0AdB04t89/1O/w1cDnyilFU='))
handler = WebhookHandler('53c3084b1fd0d433edcab1f0b8dd745d')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

if __name__ == "__main__":
    app.run()