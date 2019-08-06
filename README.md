# CODEF API - Python
Python sample for CODEF API

## Documentation

본 샘플은 CODEF API의 연동을 위한 공통 코드를 포함하고 있으며, 지원하는 모든 API의 엔드포인트(은행, 카드, 보험, 증권, 공공, 기타)는
https://develpers.codef.io 를 통해 확인할 수 있습니다.

## CODEF API Env

CODEF API는 원활한 개발을 위해 샌드박스, 개발, 운영 환경을 각각 제공한다.

- 샌드박스 : https://sandbox.codef.io
- 개발 : https://development.codef.io
- 운영 : https://api.codef.io

## Getting Started


### OAuth2.0

CODEF API를 사용하기 위해서는 'access_token' 발행이 선행되어야 하며, 거래 시 Header 에 포함하여 요청합니다.  
'access_token'을 발급 받기 위한 'client_id' 및 'client_secret'은 https://codef.io/#/account/keys 에서 확인할 수 있습니다.  
발급받은 access_token은 **모든 CODEF API 호출 시 Headers 에 추가**되어야 합니다. ('Authorization': 'Bearer ' + access_token)

* **access_token은 일주일간 유효**합니다. 데이터베이스나 글로벌 변수에 저장하여 재사용하는 것을 권장합니다. 
* CODEF API를 호출 할 때마다 access_token을 요청하는 것은 퍼포먼스에 부정적입니다.
* 권장하는 흐름은 다음과 같습니다. [1.토큰 발급 -> 2.토큰 저장 -> 3.저장된 토큰을 이용하여 API 호출 -> 4.토큰이 유효하지 않을경우 토큰 재발급 -> 5.API 재시도]

```python
token_url = 'https://oauth.codef.io/oauth/token'
response_oauth = request_token(token_url, 'CODEF로부터 발급받은 클라이언트 아이디', 'CODEF로부터 발급받은 시크릿 키')
if response_oauth.status_code == 200:
    dict = json.loads(response_oauth.text)
    # reissue_token
    token = dict['access_token']

    print('access_token = ' + token)
else:
    print('토큰발급 오류')
```
```json
{
  "access_token" : "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX3R5cGUiOiIwIiwic2NvcGUiOlsicmVhZCJdLCJzZXJ2aWNlX25vIjoiMDAwMDAwMDQyMDAxIiwiZXhwIjoxNTYzOTQ4NDQ2LCJhdXRob3JpdGllcyI6WyJJTlNVUkFOQ0UiLCJQVUJMSUMiLCJCQU5LIiwiRVRDIiwiU1RPQ0siLCJDQVJEIl0sImp0aSI6Ijc4NDUyMjY4LWFkNDctNGVhNS04ZjljLTQ5ZWI5Yjk1YmQxZCIsImNsaWVudF9pZCI6ImNvZGVmX21hc3RlciJ9.ddZ38ARfTIa4_E8by6gITeIadhQKeDDG4YoGQdGiu-n2sJ1iQ7z81dsMJtc9-YYV-ItIcEn5OXqnIZlGaeF8Ya6Jqy6XdrIb8ou5Sq-jYoB6UXyQRzQsV_1oIIXYSeQtQKalSpPbGGOgLaXsm61fBKimFnnCd1anhxtZAIHwCLMbvQCZlwOeTls1F1EEOvQ76qcdUcmsw-LHM_9I68DwjIwAjyOTe4WPMhsK6KD4MryCAfZRAmdRhG6BWVKk_8D1JPFy42qQmILAr9LXOMODqnVaNeGA-izmtfX5KqqdYxAR6XV_7B9muzYPyGnBL_l2pEcLq5kVSL7YGtczwqB-AA",
  "scope" : "read",
  "token_type" : "bearer",
  "expires_in" : 604799
}
```


### 계정 생성

CODEF API를 사용하기 위해서는 엔드유저가 사용하는 대상기관의 인증수단 등록이 필요하며, 이를 통해 사용자마다 유니크한 'connectedId'를 발급받을 수 있습니다.
이후에는 별도의 인증수단 전송 없이 'connectedId'를 통해서 대상기관의 데이터를 연동할 수 있습니다. 'connectedId' 발급은 최초 계정 생성 요청시에만 가능하며 이후에 엔드유저의 인증수단 관리는 계정 추가, 계정 수정, 계정 삭제 거래를 이용해야 합니다.

