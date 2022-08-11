import os
import re
from pygrok import Grok
import LogObjParser.handle_file as hf
from LogObjParser.pattern import PATH_GROK, DATE_GROK, upload_sub_path_regex, STRIP_PATH, MIMETYPE_REGEX, IP_GROK
from LogObjParser.parser import get_path_objs, get_ip_objs

SUB_SIGN = "   #spec#   "  # 각 obj 를 인식 후 해당 obj 자리 제거를 위한 string
SUBTRACT_PATH = re.compile(
    r"(\s([-=+,%#\?:\^.@*\"※~ㆍ!』\|\(\)\[\]…》·\w]+/[\w]+){1}[-=+,%#\?:\^.@*\"※~ㆍ!』‘\|\(\)\[\]`\'…》\”\“\’·|\s])|</\w*>|/>{1}|N/A"
)


def get_path_objs_for_analyzing(log: str, regex_obj):
    """
        기존에 구현한 path 인식 알고리즘과 분석을 하기 위한 함수

        무엇을?
        - path 인식 전 file path 가 아닌 객체 pattern 수정
        - SUBTRACT_PATH, DATE PATTERN 제거
    """
    sub_regex = upload_sub_path_regex()

    sub_regex["SUBTRACT_PATH_REGEX"] = SUBTRACT_PATH
    sub_regex["DATE"] = DATE_GROK.regex_obj

    # ip pattern 만으로 ip obj 를 subtract 하는게 아닌 get_ip_objs 함수로 걸러진 ip obj 를 subtract
    # => 정확도 상승을 위해
    del sub_regex["IP_REGEX"]
    is_ip_objs = get_ip_objs(log, IP_GROK.regex_obj)
    sub_log = log
    if is_ip_objs:
        for ip_obj in is_ip_objs:
            sub_log = sub_log.replace(ip_obj, SUB_SIGN)

    # file path obj 추출 전 URI, IP, 미리 제거 sub_path obj 제거
    for regex in sub_regex.values():
        sub_log = regex.sub(SUB_SIGN, sub_log)  # log data 에서 subtract 할 regex pattern 객체

    is_path_objs = regex_obj.findall(sub_log)

    if is_path_objs:
        parsed_path_objs = list()
        for obj in is_path_objs:
            # findall 로 리턴된 튜플 안에서 0번째 path 선택 & file path 처음 및 마지막 필요 없는 str obj 제거
            parsed_path_objs.append(obj[0].strip(STRIP_PATH))
        return parsed_path_objs

    return is_path_objs


class Path_Analysis:
    def __init__(self):
        self.result = list()

    def run(self, path):
        self.extract_log_from_path(path)
        self.identify_custom_file_path_pattern()
        self.identify_custom_file_path_pattern_for_analyzing()
        self.compare_result()
        hf.output_obj_to_csv(self.result, "./result/analysis/")

        return 0

    def extract_log_from_path(self, in_path: str):
        """
            Extract from the path to log data str object
        """

        if os.path.isfile(in_path):  # in_path 가 file 인 경우 : 파일 전체 log data
            self.extract_log_from_file(in_path)
        elif os.path.isdir(in_path):  # in_path 가 directory 인 경우 : 각 파일 50 줄 log data
            self.extract_log_from_dir(in_path)
        else:  # 해당 경로에 파일 혹은 디렉터리가 존재 X
            print("해당 경로에 파일 혹은 디렉터리가 존재하지 않습니다.")

    def extract_log_from_file(self, in_file: str):
        """
            Extract from a file to log data str object
        """
        self.result.append(["Where", "Log", "Existing", "New"])

        log_file = open(f"{in_file}", "rt")
        log_lines = log_file.readlines()
        for log in log_lines:
            self.result.append([log_file, log])

    def extract_log_from_dir(self, in_dir: str):
        """
            Extract from files in the directory path to log data str object
        """

        self.result.append(["Where", "Log", "Existing", "New"])
        files = hf.get_filenames(in_dir)
        for file in files:
            log_file = open(f"{in_dir}/{file}", "rt")
            log_lines = log_file.readlines()
            for log in log_lines:
                self.result.append([file, log])

    def identify_existing_file_path_pattern(self):
        existing_path_grok_pattern = "%{PATH:path}"
        existing_path_grok = Grok(existing_path_grok_pattern)

        for log in self.result[1:]:
            is_path_objs = list()
            find_path_objs = existing_path_grok.regex_obj.findall(log[1])
            for path_obj in find_path_objs:
                is_path_objs.append(path_obj[0])
            log.extend([is_path_objs])

    def identify_custom_file_path_pattern(self):
        for log in self.result[1:]:
            is_path_objs = get_path_objs(log[1], PATH_GROK.regex_obj)
            log.extend([is_path_objs])

    def identify_custom_file_path_pattern_for_analyzing(self):
        for log in self.result[1:]:
            is_path_objs = get_path_objs_for_analyzing(log[1], PATH_GROK.regex_obj)
            log.extend([is_path_objs])

    def identify_mime_type(self):
        for log in self.result[1:].copy():
            is_mime_objs = MIMETYPE_REGEX.findall(log[1])
            if is_mime_objs:
                is_mime_objs = [mime_obj[0] for mime_obj in is_mime_objs]
                log.extend([is_mime_objs])
            else:
                self.result.remove(log)

    def identify_ip_obj(self):
        for log in self.result[1:].copy():
            is_ip_objs = get_ip_objs(log[1], IP_GROK.regex_obj)
            if is_ip_objs:
                log.extend([is_ip_objs])
            else:
                self.result.remove(log)

    def compare_result(self):
        for data in self.result[1:].copy():
            if data[2] == data[3]:
                self.result.remove(data)
