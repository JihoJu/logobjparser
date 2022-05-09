from collections import OrderedDict
from LogObjParser.handle_pattern import upload_grok_obj, upload_sub_path_regex, upload_sub_ip_regex, SUBTRACT_TIME_GROK
import ast
import json

SUB_SIGN = "   #spec#   "  # 각 obj 를 인식 후 해당 obj 자리 제거를 위한 string
TYPE_OBJ = ["TIME", "DATE", "URI", "IP", "PATH", "JSON"]


def parse_log_data(log: str):
    """
    로그 data 한 줄을 입력 시
    - "TIME", "DATE", "URI", "IP", "PATH" 등
    각 type 에 해당 obj 들을 identifying 후 json 형식 표현을 위해 dict data structure 에 저장

        :param log: log data 한 줄, type: str
        :return: "TIME", "DATE", "URI", "IP", "PATH" 각 type 이 key 값으로 가지고 인식된 obj 를 가지고 있는 Orderdict 객체
    """

    return_data = OrderedDict()

    return_data["LOG"] = log

    # TIME ~ PATH 돌면서 추출된 각 obj 들을 dict 구조에 저장
    for obj in TYPE_OBJ:
        recognized_objs = get_all_objs(log, obj)
        return_data[obj] = recognized_objs

    return return_data


def get_all_objs(log: str, obj_type: str):
    """
        각 obj_type regrex pattern 을 log 한 줄을 findall 하여 리턴

        :param log: log data 한 줄, type: str
        :param obj_type: 이미 생성한 grok pattern 을 구별을 위함
        :return: log 한 줄에 해당 regrex findall 리스트
    """

    return_obj_list = list()
    regex_obj = upload_grok_obj()[obj_type].regex_obj

    if obj_type == "TIME":
        is_objs = get_time_objs(log, regex_obj)
    elif obj_type == "IP":
        is_objs = get_ip_objs(log, regex_obj)
    elif obj_type == "PATH":
        is_objs = get_path_objs(log, regex_obj)
    elif obj_type == "JSON":
        is_objs = get_json_objs(log)
        return is_objs
    else:
        is_objs = regex_obj.findall(log)

    for is_obj in is_objs:
        if obj_type == "PATH":
            # findall 로 리턴된 튜플 안에서 0번째 path 선택 & file path 처음 및 마지막 필요 없는 str obj 제거
            is_path = is_obj[0].strip('<>()[]{}\"\',.:=\\n ')
            return_obj_list.append(is_path)
        elif obj_type == "URI":
            is_uri = is_obj[0].strip('()=:[]\'\", ')  # URI 의 경우 string 처음 or 마지막 :, ", =, ', [, ], (, ), , 제거
            return_obj_list.append(is_uri)
        elif obj_type == "IP":
            is_ip = is_obj[0].strip('-:\"\'[]()=@, ')  # IP 의 경우 string 처음 or 마지막 -, :, ", =, ', [, ], (, ), @, , 제거
            return_obj_list.append(is_ip)
        else:
            return_obj_list.append(is_obj[0].strip())

    return return_obj_list


def get_time_objs(log: str, regex_obj):
    """
        Time obj 가 아닌 정보를 인식 문제를 해결 위한 함수로 3개에 해당 obj 를 subtract from a log data
        - {"address": "0000:00:06.2} -> "TIME": '00:00:06.2'
        - is set to 000:00:00:00.000 -> "TIME": '00:00:00:00'
        - 02:42:ac:ff:fe:11:00:02 -> "TIME": '11:00:02'

        :param log: log data 한 줄, type: str
        :param regex_obj: Time grok pattern 을 regrex 객체로 변환한 re 객체
        :return: log data 한 개에서 time obj 를 findall 로 인식한 리스트 안 튜플 data structure
    """

    sub_log = SUBTRACT_TIME_GROK.regex_obj.sub(SUB_SIGN, log)  # log data 에서 subtract 할 regex pattern 객체

    is_time_objs = regex_obj.findall(sub_log)

    return is_time_objs


