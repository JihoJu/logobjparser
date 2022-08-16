import ast
from collections import OrderedDict
import json
import LogObjParser.pattern as pattern
import xml.etree.ElementTree as ET

SUB_SIGN = "   #spec#   "  # 각 obj 를 인식 후 해당 obj 자리 제거를 위한 string
TYPE_OBJ = ["TIME", "DATE", "URI", "IP", "PATH", "JSON", "XML"]


def parse_log_data(log: str):
    """ Recognize each type obj for single-line entry of a log data

        로그 data 한 줄을 입력 시
        Type: "TIME", "DATE", "URI", "IP", "PATH", "JSON", "well-defined XML"
        위에 해당 type obj 를 identifying 후 json 형식 표현을 위해 dictionary data structure 에 저장

        :param log: log data 한 줄, type: str
        :return: 각 type 이 key 값, 인식된 obj 를 값으로 가지고 있는 Orderdict 객체
    """

    return_data = OrderedDict()

    return_data["LOG"] = log
    return_data["TIME"] = get_time_objs(log, pattern.TIME_GROK.regex_obj)
    return_data["DATE"] = get_date_objs(log, pattern.DATE_GROK.regex_obj)
    return_data["URI"] = get_uri_objs(log, pattern.URI_GROK.regex_obj)
    return_data["IP"] = get_ip_objs(log, pattern.IP_GROK.regex_obj)
    return_data["PATH"] = get_path_objs(log, pattern.PATH_GROK.regex_obj)
    return_data["JSON"] = get_json_objs(log)
    return_data["XML"] = get_xml_objs(log)

    return return_data


def get_time_objs(log: str, regex_obj):
    """ Identify TIME obj from a log data

        Time obj 가 아닌 정보를 인식 문제를 해결 위한 함수로 3개에 해당 obj 를 subtract from a log data
        - {"address": "0000:00:06.2} -> "TIME": '00:00:06.2'
        - is set to 000:00:00:00.000 -> "TIME": '00:00:00:00'
        - 02:42:ac:ff:fe:11:00:02 -> "TIME": '11:00:02'

        :param log: log data 한 줄, type: str
        :param regex_obj: Time grok pattern 을 regrex 객체로 변환한 re 객체
        :return: log data 한 개에서 time obj 를 findall 로 인식한 리스트 안 튜플 data structure
    """

    sub_log = pattern.SUBTRACT_TIME_GROK.regex_obj.sub(SUB_SIGN, log)  # log data 에서 subtract 할 regex pattern 객체

    is_time_objs = regex_obj.findall(sub_log)

    if is_time_objs:
        parsed_time_objs = list()
        for obj in is_time_objs:
            parsed_time_objs.append(obj[0].strip())
        return parsed_time_objs

    return is_time_objs


def get_date_objs(log: str, regex_obj):
    """ Identify DATE objs from a log data

        :param log: log data 한 줄, type: str
        :param regex_obj: Date grok pattern 을 regrex 객체로 변환한 re 객체
        :return: log data 한 개에서 date obj 를 findall 로 인식한 리스트 안 튜플 data structure
    """
    is_date_objs = regex_obj.findall(log)

    if is_date_objs:
        parsed_date_objs = list()
        for obj in is_date_objs:
            parsed_date_objs.append(obj[0].strip())
        return parsed_date_objs

    return is_date_objs


def get_uri_objs(log: str, regex_obj):
    """ Identify URI objs from a log data

        :param log: log data 한 줄, type: str
        :param regex_obj: URI grok pattern 을 regrex 객체로 변환한 re 객체
        :return: log data 한 개에서 URI obj 를 findall 로 인식한 리스트 안 튜플 data structure
    """
    is_uri_objs = regex_obj.findall(log)

    if is_uri_objs:
        parsed_uri_objs = list()
        for obj in is_uri_objs:
            # URI 의 경우 string 처음 or 마지막 :, ", =, ', [, ], (, ), , 제거
            parsed_uri_objs.append(obj[0].strip(pattern.STRIP_URI))
        return parsed_uri_objs

    return is_uri_objs


