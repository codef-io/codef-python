# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

######################################
##      은행 법인 외화 거래내역
######################################


import requests, json, base64
import urllib

# ========== HTTP 기본 함수 ==========

def http_sender(url, token, body):
    headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
        }

    response = requests.post(url, headers = headers, data = urllib.parse.quote(str(json.dumps(body))))

    print('response.status_code = ' + str(response.status_code))
    print('response.text = ' + urllib.parse.unquote_plus(response.text))

    return response
# ========== HTTP 함수  ==========

# ========== Toekn 재발급  ==========
def request_token(url, client_id, client_secret):
    authHeader = stringToBase64(client_id + ':' + client_secret).decode("utf-8")

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + authHeader
        }

    response = requests.post(url, headers = headers, data = 'grant_type=client_credentials&scope=read')

    print(response.status_code)
    print(response.text)

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

# 은행 법인 외화 거래내역
transaction_list_path = '/v1/kr/bank/b/exchange/transaction-list'

# 기 발급된 토큰
token =''

# BodyData
body = {
    'connectedId':'sandbox_connectedId',     # 엔드유저의 은행/카드사 계정 등록 후 발급받은 커넥티드아이디 예시
    'organization':'0003',
    'account':'0530815995600000',
    'startDate':'20190401',
    'endDate':'20190630',
    'orderBy':'0',
    'currency':'USD'
}

# CODEF API 요청
response_codef_api = http_sender(CODEF_URL + transaction_list_path, token, body)

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
        response = http_sender(CODEF_URL + transaction_list_path, token, body)
    else:
        print('토큰발급 오류')
else:
    print('API 요청 오류')