def get_path_objs(log: str, regex_obj):
    """
        File Path obj 가 아닌 obj 인식 문제를 해결 위한 함수로 아래 경우에 해당 obj 를 subtract from a log data
        - 3 ops, 0%/0% of on/off-heap limit -> 'PATH': '/0%'

        :param log: log data 한 줄, type: str
        :param regex_obj: File path grok pattern 을 regrex 객체로 변환한 re 객체
        :return: log data 한 개에서 file path obj 를 findall 로 인식한 리스트 안 튜플 data structure
    """

    sub_regex = upload_sub_path_regex()  # 위의 주석의 경우와 URI, IP 차례로 log data 에서 subtract 위한 regex 객체 (dict)

    sub_log = log
    for regex in sub_regex.values():
        sub_log = regex.sub(SUB_SIGN, sub_log)  # log data 에서 subtract 할 regex pattern 객체

    is_path_objs = regex_obj.findall(sub_log)

    return is_path_objs


def get_ip_objs(log: str, regex_obj):
    """
        IP obj 가 Overlapping 되는 경우
            - 'http://192.168.122.122:9292/v1/images/53664ce3-7125-48c1-974e-eceb6f69d912#012x-image-meta-min_ram:'
            - 'URI': 'http://192.168.122.122:9292/v1/images/53664ce3-7125-48c1-974e-eceb6f69d912#012x-image-meta-min_ram:'
            - 'IP': '/192.168.122.122:9292'
        => Overlapping 된 IP obj 가 URI 에 포함 관계

        IP obj 인식 전 subtract 해줘야 하는 case
            - \n10.0.0.2/24 -> n10.0.0.2 로 인식 -> \n 을 subtract

        IP obj 인식 전에 log data 에서 위의 subtract case 와 URI obj 를 subtract 해주자

        :param log: log data 한 줄, type: str
        :param regex_obj: IP grok pattern 을 regrex 객체로 변환한 re 객체
        :return: log data 한 개에서 IP obj 를 findall 로 인식한 리스트 안 튜플 data structure
    """

    sub_regex = upload_sub_ip_regex()  # 위의 주석의 경우와 URI 차례로 log data 에서 subtract 위한 regex 객체 (dict)

    sub_log = log
    for regex in sub_regex.values():
        sub_log = regex.sub(SUB_SIGN, sub_log)

    is_ip_objs = regex_obj.findall(sub_log)

    return is_ip_objs


def validateJSON(jsonData):
    try:
        json.loads(json.dumps(ast.literal_eval(jsonData)))
    except SyntaxError:
        return False
    except ValueError:
        return False
    return True


def get_could_be_json(log: str):
    """
        설명: log data 를 input 으로 log 한 줄 내에 있는 json 형식일 수도 있는 obj 들을 모두 모아 리턴
        json 형식일 수도 있다는 것의 기준: { 와 } 가 개수가 맞을 경우 -> Parenthesis 가 valid 한 경우를 json 형식 이라 가정

        :param log: log data 한 문장
        :return json_list: log data 내에 있는 json 인지를 판별할 str obj 를 모아둔 리스트
    """
    stack = list()
    json_list = list()

    for index, s in enumerate(log):
        if s == '{':
            if len(stack) == 0:
                start_idx = index
            stack.append(s)
        elif s == '}':
            if len(stack) == 0:
                stack.clear()
                continue
            stack.pop()
            if len(stack) == 0:
                end_idx = index
                json_list.append(log[start_idx: end_idx + 1])

    return json_list


def get_json_objs(log: str):
    """
        obj.replace('\'', '\"'):
            - log data 에서 valid 한 json 형식이 아니지만 json 형식으로 써놓은 것들이 있다.
            - valid => {"log": data}
            - invalid => {'log': data}
            - 일단 ' 를 " 로 변경 후 json obj 가 valid 한 지 판단

        :param log: log data 한 문장
        :return is_json_objs: log 한 data 에서 valid 한 json obj 들을 모아 list 형태로 return
    """

    is_json_objs = list()

    obj_list = get_could_be_json(log)
    for obj in obj_list:
        if validateJSON(obj.replace('\'', '\"')):   # 설명
            is_json_objs.append(obj)

    return is_json_objs
