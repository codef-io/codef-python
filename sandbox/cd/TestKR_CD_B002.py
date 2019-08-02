# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

######################################
##      카드 법인 승인내역 조회
######################################


import requests, json, base64
import urllib

# ========== HTTP 기본 함수 ==========

def http_sender(url, token, body):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    response = requests.post(url, headers=headers, data=urllib.parse.quote(json.dumps(body)))

    print('response.status_code = ' + str(response.status_code))
    print('response.text = ' + urllib.parse.unquote_plus(response.text, encoding='utf-8'))

    return response
# ========== HTTP 함수  ==========

# ========== Toekn 재발급  ==========
def request_token(url, client_id, client_secret):
    authHeader = stringToBase64(client_id + ':' + client_secret)

    headers = {
        'Acceppt': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + authHeader.decode('utf-8')
        }

    response = requests.post(url, headers=headers, data='grant_type=client_credentials&scope=read')

    print('response.status_code = ' + str(response.status_code))
    print('response.text = ' + urllib.parse.unquote_plus(response.text, encoding='utf-8'))

    return response
# ========== Toekn 재발급  ==========

# ========== Encode string data  ==========
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
# ========== Encode string data  ==========

# API서버 샌드박스 도메인
CODEF_URL = 'https://tsandbox.codef.io';
TOKEN_URL = 'https://toauth.codef.io/oauth/token';
SANDBOX_CLIENT_ID 	= 'ef27cfaa-10c1-4470-adac-60ba476273f9';        # CODEF 샌드박스 클라이언트 아이디
SANDBOX_SECERET_KEY 	= '83160c33-9045-4915-86d8-809473cdf5c3';    # CODEF 샌드박스 클라이언트 시크릿

# 카드 법인 승인내역 조회
approval_list_path = '/v1/kr/card/b/account/approval-list'

# 기 발급된 토큰
token =''

# BodyData
body = {
    'connectedId':'sandbox_connectedId',
    'organization':'0301',
    'identity':'1138630000',
    'startDate':'20190101',
    'endDate':'20190331',
    'orderBy':'0',
    'inquiryType':'0',
    'cardNo':'426586******0000',
    'cardName':'',
    'duplicateCardSelect':'',
    'duplicateCardIdx':'',
    'memberStoreInfoType':'0'
}

# CODEF API 요청
response_codef_api = http_sender(CODEF_URL + approval_list_path, token, body)

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
    response_oauth = request_token(TOKEN_URL, SANDBOX_CLIENT_ID, SANDBOX_SECERET_KEY);
    if response_oauth.status_code == 200:
        dict = json.loads(response_oauth.text)
        # reissue_token
        token = dict['access_token']
        print('access_token = ' + token)

        # request codef_api
        response = http_sender(CODEF_URL + approval_list_path, token, body)

        # codef_api 응답 결과
        print(response.status_code)
        print(response.text)
    else:
        print('토큰발급 오류')
else:
    print('API 요청 오류')
