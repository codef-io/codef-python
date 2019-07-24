# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

######################################
##      계정 목록 조회
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

    print(response.status_code)
    print(response.text)

    return response
# ========== Toekn 재발급  ==========

# ========== Toekn 재발급  ==========
def publicEncRSA(publicKey, data):
    keyDER = base64.b64decode(pubKey)
    keyPub = RSA.importKey(keyDER)
    cipher = Cipher_PKCS1_v1_5.new(keyPub)
    cipher_text = cipher.encrypt(data.encode())

    encryptedData = base64.b64encode(cipher_text)
    print('encryptedData = ' + encryptedData)

    return encryptedData
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
connected_id = 'CODEF로부터 계정등록 시 발급받은 connectedId'

# 기 발급된 토큰
token =''

pubKey = 'CODEF로부터 발급받은 publicKey'
##############################################################################
##                               계정 생성 Sample                             ##
##############################################################################
# Input Param
#
# accountList : 계정목록
#   countryCode : 국가코드
#   businessType : 비즈니스 구분
#   clientType : 고객구분(P: 개인, B: 기업)
#   organization : 기관코드
#   loginType : 로그인타입 (0: 인증서, 1: ID/PW)
#   password : 인증서 비밀번호
#   derFile : 인증서 derFile
#   keyFile : 인증서 keyFile
#
##############################################################################
print('=============================== 계정목록 ===============================')


# encryptedPassword = encrypt = pubkey.encrypt(message.encode(), 32)
codef_account_create_url = 'https://tapi.codef.io/v1/account/list'
# codef_account_create_url = 'http://192.168.10.126:8101/v1/account/create'
codef_account_create_body = {
            'connectedId':connected_id
}

response_account_create = http_sender(codef_account_create_url, token, codef_account_create_body)
if response_account_create.status_code == 200:      # success
    dict = json.loads(urllib.unquote_plus(response_account_create.text.encode('utf8')))
    print(urllib.unquote_plus(response_account_create.text.encode('utf8')))
    if 'data' in dict and str(dict['data']) != '{}':
        print('조회 정상 처리')
    else:
        print('조회 오류')
elif response_account_create.status_code == 401:      # token error
    dict = json.loads(response_account_create.text)
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
        response = http_sender(codef_account_create_url, token, codef_account_create_body)
        if response.status_code == 200:      # success
            dict = json.loads(urllib.unquote_plus(response.text.encode('utf8')))
            print(urllib.unquote_plus(response_account_create.text.encode('utf8')))
            if 'data' in dict and str(dict['data']) != '{}':
                print('조회 정상 처리')
            else:
                print('조회 오류')
    else:
        print('토큰발급 오류')
else:
    print('조회 오류')
