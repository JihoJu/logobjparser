from LogObjParser.handle_file import extract_log_from_path, output_obj_to_csv
from LogObjParser.parser import parse_log_data


# SUB_SIGN = "   #spec#   "  # 각 obj 를 인식 후 해당 obj 자리 제거를 위한 string


class LogParser:
    """ Object parsing log str obj """

    def __init__(self, path):
        self.in_path = path  # param 으로 입력 받은 파일 or 디렉터리 path
        self.log_data = list()  # 로그 파일들 안에 있는 모든 log data 를 한 줄씩 모아둔 리스트
        self.csv_data = list()  # parsing 한 str obj => 일단 리스트 형태로 csv 에 넣어 주기 위함

    def run(self):

        """
            LogParser 객체 main 함수

            - extract_log_from_path(self.in_path) : log_data 를 LogParser 객체 log_data 에 저장
            - output_obj_to_csv(self.parse()) : 각 str obj 인식 후 csv 파일에 저장
        """

        self.log_data = extract_log_from_path(self.in_path)
        if self.log_data is not None:  # 해당 경로에 파일 혹은 directory 존재
            output_obj_to_csv(self.parse())

        return 0

    def parse(self):

        """
            Parsing all log datas

            1. 모든 log data 를 한 줄씩 읽는다.
            2. "Time", "Date", "Uri", "IP", "Path" 에 해당 모든 objs 들을 추출
            3. parsed_data (OrderDict) 에 담겨진 str obj 만 뽑아서 list data type 인 data_in_csv 에 저장
            4. self.csv_data 에 parsing 된 obj 를 담아 csv 로 출력
        """

        self.csv_data.append(["Log", "Time", "Date", "Uri", "IP", "Path"])  # output data (in csv) 에 첫 행 데이터 추가

        for log in self.log_data:
            parsed_data = parse_log_data(log)  # LOG, TIME, URI, IP, PATH 에 대한 obj 들이 담긴 OrderDict 객체

            data_in_csv = [obj[1] for obj in list(parsed_data.items())]  # csv 각 행에 들어갈 log obj 리스트 데이터
            self.csv_data.append(data_in_csv)

        return self.csv_data
