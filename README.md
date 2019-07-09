# CODEF API - Python
Python sample for CODEF API

## Documentation

본 샘플은 CODEF API의 연동을 위한 공통 코드를 포함하고 있으며, 지원하는 모든 API의 엔드포인트(은행, 카드, 보험, 증권, 공공, 기타)는
https://develpers.codef.io/abcd 를 통해 확인할 수 있습니다.

## Getting Started

### 계정 생성

CODEF API를 사용하기 위해서는 엔드유저가 사용하는 대상기관의 인증수단 등록이 필요하며, 이를 통해 사용자마다 유니크한 connected_id를 발급받을 수 있습니다.
이후에는 별도의 인증수단 전송 없이 connected_id를 통해서 대상기관의 데이터를 연동할 수 있습니다.

```python
codef_account_create_url = 'https://codef.io/account/create'
codef_account_create_body = {
            'accountList':[                    # 계정목록
                {
                    'organization':'0003',     # 기관코드
                    'loginType':'0',           # 로그인타입 (0: 인증서, 1: ID/PW)
                    'password':'1234',         # 인증서 비밀번호             
                    'derFile':'인증서 DerFile',  # Base64String
                    'keyFile':'인증서 KeyFile'   # Base64String
                }
            ]
}

# CODEF API 호출
response_account_create = http_sender(codef_account_create_url, token, codef_account_create_body)

...

# request codef_api
response_account_create = http_sender(codef_account_create_url, token, codef_account_create_body)
dict = json.loads(urllib.unquote_plus(response.text.encode('utf8')))
connected_id = dict['data']['connectedId']
```

### 계정 추가

계정 생성을 통해 발급받은 connected_id에 추가 기관의 인증수단을 등록할 수 있습니다. 추가 등록한 기관을 포함하여 이후에는 별도의 인증수단 전송없이
connected_id를 통해서 대상기관의 데이터를 연동할 수 있습니다.

```python
codef_account_add_url = 'https://codef.io/account/add'
codef_account_add_body = {
            'connectedId': '계정생성 시 발급받은 아이디',    # connected_id
            'accountList':[                    # 계정목록
                {
                    'organization':'0003',     # 기관코드
                    'loginType':'0',           # 로그인타입 (0: 인증서, 1: ID/PW)
                    'password':'1234',         # 인증서 비밀번호             
                    'derFile':'인증서 DerFile',  # Base64String
                    'keyFile':'인증서 KeyFile'   # Base64String
                }
            ]
}

# CODEF API 호출
response_account_add = http_sender(codef_account_add_url, token, codef_account_add_body)

...

# request codef_api
response_account_add = http_sender(codef_account_add_url, token, codef_account_add_body)
```

### 계정 수정

### 계정 삭제


각 엔드포인트는 JSON을 포함한 HTTP 응답을 리턴합니다.

### Errors

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
