from LogObjParser.handle_pattern import upload_regex_obj, upload_grok_obj

SUB_SIGN = "   #spec#   "


class LogParser:
    """ Object parsing log str obj """

    def __init__(self, data):
        self.log_data = data
        self.log_line = ""  # 로그 한 줄 -> 각 str obj 를 인식 후 구 log 줄에서 없애 주기 위함
        self.obj_data = list()  # parsing 한 str obj => 일단 리스트로 csv 에 넣어 주기 위함
        self.grok_patterns = upload_grok_obj()  # 사용할 grok patterns 객체들
        self.valid_path_regx = upload_regex_obj()  # file_path 검증에 사용할 regx 객체들

    def subtract_obj_from_string(self, sub_regex):
        """ Subtracting specific obj from log """

        self.log_line = sub_regex.sub(SUB_SIGN, self.log_line)

    @staticmethod
    def is_valid_path(string: str, valid_path_regx):
        """ Check if the file path is correct """

        if string and isinstance(string, str):
            for regx in valid_path_regx:
                if regx.match(string):
                    return True

        return False

    def get_valid_path(self, paths: list, valid_regx):
        """ Select only valid file paths """

        file_path = list()

        for path in paths:
            if self.is_valid_path(path[1:], valid_regx):
                if path[-1] == " ":
                    path = path[:-1]
                file_path.append(path[1:])

        return file_path

    def get_file_path(self):
        """" Get valid file path string object """

        path_regrex = self.grok_patterns["PATH"].regex_obj
        path_collection = (lambda fpath: list(fpath))(fp[0] for fp in path_regrex.findall(self.log_line))

        if path_collection:
            is_file_path = self.get_valid_path(path_collection, self.valid_path_regx.values())
            if not len(is_file_path):
                return "None"
        else:
            return "None"

        return is_file_path

    def get_time(self):
        """ Get valid time string object """

        is_time = self.grok_patterns["TIME"].match(self.log_line)

        if is_time:
            self.subtract_obj_from_string(self.grok_patterns["TIME"].regex_obj)
        else:
            return "None"

        return is_time

    def get_date(self):
        """ Get valid date string object """

        is_date = self.grok_patterns["DATE"].match(self.log_line)

        if is_date:
            self.subtract_obj_from_string(self.grok_patterns["DATE"].regex_obj)
        else:
            return "None"

        return is_date

    def get_uri(self):
        """ Get valid uri string object """

        is_uri = self.grok_patterns["URI"].match(self.log_line)

        if is_uri:
            self.subtract_obj_from_string(self.grok_patterns["URI"].regex_obj)
        else:
            return "None"

        return is_uri

    def get_ip(self):
        """ Get valid IP string object """

        is_ip = self.grok_patterns["IP"].match(self.log_line)

        if is_ip:
            self.subtract_obj_from_string(self.grok_patterns["IP"].regex_obj)
        else:
            return "None"

        return is_ip

    def parse(self):
        """ Parsing all log datas """

        self.obj_data.append(["Log", "Time", "Date", "Uri", "IP", "Path"])

        for log in self.log_data:
            self.log_line = log

            time = self.get_time()
            date = self.get_date()
            uri = self.get_uri()
            ip = self.get_ip()
            path = self.get_file_path()

            self.obj_data.append([log, time, date, uri, ip, path])

        return self.obj_data
