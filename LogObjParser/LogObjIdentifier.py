from collections import OrderedDict
from difflib import SequenceMatcher
from LogObjParser.handle_pattern import upload_regex_obj, upload_grok_obj
from LogObjParser.handle_file import extract_log_from_path, output_obj_to_csv


class LogIdentifier:
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
            - output_obj_to_csv(self.recognize_all_obj()) : 각 str obj 들을 인식 후 csv 파일에 저장
        """

        self.log_data = extract_log_from_path(self.in_path)
        if self.log_data is not None:  # 해당 경로에 파일 혹은 디렉터리 존재
            output_obj_to_csv(self.recognize_all_obj())  # issue4 를 위한 실행 코드

        return 0

    def display_char_position_overlapping_part_by_ratio(self, param_data: OrderedDict):

        """
            Time, Date, IP, URI, File path 순으로 겹치는 부분이 있다면
            해당 부분을 dict 으로 생성 후 overlapping list 에 추가

            * overlapping 판단 기준 : SequenceMatcher 의 ratio 가 0.5 이상인 경우를 overlapping 이라 가정

            :param:
                param_data => OrderedDict([('TIME', []), ('DATE', []), ('URI', []), ('IP', []), ('PATH', [])])
                obj_data_list => [('TIME', []), ('DATE', []), ('URI', []), ('IP', []), ('PATH', [])]
                comp_obj : 비교 obj 변수 (comparison)
            :return:
        """

        obj_data_list = list(param_data.items())  # dict -> tuple list
        overlap_list = list()  # overlap info 가 담기는 List

        for index, curr_obj in enumerate(obj_data_list[:-1]):
            if len(curr_obj[1]) == 0:
                continue
            for comp_obj in obj_data_list[index + 1:]:
                if len(comp_obj[1]) == 0:
                    continue
                for curr_str in curr_obj[1]:
                    for comp_str in comp_obj[1]:
                        ratio = SequenceMatcher(None, curr_str, comp_str).ratio()
                        if ratio >= 0.5:
                            overlap_list.append({curr_obj[0]: curr_str,
                                                 comp_obj[0]: comp_str, "ratio": ratio})

        return overlap_list

    def display_char_position_overlapping_part_by_in(self, param_data: OrderedDict):
        """
            Time, Date, IP, URI, File path 순으로 겹치는 부분이 있다면
            해당 부분을 dict 으로 생성 후 overlapping list 에 추가

            * overlapping 판단 기준 : 인식된 obj 를 띄어 쓰기 구분 후 해당 부분이 다른 obj 에 포함이 될 경우!!

            :param:
                param_data => OrderedDict([('TIME', []), ('DATE', []), ('URI', []), ('IP', []), ('PATH', [])])
                obj_data_list => [('TIME', []), ('DATE', []), ('URI', []), ('IP', []), ('PATH', [])]
                comp_obj : 비교 obj 변수 (comparison)
            :return:
        """

        obj_data_list = list(param_data.items())  # dict -> tuple list
        overlap_list = list()  # overlap info 가 담기는 List

        for index, curr_obj in enumerate(reversed(obj_data_list)):
            if len(curr_obj[1]) == 0:
                continue
            for comp_obj in obj_data_list[0:-(index + 1)]:
                if len(comp_obj[1]) == 0:
                    continue
                for curr_str in curr_obj[1]:
                    split_curr_str = curr_str.split(" ")
                    for split_str in split_curr_str:
                        if split_str.isdigit():  # 숫자만 있는 경우 (예) time : "17:18", path : "17" -> 방지
                            continue
                        for comp_str in comp_obj[1]:
                            if split_str in comp_str:
                                overlap_list.append({curr_obj[0]: curr_str, comp_obj[0]: comp_str})

        return overlap_list

    def recognize_all_obj(self):

        """
            Time, Date, file path, URL 등을 각 로그 별로 인식 method
        """
        self.obj_data.append(
            ["Log", "Time", "Date", "URI", "IP", "Path", "Overlapping Position"])  # output data 에 첫 행 데이터 추가

        obj_list = ["TIME", "DATE", "URI", "IP", "PATH"]

        for log in self.log_data:
            input_data = list()  # obj_data 에 추가될 리스트 (엑셀 기준: 행)
            self.log_line = log

            input_data.append(self.log_line)  # Log 열 부분에 들어갈 log 한 줄 데이터

            # TIME ~ PATH 돌면서 findall 로 추출된 각 objs 를 input_data 에 순서대로 추가
            for obj in obj_list:
                recognized_objs = self.get_regrex_findall_objs(obj)
                input_data.append(recognized_objs)

            # display_char_position_overlapping_part 에 넘겨줄 인자로 obj name 과 해당 obj list 를 매칭 후 dict 형태로 구성
            arg_data = OrderedDict()
            for index, obj_name in enumerate(obj_list):
                arg_data[obj_name] = input_data[index + 1]

            # input data 에 overlapping position data 를 추가
            input_data.append(self.display_char_position_overlapping_part_by_in(arg_data))  # log 한 줄 데이터 빼고 전달

            self.obj_data.append(input_data)

        return self.obj_data

    def get_regrex_findall_objs(self, obj_name: str):

        """
            각 obj_name regrex pattern 을 log 한 줄을 findall 하여 리턴

            :param obj_name: 이미 생성한 grok pattern 을 구별을 위함
            :return: log 한 줄에 해당 regrex findall 리스트
        """

        return_obj_list = list()
        obj_regrex = self.grok_patterns[obj_name].regex_obj

        is_objs = obj_regrex.findall(self.log_line)
        if is_objs:
            for is_obj in is_objs:
                if obj_name == "PATH":
                    return_obj_list.append(
                        is_obj[0][1:].rstrip())  # findall 로 리턴된 튜플 안에서 1번째 path 가 가장 정확 (거의 대부분 앞에 =, " " 등 삭제)
                elif obj_name == "IP":
                    is_ip = is_obj[0].strip()
                    if is_ip[0] == '"' or is_ip[0] == "=":  # IP 의 경우 string 첫번째 문자가 ", = 경우가 있어 제거
                        is_ip = is_ip[1:]
                    return_obj_list.append(is_ip)
                else:
                    return_obj_list.append(is_obj[0].strip())

        return return_obj_list