* 은행/카드 업무의 경우 동일한 기관에 등록 가능한 인증수단은 개인 고객/기업 고객 각각 1건입니다.
* API서버를 향한 모든 요청 파라미터는 URLEncoder를 통해 UTF-8로 인코딩되어야 합니다. (RegisterAccount.py 참조)
* 계정 생성 시 포함되는 모든 비밀번호는 API 호출 시 발급된 publicKey 를 통해 암호화 후 전송해야 합니다.

```python
codef_account_create_url = 'https://api.codef.io/account/create'
codef_account_create_body = {
            'accountList':[                    # 계정목록
                {
                    'countryCode':'KR',        # 국가코드
                    'businessType':'BK',       # 비즈니스 구분
                    'clientType':'P',          # 고객구분(P: 개인, B: 기업)
                    'organization':'0003',     # 기관코드
                    'loginType':'0',           # 로그인타입 (0: 인증서, 1: ID/PW)
                    'password':publicEncRSA(pubKey, '1234'),    # 엔드유저의 인증서 비밀번호 입력
                    'derFile':'MIIF...',                        # 엔드유저의 인증서 인증서 DerFile
                    'keyFile':'MIIF...'                         # 엔드유저의 인증서 인증서 KeyFile
                },
                {
                    'countryCode':'KR',        # 국가코드
                    'businessType':'BK',       # 비즈니스 구분
                    'clientType':'P',          # 고객구분(P: 개인, B: 기업)
                    'organization':'0004',     # 기관코드
                    'loginType':'0',           # 로그인타입 (0: 인증서, 1: ID/PW)
                    'password':publicEncRSA(pubKey, '1234'),    # 엔드유저의 인증서 비밀번호 입력
                    'derFile':'MIIF...',                        # 엔드유저의 인증서 인증서 DerFile
                    'keyFile':'MIIF...'                         # 엔드유저의 인증서 인증서 KeyFile
                }
            ]
}

# CODEF API 호출
response_account_create = http_sender(codef_account_create_url, token, codef_account_create_body)
```
```python
import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

def publicEncRSA(publicKey, data):
    keyDER = base64.b64decode(pubKey)
    keyPub = RSA.importKey(keyDER)
    cipher = Cipher_PKCS1_v1_5.new(keyPub)
    cipher_text = cipher.encrypt(data.encode())

    encryptedData = base64.b64encode(cipher_text)
    print('encryptedData = ' + encryptedData)

    return encryptedData
```
```json
{
  "result" : {
    "code" : "CF-00000",
    "extraMessage" : "",
    "message" : "정상"
  },
  "data" : {
    "successList" : [ {
      "clientType" : "P",
      "code" : "CF-00000",
      "loginType" : "0",
      "countryCode" : "KR",
      "organization" : "0003",
      "businessType" : "BK",
      "message" : "성공"
    }, {
      "clientType" : "P",
      "code" : "CF-00000",
      "loginType" : "1",
      "countryCode" : "KR",
      "organization" : "0004",
      "businessType" : "BK",
      "message" : "성공"
    } ],
    "errorList" : [ ],
    "connectedId" : "45t4DJOD44M9uwH7zxSgBg"
  }
}
```


### 계정 추가

계정 생성을 통해 발급받은 'connectedId'에 추가 기관의 인증수단을 등록할 수 있습니다. 추가 등록한 기관을 포함하여 이후에는 별도의 인증수단 전송없이
'connectedId'를 통해서 대상기관의 데이터를 연동할 수 있습니다.

* 은행/카드 업무의 경우 동일한 기관에 등록 가능한 인증수단은 개인 고객/기업 고객 각각 1건입니다.
* API서버를 향한 모든 요청 파라미터는 URLEncoder를 통해 UTF-8로 인코딩되어야 합니다. (RegisterAccount.py 참조)

