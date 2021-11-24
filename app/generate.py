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