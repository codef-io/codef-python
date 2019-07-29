# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
#######################################
##      계정목록조회
######################################
import requests, json, base64
import urllib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

# ========== HTTP 기본 함수 ==========

def http_sender(url, token, body):
    headers = {'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
        }

    response = requests.post(url, headers = headers, data = urllib.quote(str(json.dumps(body))))

    # print('//////////////// = ' + urllib.urlencode(json.dumps(body)))
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
    print('response.text = ' + response.text)

    return response
# ========== Toekn 재발급  ==========

# ========== Encode string data  ==========
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
# ========== Encode string data  ==========

# token URL
token_url = 'https://toauth.codef.io/oauth/token'

# CODEF 연결 아이디
connected_id = '엔드유저의 은행/카드사 계정 등록 후 발급받은 커넥티드아이디'

# 기 발급된 토큰
token =''
##############################################################################
##                               계정목록조회                                  ##
##############################################################################
# Input Param
#
# connectedId : 페이지 번호(생략 가능) 생략시 1페이지 값(0) 자동 설정
#
##############################################################################
codef_account_list_url = 'https://tapi.codef.io/v1/account/list'
codef_account_list_body = {
    'connectedId':connected_id          # 엔드유저의 은행/카드사 계정 등록 후 발급받은 커넥티드아이디 예시
}

response_account_list = http_sender(codef_account_list_url, token, codef_account_list_body)
if response_account_list.status_code == 200:      # success
    dict = json.loads(urllib.unquote_plus(response_account_list.text.encode('utf8')))
    if 'data' in dict and str(dict['data']) != '{}':
        print('조회 정상 처리')
    else:
        print('조회 오류')
elif response_account_list.status_code == 401:      # token error
    dict = json.loads(response_account_list.text)
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

        # request codef_api
        response = http_sender(codef_account_list_url, token, codef_account_list_body)
        if response.status_code == 200:      # success
            dict = json.loads(urllib.unquote_plus(response.text.encode('utf8')))
            if 'data' in dict and str(dict['data']) != '{}':
                print('조회 정상 처리')
            else:
                print('조회 오류')
    else:
        print('토큰발급 오류')
else:
    print('조회 오류')
