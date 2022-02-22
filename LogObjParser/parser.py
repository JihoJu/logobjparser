from collections import OrderedDict
from LogObjParser.handle_pattern import upload_regex_obj, upload_grok_obj, SUBTRACT_TIME_GROK

SUB_SIGN = "   #spec#   "  # 각 obj 를 인식 후 해당 obj 자리 제거를 위한 string
TYPE_OBJ = ["TIME", "DATE", "URI", "IP", "PATH"]


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
    else:
        is_objs = regex_obj.findall(log)

    if is_objs:
        for is_obj in is_objs:
            if obj_type == "PATH":
                # findall 로 리턴된 튜플 안에서 0번째 path 선택 & file path 처음 및 마지막 필요 없는 str obj 제거
                return_obj_list.append(
                    is_obj[0][1:].strip(',.:= '))
            elif obj_type == "IP":
                is_ip = is_obj[0].strip()
                if is_ip[0] == '"' or is_ip[0] == "=":  # IP 의 경우 string 첫번째 문자가 ", = 경우가 있어 제거
                    is_ip = is_ip[1:]
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
