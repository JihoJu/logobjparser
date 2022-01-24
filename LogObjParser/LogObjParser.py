from LogObjParser.handle_pattern import upload_regex_obj, upload_grok_obj
from LogObjParser.handle_file import extract_log_from_path, output_obj_to_csv

SUB_SIGN = "   #spec#   "  # 각 obj 를 인식 후 해당 obj 자리 제거를 위한 string


class LogParser:
    """ Object parsing log str obj """

    def __init__(self, path):
        self.in_path = path  # param 으로 입력 받은 파일 or 디렉터리 path
        self.log_data = list()  # 로그 파일들 안에 있는 모든 log data 를 한 줄씩 모아둔 리스트
        self.log_line = ""  # 로그 한 줄 -> 각 str obj 를 인식 후 구 log 줄에서 없애 주기 위함
        self.obj_data = list()  # parsing 한 str obj => 일단 리스트 형태로 csv 에 넣어 주기 위함
        self.grok_patterns = upload_grok_obj()  # 사용할 grok patterns 객체들
        self.valid_path_regex = upload_regex_obj()  # file_path 검증에 사용할 regx 객체들

    def run(self):

        """
            LogParser 객체 main 함수

            - extract_log_from_path(self.in_path) : log_data 를 LogParser 객체 log_data 에 저장
            - output_obj_to_csv(self.parse()) : 각 str obj 인식 후 csv 파일에 저장
        """

        self.log_data = extract_log_from_path(self.in_path)
        if self.log_data is not None:  # 해당 경로에 파일 혹은 디렉터리가 존재
            output_obj_to_csv(self.parse())

        return 0

    def parse(self):

        """
            Parsing all log datas

            1. 모든 log data 를 한줄씩 읽는다.
            2. time -> date -> uri -> ip -> path 순으로 obj 를 인식
            3. 각 obj 를 인식한 후 log 에서 해당 obj 를 제거
            4. obj_data 에 각 obj 를 담아 csv 로 출력
        """

        self.obj_data.append(["Log", "Time", "Date", "Uri", "IP", "Path"])  # output data 에 첫 행 데이터 추가

        for log in self.log_data:
            self.log_line = log

            time = self.get_time()
            date = self.get_date()
            uri = self.get_uri()
            ip = self.get_ip()
            path = self.get_file_path()

            self.obj_data.append([log, time, date, uri, ip, path])

        return self.obj_data

    def subtract_obj_from_string(self, sub_regex):

        """
            Subtracting specific obj from log

            한 줄의 log data 에서 특정 obj 를 제거
        """

        self.log_line = sub_regex.sub(SUB_SIGN, self.log_line)

    @staticmethod
    def is_valid_path(string: str, valid_path_regex):

        """
            Check if the file path is correct

            valid file path 인지 판별
            valid : True 리턴
            invalid : False 리턴
        """

        if string and isinstance(string, str):
            for regx in valid_path_regex:
                if regx.match(string):
                    return True

        return False

    def get_valid_path(self, paths: list, valid_regx):

        """
            Select only valid file paths

            file_path : valid 한 file path 를 담기 위한 list
            paths: re.findall() 해서 뽑아온 모든 file path 후보
            valid_regex : 후보들 중 정말 file path 인지 판별을 위한 regex obj list

            path 후보가 file path 인지 판별 후 맞다면 path 의 마지막 문자가 " " 라면 공백 제거
        """

        file_path = list()

        for path in paths:
            if self.is_valid_path(path[1:], valid_regx):
                if path[-1] == " ":
                    path = path[:-1]
                file_path.append(path[1:])

        return file_path

    def get_file_path(self):

        """
            Get valid file path string object

            path_regrex : path obj 판별을 위한 grok pattern
            path_collection : re.findall() 시 리턴된 값은 다음과 같은 튜플 형태로 리턴 -> 이 중 첫번째 값만을 가진 리스트
                                            '/tmp/aa' -> ('/tmp/aa', '/tmp', '/aa', '/')
            is_file_path : path_collection 에 있는 후보 중 valid file path 를 담은 리스트
        """

        path_regrex = self.grok_patterns["PATH"].regex_obj
        path_collection = (lambda fpath: list(fpath))(fp[0] for fp in path_regrex.findall(self.log_line))

        if path_collection:
            is_file_path = self.get_valid_path(path_collection, self.valid_path_regex.values())
            if not len(is_file_path):
                return "None"
        else:
            return "None"

        return is_file_path

    def get_time(self):

        """
            Get valid time string object

            is_time : time obj 판별을 위한 grok pattern
            self.subtract_obj_from_string(self.grok_patterns["TIME"].regex_obj)
                : log data 에서 time obj 제거
        """

        is_time = self.grok_patterns["TIME"].match(self.log_line)

        if is_time:
            self.subtract_obj_from_string(self.grok_patterns["TIME"].regex_obj)
        else:
            return "None"

        return is_time

    def get_date(self):

        """
            Get valid date string object

            is_date : time obj 판별을 위한 grok pattern
            self.subtract_obj_from_string(self.grok_patterns["DATE"].regex_obj)
                : log data 에서 date obj 제거
        """

        is_date = self.grok_patterns["DATE"].match(self.log_line)

        if is_date:
            self.subtract_obj_from_string(self.grok_patterns["DATE"].regex_obj)
        else:
            return "None"

        return is_date

    def get_uri(self):

        """
            Get valid uri string object

            is_uri : time obj 판별을 위한 grok pattern
            self.subtract_obj_from_string(self.grok_patterns["URI"].regex_obj)
                : log data 에서 uri obj 제거
        """

        is_uri = self.grok_patterns["URI"].match(self.log_line)

        if is_uri:
            self.subtract_obj_from_string(self.grok_patterns["URI"].regex_obj)
        else:
            return "None"

        return is_uri

    def get_ip(self):

        """
            Get valid IP string object

            is_ip : time obj 판별을 위한 grok pattern
            self.subtract_obj_from_string(self.grok_patterns["IP"].regex_obj)
                : log data 에서 IP obj 제거
        """

        is_ip = self.grok_patterns["IP"].match(self.log_line)

        if is_ip:
            self.subtract_obj_from_string(self.grok_patterns["IP"].regex_obj)
        else:
            return "None"

        return is_ip
