# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

######################################
##      카드 개인  승인내역 조회
######################################


import requests, json, base64
import urllib

# ========== HTTP 기본 함수 ==========

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
        'Acceppt': 'application/json',
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

# CodefURL
codef_url = 'https://development.codef.io'
token_url = 'https://oauth.codef.io/oauth/token'

# 카드 개인  승인내역 조회
approval_list_path = '/v1/kr/card/p/account/approval-list'

# 기 발급된 토큰
token =''

# BodyData
body = {
    'connectedId':'엔드유저의 은행/카드사 계정 등록 후 발급받은 커넥티드아이디',
    'organization':'기관코드',
    'birthDate':'생년월일',
    'startDate':'조회시작일자',
    'endDate':'조회종료일자',
    'orderBy':'정렬기준',
    'inquiryType':'조회구분',
    'cardNo':'카드번호',
    'cardName':'카드명칭',
    'duplicateCardSelect':'중복카드선택',
    'duplicateCardIdx':'중복카드일련번호',
    'memberStoreInfoType':'가맹점정보포함여부'
}

# CODEF API 요청
response_codef_api = http_sender(codef_url + approval_list_path, token, body)

if response_codef_api.status_code == 200:
    dict = json.loads(urllib.parse.unquote_plus(response_account_create.text))
    print(urllib.parse.unquote_plus(response_account_create.text))
    if 'data' in dict and str(dict['data']) != '{}':
        print('조회 정상 처리')
    else:
        print('조회 오류')
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
        response = http_sender(codef_url + approval_list_path, token, body)
        if response.status_code == 200:      # success
            dict = json.loads(urllib.parse.unquote_plus(response.text))
            if 'data' in dict and str(dict['data']) != '{}':
                print('조회 정상 처리')
            else:
                print('조회 오류')
    else:
        print('토큰발급 오류')
else:
    print('조회 오류')