def get_path_objs(log: str, regex_obj):
    """ Identify File Path obj from a log data

        File Path obj 가 아닌 obj 인식 문제를 해결 위한 함수로 아래 경우에 해당 obj 를 subtract from a log data
        - 3 ops, 0%/0% of on/off-heap limit -> 'PATH': '/0%'

        :param log: log data 한 줄, type: str
        :param regex_obj: File path grok pattern 을 regrex 객체로 변환한 re 객체
        :return: log data 한 개에서 file path obj 를 findall 로 인식한 리스트 안 튜플 data structure
    """

    # 위의 주석의 경우와 URI, sub_path 차례로 log data 에서 subtract 위한 regex 객체 (dict)
    sub_regex = pattern.upload_sub_path_regex()

    # file path obj 인식 전 get_ip_objs 함수가 인식한 ip objs 를 log 에서 subtract
    sub_ip_objs = get_ip_objs(log, pattern.IP_GROK.regex_obj)
    for obj in sub_ip_objs:
        log = log.replace(obj, SUB_SIGN)

    # file path obj 추출 전 URI, sub_path obj 제거
    for regex in sub_regex.values():
        log = regex.sub(SUB_SIGN, log)  # log data 에서 subtract 할 regex pattern 객체

    is_path_objs = regex_obj.findall(log)

    if is_path_objs:
        parsed_path_objs = list()
        for obj in is_path_objs:
            # findall 로 리턴된 튜플 안에서 0번째 path 선택 & file path 처음 및 마지막 필요 없는 str obj 제거
            parsed_path_objs.append(obj[0].strip(pattern.STRIP_PATH))
        return parsed_path_objs

    return is_path_objs


def get_ip_objs(log: str, regex_obj):
    """ Identify IP obj from a log data

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

    sub_regex = pattern.upload_sub_ip_regex()  # 위의 주석의 경우와 URI 차례로 log data 에서 subtract 위한 regex 객체 (dict)

    # ip obj 추출 전 \n, uri obj 제거
    for regex in sub_regex.values():
        log = regex.sub(SUB_SIGN, log)

    is_ip_objs = regex_obj.findall(log)

    if is_ip_objs:
        parsed_ip_objs = list()
        for obj in is_ip_objs:
            if obj[0] == '::':  # '::' 만 인식 case 제거
                continue
            if pattern.SUBTRACT_IPV6_REGEX.fullmatch(obj[0]):  # abca::abcf -> 'abca::abcf' 인식 case 제거
                continue
            # IP 의 경우 string 처음 or 마지막 -, :, ", =, ', [, ], (, ), @, , 제거
            parsed_ip_objs.append(obj[0].strip(pattern.STRIP_IP))
        return parsed_ip_objs

    return is_ip_objs


def validateJSON(jsonData: str):
    """ Validate if obj is json format

        - ast.literal_eval(jsonData): str type 의 dictionary, list 를 python object 로 변환
            - unicode 형식의 obj issue 를 해결하기 위해 사용 (prefix 'u')
            - ex) "{u'id': u'asdf'}"
        - json.dumps(): python 객체를 json 문자열 변환
            - could_be_json object 가 python dictionary 형태일 경우를 고려
            - ex) json format: null, false, true / dict: None, False, True etc...
        -json.load(): json format data 를 python object 로 변환
            - 이 과정에서 data 가 json format 에 적합하지 않다면 SyntaxError or ValueError 발생

        :param jsonData: str type 의 could be json obj
        :return: jsonData 가 json format 에 해당 : True or not False
    """
    try:
        json.loads(jsonData)
    except ValueError:
        try:
            json.loads(json.dumps(ast.literal_eval(jsonData)))
        except ValueError:
            return False
        except SyntaxError:
            return False
    return True


def get_could_be_json(log: str):
    """ Extract could be json obj from a log data

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