```python
codef_account_add_url = 'https://api.codef.io/account/add'
codef_account_add_body = {
            'connectedId': '엔드유저의 은행/카드사 계정 등록 후 발급받은 커넥티드아이디 입력',    # connectedId
            'accountList':[                  # 계정목록
              {
                  'countryCode':'KR',        # 국가코드
                  'businessType':'BK',       # 비즈니스 구분
                  'clientType':'P',          # 고객구분(P: 개인, B: 기업)
                  'organization':'0020',     # 기관코드
                  'loginType':'0',           # 로그인타입 (0: 인증서, 1: ID/PW)
                  'password':publicEncRSA(pubKey, '1234'),    # 엔드유저의 인증서 비밀번호 입력
                  'derFile':'MIIF...',                        # 엔드유저의 인증서 인증서 DerFile
                  'keyFile':'MIIF...'                         # 엔드유저의 인증서 인증서 KeyFile
              }
            ]
}

# CODEF API 호출
response_account_add = http_sender(codef_account_add_url, token, codef_account_add_body)
```
```json
{
  "result" : {
    "code" : "CF-00000",
    "extraMessage" : "",
    "message" : "정상"
  },
  "data" : {
    "successList" : [ {
      "clientType" : "P",
      "code" : "CF-00000",
      "loginType" : "0",
      "countryCode" : "KR",
      "organization" : "0020",
      "businessType" : "BK",
      "message" : "성공"
    } ],
    "errorList" : [ ],
    "connectedId" : "45t4DJOD44M9uwH7zxSgBg"
  }
}
```


### 계정 수정

계정 생성을 통해 발급받은 'connectedId'에 등록된 기관의 인증수단을 변경할 수 있습니다. 변경 요청한 기관의 인증 수단은 호출 즉시 변경되며, 이 후
'connectedId'를 통해서 대상기관의 데이터를 연동할 수 있습니다.

* API서버를 향한 모든 요청 파라미터는 URLEncoder를 통해 UTF-8로 인코딩되어야 합니다. (RegisterAccount.py 참조)

```python
codef_account_update_url = 'https://api.codef.io/account/update'
codef_account_update_body = {
            'connectedId': '계정생성 시 발급받은 아이디',    # connectedId
            'accountList':[                    # 계정목록
                {
                    'countryCode':'KR',        # 국가코드
                    'businessType':'BK',       # 비즈니스 구분
                    'clientType':'P',          # 고객구분(P: 개인, B: 기업)
                    'organization':'0020',     # 기관코드
                    'loginType':'0',           # 로그인타입 (0: 인증서, 1: ID/PW)
                    'password':publicEncRSA(pubKey, '1234'),    # 엔드유저의 인증서 비밀번호 입력   
                    'derFile':'인증서 DerFile',  # Base64String
                    'keyFile':'인증서 KeyFile'   # Base64String
                }
            ]
}

# CODEF API 호출
response_account_update = http_sender(codef_account_update_url, token, codef_account_update_body)
```
```json
{
  "result" : {
    "code" : "CF-00000",
    "extraMessage" : "",
    "message" : "정상"
  },
  "data" : {
    "successList" : [ {
      "clientType" : "P",
      "code" : "CF-00000",
      "loginType" : "0",
      "countryCode" : "KR",
      "organization" : "0020",
      "businessType" : "BK",
      "message" : "성공"
    } ],
    "errorList" : [ ],
    "connectedId" : "45t4DJOD44M9uwH7zxSgBg"
  }
}
```


### 계정 삭제

엔드유저가 등록된 계정의 삭제를 요청 시 'connectedId'에 등록된 기관의 인증수단을 즉시 삭제할 수 있습니다. 요청한 기관의 인증 수단은 호출 즉시 삭제되며,
해당 데이터는 복구할 수 없습니다.

* API서버를 향한 모든 요청 파라미터는 URLEncoder를 통해 UTF-8로 인코딩되어야 합니다. (RegisterAccount.py 참조)

```python
codef_account_delete_url = 'https://api.codef.io/account/delete'
codef_account_delete_body = {
            'connectedId': '계정생성 시 발급받은 아이디',    # connectedId
            'accountList':[                    # 계정목록
                {
                    'countryCode':'KR',        # 국가코드
                    'businessType':'BK',       # 비즈니스 구분
                    'clientType':'P',          # 고객구분(P: 개인, B: 기업)
                    'organization':'0020',     # 기관코드
                    'loginType':'0',           # 로그인타입 (0: 인증서, 1: ID/PW)
                }
            ]
}

# CODEF API 호출
response_account_delete = http_sender(codef_account_delete_url, token, codef_account_delete_body)
```
```json
{
  "result" : {
    "code" : "CF-00000",
    "extraMessage" : "",
    "message" : "정상"
  },
  "data" : {
    "successList" : [ {
      "clientType" : "P",
      "loginType" : "0",
      "countryCode" : "KR",
      "organization" : "0020",
      "businessType" : "BK"
    } ],
    "connectedId" : "45t4DJOD44M9uwH7zxSgBg"
  }
}
```


