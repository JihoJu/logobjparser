import os
from pygrok import Grok
import LogObjParser.handle_file as hf
from LogObjParser.pattern import PATH_GROK
from LogObjParser.parser import get_path_objs


class Path_Analysis:
    def __init__(self):
        self.result = list()

    def run(self, path):
        self.extract_log_from_path(path)
        self.identify_existing_file_path_pattern()
        self.identify_custom_file_path_pattern()
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
        self.result.append(["Where", "Log", "Existing", "Custom"])

        log_file = open(f"{in_file}", "rt")
        log_lines = log_file.readlines()
        for log in log_lines:
            self.result.append([log_file, log])

    def extract_log_from_dir(self, in_dir: str):
        """
            Extract from files in the directory path to log data str object
        """

        self.result.append(["Where", "Log", "Existing", "Custom"])
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

    def compare_result(self):
        for data in self.result[1:].copy():
            if data[2] == data[3]:
                self.result.remove(data)