def check_exception_case_in_json(json_obj: str):
    """ Determine if obj is included in the json exception case

        다음 case 에 포함이 된다면 json format 에 맞게 replace

        1. openstack object
            - <KeystoneToken ~>, <nova.api.~>, etc 가 포함되어 있는 case
                - "{..., 'token': <KeystoneToken (audit_id=Ax_ByWknSh6oMIA4tCd41w, \
                        audit_chain_id=Ax_ByWknSh6oMIA4tCd41w) at 0x7f4222e832a0>, ...}"
                - "{'action': u'detail', 'controller': <nova.api.openstack.wsgi.Resource object at 0x469e5d0>}"

            - '"' 로 감싸준 뒤 json validation 과정을 수행 (string type 으로 변환)

        2. python datetime object
            - "{u'created_at': datetime.datetime(2013, 10, 30, 14, 20, 44), \
                u'updated_at': datetime.datetime(2014, 8, 11, 8, 18, 47), u'disabled': False}"

            - datetime.~~ str obj 가 포함되어 있는 case
            - '"' 로 감싸준 뒤 json validation 과정을 수행 (string type 으로 변환)

        3. suffix 'L'
            - "{u'report_count': 2397970L, u'disabled': False, u'deleted_at': None, u'disabled_reason': None, u'id': 5L}"
            - 숫자 뒤 L 를 빼고 json validation 과정을 수행

        :param json_obj: str type 의 could be json obj
        :return json_obj: 특정 case 가 replace 된 json obj (예외 case 에 해당되는 경우)
    """
    exception_regex = pattern.upload_replace_exception_case_regex_in_json()

    if pattern.OPENSTACK_GROK_IN_JSON.match(json_obj):
        exc_list = exception_regex["OPENSTACK_REGEX"].findall(json_obj)
        for exc in exc_list:
            json_obj = json_obj.replace(exc, '"' + exc + '"')
    if pattern.DATETIME_GROK_IN_JSON.match(json_obj):
        exc_list = exception_regex["DATETIME_REGEX"].findall(json_obj)
        for exc in exc_list:
            json_obj = json_obj.replace(exc, '"' + exc + '"')
    if exception_regex["LONG_DIGIT_REGEX"].findall(json_obj):
        exc_list = exception_regex["LONG_DIGIT_REGEX"].findall(json_obj)
        for exc in exc_list:
            json_obj = json_obj.replace(exc, exc[:-1])

    return json_obj


def get_json_objs(log: str):
    """ Identify JSON obj from a log data

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
        parsed_obj = check_exception_case_in_json(obj.replace('\'', '\"'))
        if validateJSON(parsed_obj):  # 설명
            is_json_objs.append(obj)

    return is_json_objs


def validateXML(xml: str):
    """ Check if obj that could be xml is valid

        :param xml: string obj could be xml
        :return: xml 이 맞다면 true, 아니면 false
    """
    try:
        ET.fromstring(xml)
    except SyntaxError:
        return False
    except ValueError:
        return False
    return True


def get_xml_last_index(start: int, word: str, log: str):
    """ word (xml tag) 에 대응하는 end tag index 반환

        :param start: log data 에서 word 를 찾기 시작할 시작 index
        :param word: xml start tag
        :param log: a log data
        :return: start tag 대응 end tag 가 존재: end tag index / 존재 x: -1
    """
    index = start + 1
    while index != -1:
        index = log.find(word, index)
        if index > -1:
            return index + len(word)
    return -1


def get_could_xml_objs(log: str):
    """ Extract all obj that can be xml obj

        :param log: a log data
        :return: all obj that can be xml
    """

    is_could_xml = list()

    index = 0
    end_idx = 0  # last tag index in xml obj
    for idx in range(0, len(log)):
        if idx < end_idx:
            continue
        if log[idx] == "<":
            index = idx + 1
        elif log[idx] == ">":
            word = log[index:idx].split(" ")[0]  # tag 를 word 변수에 할당 ex) <domain type="qemu">
            finding_word = f"</{word}>"
            end_idx = get_xml_last_index(idx + 1, finding_word, log)
            if end_idx != -1:
                is_could_xml.append(log[index - 1: end_idx])

    return is_could_xml


def get_xml_objs(log: str):
    """ Identify well-defined XML obj from a log data

        :param log: A log data
        :return xml_obj: xml objects
    """
    is_xml_obj = list()

    is_xml = get_could_xml_objs(log)
    for xml in is_xml:
        if validateXML(xml):
            is_xml_obj.append(xml)

    return is_xml_obj
