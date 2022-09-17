from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction

line_bot_api = LineBotApi('53c3084b1fd0d433edcab1f0b8dd745d')
handler = WebhookHandler('CevuEwc722zOiBwgCnJS8yYK12kEa0LVUnMQWlyOMkMNl95vRhZ40SNrCt1Dr3H4S8AgNnLWu7hwEB3f2nblSO/YkbhaItdAWFrUpE0b7Zv0aGuk5E8XCuZMV8RM5pNdipH67O87Nrx5xHUrs+HI0AdB04t89/1O/w1cDnyilFU=')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def sendButton(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='遺失物檢索',
            template=ButtonsTemplate(
                title='遺失物檢索',  #主標題
                text='請選擇：',  #副標題
                actions=[
                    URITemplateAction(  #開啟網頁
                        label='連結網頁',
                        uri='http://www.e-happy.com.tw'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def handle_message(event):
    input_text = event.message.text

    if input_text == '您好，我的東西好像掉在你那':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='是的，這裡是陽光服飾店'))
    elif input_text == '我的東西掉了':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='是的，這裡是陽光服飾店'))
    elif input_text == '您好':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='是的，這裡是陽光服飾店'))
def handle_message(event):
    input_text = event.message.text

    if input_text == '方便現在去拿嗎':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='可以，到了請撥打0975982***這支電話'))
    elif input_text == '馬上過去拿':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='可以，到了請撥打0975982***這支電話'))
    elif input_text == '太好了':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='來拿時，請撥打0975982***這支電話'))
def handle_message(event):
    input_text = event.message.text

    if input_text == '謝謝':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='不客氣'))
    elif input_text == '感恩您':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='不客氣'))


if __name__ == '__main__':
    app.run()
