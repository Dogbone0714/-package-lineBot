from flask import request
import json
import os, urllib

client_id = os.environ['YJUX55mHv95PBJd2HvBSDF']
client_secret = os.environ['GEpQUulTQ9GRZBrEqt3TgbbunA0gc0b13s2MzDsuxIC']
redirect_uri = f"https://{os.environ['package-linebot']}.herokuapp.com/callback/notify"

def create_auth_link(user_id, client_id=client_id, redirect_uri=redirect_uri):
    
    data = {
        'response_type': 'code', 
        'client_id': client_id, 
        'redirect_uri': redirect_uri, 
        'scope': 'notify', 
        'state': user_id
    }
    query_str = urllib.parse.urlencode(data)
    
    return f'https://notify-bot.line.me/oauth/authorize?{query_str}'


@app.route("/callback/notify", methods=['GET'])
def callback_nofity():
    assert request.headers['referer'] == 'https://notify-bot.line.me/'
    code = request.args.get('code')
    state = request.args.get('state')

    # 接下來要繼續實作的函式
    access_token = get_token(code, client_id, client_secret, redirect_uri)

    return '恭喜完成 LINE Notify 連動！請關閉此視窗。'


def get_token(code, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri):
    url = 'https://notify-bot.line.me/oauth/token'
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    page = urllib.request.urlopen(req).read()
    
    res = json.loads(page.decode('utf-8'))
    return res['access_token']

def send_message(access_token, text_message, picurl):

    url = 'https://notify-api.line.me/api/notify'
    headers = {"Authorization": "Bearer "+ access_token}

    data = {'message': text_message, 
            "stickerPackageId": 2, 'stickerId': 38, 
            'imageThumbnail':picurl, 'imageFullsize':picurl}

    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    page = urllib.request.urlopen(req).read()