### 계정 목록 조회

계정 등록, 추가 등을 통해 CODEF에 등록된 엔드 유저의 인증수단 정보 목록에 대한 조회를 요청할 수 있습니다. 엔드유저에 대한 유니크한 식별값인 'connectedId'를 요청 파라미터로 사용하며 해당 'connectedId'에 연결된 인증수단 정보 목록을 반환합니다.

* API서버를 향한 모든 요청 파라미터는 URLEncoder를 통해 UTF-8로 인코딩되어야 합니다. (AccountList.py 참조)

```python
codef_account_list_url = 'https://api.codef.io/v1/account/list'
codef_account_list_body = {
    'connectedId':connectedId          # 엔드유저의 은행/카드사 계정 등록 후 발급받은 커넥티드아이디 예시
}

# CODEF API 호출
response_account_list = http_sender(codef_account_list_url, token, codef_account_list_body)
```
```json
{
  "result" : {
    "code" : "CF-00000",
    "extraMessage" : "",
    "message" : "성공"
  },
  "data" : {
    "accountList" : [ {
      "clientType" : "B",
      "organizationCode" : "0003",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "BK"
    }, {
      "clientType" : "B",
      "organizationCode" : "0004",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "BK"
    }, {
      "clientType" : "P",
      "organizationCode" : "0004",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "BK"
    }, {
      "clientType" : "B",
      "organizationCode" : "0011",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "BK"
    }, {
      "clientType" : "P",
      "organizationCode" : "0020",
      "loginType" : "1",
      "countryCode" : "KR",
      "businessType" : "BK"
    }, {
      "clientType" : "B",
      "organizationCode" : "0301",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "CD"
    }, {
      "clientType" : "P",
      "organizationCode" : "0302",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "CD"
    }, {
      "clientType" : "B",
      "organizationCode" : "0309",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "CD"
    }, {
      "clientType" : "P",
      "organizationCode" : "0309",
      "loginType" : "0",
      "countryCode" : "KR",
      "businessType" : "CD"
    } ],
    "connectedId" : "bybF-S85kX998Trh23JUVb"
  }
}
```


### 'connectedId' 목록 조회

CODEF로부터 발급된 'connectedId'의 목록에 대한 조회를 요청할 수 있습니다. 요청 결과는 페이징(5만건) 단위로 전송되며 결과 값(hasNext == true)에 따라 다음 페이지(nextPageNo)에 대한 요청이 가능합니다.

* API서버를 향한 모든 요청 파라미터는 URLEncoder를 통해 UTF-8로 인코딩되어야 합니다. (ConnectedIdList.py 참조)

```python
codef_connectedId_list_url = 'https://api.codef.io/v1/account/connectedId-list'
codef_connectedId_list_body = {
    'pageNo':'5'            # 페이지 번호(생략 가능) 생략시 1페이지 값(0) 자동 설정
}

# CODEF API 호출
response_connectedId_list = http_sender(codef_connectedId_list_url, token, codef_connectedId_list_body)
```
```json
{
  "result" : {
    "code" : "CF-00000",
    "extraMessage" : "",
    "message" : "성공"
  },
  "data" : {
    "connectedIdList" : [ "6OOOZ58zAU.aX0pRRgzEBk", "bybF-S85kX998Trh23JUVb" ],
    "pageNo" : 0,
    "hasNext" : true,
    "nextPageNo" : 1
  }
}
```


### CODEF API(법인 보유계좌조회)

발급받은 'connectedId' 를 통해 등록된 기관의 보유계좌를 조회할 수 있습니다.

* API서버를 향한 모든 요청 파라미터는 URLEncoder를 통해 UTF-8로 인코딩되어야 합니다. (TestKR_BK_1_B_001.py 참조)

