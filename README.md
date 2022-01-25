# logobjparser
#### Identify known string objects from logs. Known string objects are: Time, Date, IP address, XML, Json, file path ... etc.

# Testing 방법

git clone 후 logobjparser 폴더 안에서 다음 명령어 수행
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

- 가상환경 : anaconda (다른 가상환경이라도 상관 X)
- python version : 3.8.11

# 설명

#### Parameter path

- path 가 file 인 경우: file 내 모든 log data
- path 가 directory 인 경우: directory 내 모든 파일 내 log data 50줄씩

#### Parsing 과정

log data 각 로그 한 줄씩 읽은 후 시간, 날짜, uri, ip, file path 순으로 str obj 를 인식 후 csv 파일에 저장