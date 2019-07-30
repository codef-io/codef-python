# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

######################################
##      저축 은행 개인 보유계좌
######################################


import requests, json, base64
import urllib

# ========== HTTP 기본 함수 ==========

def http_sender(url, token, body):
    headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
        }

    response = requests.post(url, headers = headers, data = urllib.quote(json.dumps(body)))

    print('response.status_code = ' + str(response.status_code))
    print('response.text = ' + urllib.unquote_plus(response.text.encode('utf8')))

    return response
# ========== HTTP 함수  ==========

# ========== Toekn 재발급  ==========
def request_token(url, client_id, client_secret):
    authHeader = stringToBase64(client_id + ':' + client_secret)

    headers = {
        'Acceppt': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + authHeader
        }

    response = requests.post(url, headers = headers, data = 'grant_type=client_credentials&scope=read')

    print('response.status_code = ' + str(response.status_code))
    print('response.text = ' + urllib.unquote_plus(response.text.encode('utf8')))

    return response
# ========== Toekn 재발급  ==========

# ========== Encode string data  ==========
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
# ========== Encode string data  ==========

# CodefURL
codef_url = 'https://tapi.codef.io'
token_url = 'https://toauth.codef.io/oauth/token'

# 저축 은행 개인 보유계좌
account_list_path = '/v1/kr/bank2/p/account/account-list'

# 기 발급된 토큰
token =''

# BodyData
body = {
    'connectedId':'9LUm.uhVQbzaangazwI0tr',     // 엔드유저의 은행/카드사 계정 등록 후 발급받은 커넥티드아이디 예시
    'organization':'기관코드',
    'bankName':'<저축은행 중앙회 모듈 필수: [서브도메인 명]>'
}

# CODEF API 요청
response_codef_api = http_sender(codef_url + account_list_path, token, body)

if response_codef_api.status_code == 200:
    print('정상처리')
# token error
elif response_codef_api.status_code == 401:
    dict = json.loads(response_codef_api.text)
    # invalid_token
    print('error = ' + dict['error'])
    # Cannot convert access token to JSON
    print('error_description = ' + dict['error_description'])

    # reissue token
    response_oauth = request_token(token_url, 'CODEF로부터 발급받은 클라이언트 아이디', 'CODEF로부터 발급받은 시크릿 키')
    if response_oauth.status_code == 200:
        dict = json.loads(response_oauth.text)
        # reissue_token
        token = dict['access_token']
        print('access_token = ' + token)

        # request codef_api
        response = http_sender(codef_url + account_list_path, token, body)

        # codef_api 응답 결과
        print(response.status_code)
        print(response.text)
    else:
        print('토큰발급 오류')
else:
    print('API 요청 오류')