TestKR_BK_1_B_001.py
```python
# CodefURL
codef_url = 'https://api.codef.io'
token_url = 'https://api.codef.io/oauth/token'

# 은행 법인 보유계좌
account_list_path = '/v1/kr/bank/b/account/list'

# 기 발급된 토큰
token =''     #access_token

# BodyData
body = {
    'connectedId':'9LUm.uhVQbzaangazwI0tr',
    'organization':'0011'
}

# CODEF API 요청
response_codef_api = http_sender(codef_url + account_list_path, token, body)

# token error
if response_codef_api.status_code == 401:
    dict = json.loads(response_codef_api.text)
    # invalid_token
    print('error = ' + dict['error'])
    # Cannot convert access token to JSON
    print('error_description = ' + dict['error_description'])

    # reissue token
    response_oauth = request_token(token_url, 'CODEF로부터 발급받은 클라이언트 아이디', 'CODEF로부터 발급받은 시크릿 키');
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
    print('정상처리')
```
```json
{
	"result": {
		"code": "CF-00000",
		"extraMessage": "",
		"message": "성공",
		"transactionId": "aedb0cade44f44e48a5f3181c2fe9a96"
	},
	"data": {
		"resAccountEndDate": "",
		"resLoanLimitAmt": "",
		"resWithdrawalAmt": "19615",
		"resAccount": "05300000004040",
		"resAccountStatus": "활동",
		"resLoanEndDate": "",
		"commEndDate": "20190630",
		"resInterestRate": "",
		"resAccountName": "OO기업자유예금",
		"resAccountStartDate": "20130605",
		"resAccountCurrency": "KRW",
		"resAccountBalance": "19615",
		"commStartDate": "20190401",
		"resTrHistoryList": [
			{
				"resAccountTrTime": "095900",
				"resAccountDesc4": "",
				"resAccountDesc3": "ｒｎｄ＿오전",
				"resAccountDesc2": "인터넷",
				"resAccountDesc1": "（주）OO",
				"resAccountTrDate": "20190628",
				"resAccountOut": "1",
				"resAfterTranBalance": "13634",
				"resAccountIn": "0"
			},
			{
				"resAccountTrTime": "174603",
				"resAccountDesc4": "",
				"resAccountDesc3": "rnd_입금표시1",
				"resAccountDesc2": "타행이체",
				"resAccountDesc1": "OO（주）",
				"resAccountTrDate": "20190627",
				"resAccountOut": "0",
				"resAfterTranBalance": "13635",
				"resAccountIn": "1"
			},
			{
				"resAccountTrTime": "164618",
				"resAccountDesc4": "",
				"resAccountDesc3": "rnd_입금표시1",
				"resAccountDesc2": "타행이체",
				"resAccountDesc1": "OO（주）",
				"resAccountTrDate": "20190627",
				"resAccountOut": "0",
				"resAfterTranBalance": "13634",
				"resAccountIn": "1"
			},
			{
				"resAccountTrTime": "092130",
				"resAccountDesc4": "",
				"resAccountDesc3": "ｒｎｄ＿오전",
				"resAccountDesc2": "인터넷",
				"resAccountDesc1": "（주）OO",
				"resAccountTrDate": "20190627",
				"resAccountOut": "1",
				"resAfterTranBalance": "13633",
				"resAccountIn": "0"
			}
		],
		"resAccountHolder": "(주)OO",
		"resManagementBranch": "(0044)북아현동",
		"resLastTranDate": "20190711"
	}
}
```


### 오류

CODEF API 오류는 HTTP status code 와 CODEF API ErrorCode로 분류합니다.

HTTP 401 - OAuth2.0 토큰 만료
```json
{"error":"invalid_token","error_description":"Cannot convert access token to JSON","code":"CF-99997","message":"OAUTH2.0 토큰 에러입니다. 메시지를 확인하세요."}
```

그 외 오류 HTTP 200 - CODEF 오류 변환(CF-XXXXX)
```json
{"result":{"code":"CF-94002","extraMessage":"","message":"사용자 계정정보 설정에 실패했습니다."},"data":{}}
```


## Change Log

CODEF API의 변경내을 [CHANGELOG.md](CHANGELOG.md) 을 통해 확인할 수 있습니다.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
