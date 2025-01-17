# logobjparser 
Identify known string objects from logs.<br> 
Known string objects are: Time, Date, IP address, XML, Json, file path, json, xml...etc

## Data

- cassandra - 51,318개
- mongodb - 144,269개
- hadoop - 222,955개
- openstack - 420,554개
- spark - 150,530개
- test - 440,963개

## Parsing

- **Time**, **Date**, **IP address**, **URI** Object
  - pygrok Library 를 사용했습니다.
  - grok pattern 활용하여 custom grok pattern 만든 후 이를 활용했습니다.
- **File path** Object
  - 데이터 레이블링 작업 후, Bert 모델를 활용해 file path 판별 로직을 구현 중에 있습니다.
- **Json** Object
  - log data 에서 Parenthesis('{', '}') 가 valid 한 경우를 json 이라 가정합니다.
  - json format 이라 가정한 object 가 정말 json format 인지를 검증 과정 수행합니다.
- **XML** Object
  - 현재까진 well-defined XML 만 parsing 가능합니다.

## Testing

git clone 후 logobjparser 폴더 안에서 다음 명령어 수행

- path 가 file 인 경우: file 내 모든 log data
- path 가 directory 인 경우: directory 내 모든 파일 내 log data 2만줄씩
```
# setup 설치
pip install --editable . 

# logparser 실행 cli
parser --path=<파일 or 디렉터리 경로>
parser -p <파일 or 디렉터리 경로>

# 예시
parser --path="./logdata"
parser -p "./logdata"
```
  