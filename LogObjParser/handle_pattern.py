import re
from pygrok import Grok

""" Grok Pattern """
TIME_PATTERN = "(?<time>(?!<[0-9])%{HOUR}:%{MINUTE}[Z]|%{TIME:time}([+]([0-9]*))?[Z]?)"
DATE_PATTERN = "(?<date>%{MONTHDAY}/%{MONTH}/%{YEAR}|%{YEAR}[/-]%{MONTHNUM}[/-]%{MONTHDAY}[T ]|%{DAY}([\S])? %{MONTHDAY} %{MONTH} %{YEAR}|%{MONTHDAY} %{MONTH} %{YEAR}|%{MONTH} %{YEAR}|%{YEAR} %{MONTH} %{MONTHDAY}|%{DAY} %{MONTH} %{MONTHDAY}|%{MONTH} %{MONTHDAY})"  # Custom Date pattern : 날짜 뒤 T 까지 추출
URI_PATTERN = "(?<url>%{URI}|GET %{PATH}[\S]*|POST %{PATH}[\S]*|PUT %{PATH}[\S]*|DELETE %{PATH}[\S]*)"
IP_PATTERN = "(?<ip>%{HOSTNAME}[/:]%{IPV4}([:](?:[0-9][0-9]*))?|[/]%{IPV4}([:](?:[0-9][0-9]*))?(/\d{2})?|[^-]%{IPV4}([:](?:[0-9][0-9]*))?(/\d{2})?|[-]%{IPV4}[-])"  # 마지막 pattern 은 수정이 필요 : =155.~~ -를 제외한 특수문자를 다 가져옴.
PATH_PATTERN = "(?<path>[^A-Za-z0-9]%{PATH}[\S]+)"
JSON_PATTERN = "(?<json>{(%{QUOTEDSTRING}[\s]?: [\w\W]*[,\s]*)*})"

TIME_GROK = Grok(TIME_PATTERN)
DATE_GROK = Grok(DATE_PATTERN)
URI_GROK = Grok(URI_PATTERN)
IP_GROK = Grok(IP_PATTERN)
PATH_PATTERN = Grok(PATH_PATTERN)
JSON_PATTERN = Grok(JSON_PATTERN)

""" Time Regrex Pattern for validation """
SUBTRACT_TIME_PATTERN = "(?<sub_time>0{3,}:0{2,}:|0{3,}:|%{MAC}([:]\d*)*)"
SUBTRACT_TIME_GROK = Grok(SUBTRACT_TIME_PATTERN)

""" IP Regrex Pattern for validation """
SUBTRACT_IP_REGEX = re.compile(r'\\n')

""" File Path Regrex Pattern for validation """
SUBTRACT_PATH_PATTERN = "(?<sub_path>( [^/ ]+/[^/ ]+ ){1}|</\w*>|/>{1})"
SUBTRACT_PATH_GROK = Grok(SUBTRACT_PATH_PATTERN)


def upload_grok_obj():
    """ Returns grok objects after converting them to a dict """

    collection_grok = dict()

    collection_grok["TIME"] = TIME_GROK
    collection_grok["DATE"] = DATE_GROK
    collection_grok["URI"] = URI_GROK
    collection_grok["IP"] = IP_GROK
    collection_grok["PATH"] = PATH_PATTERN
    collection_grok["JSON"] = JSON_PATTERN

    return collection_grok


def upload_sub_ip_regex():
    """
        Returns sub regrex objects after converting them to a dict
        Before recognizing ip obj in log data, the regex pattern to be subtracted
    """

    collection_regex = dict()

    collection_regex["SUBTRACT_IP_REGEX"] = SUBTRACT_IP_REGEX
    collection_regex["URI_REGEX"] = URI_GROK.regex_obj

    return collection_regex


def upload_sub_path_regex():
    """
        Returns sub regrex objects after converting them to a dict
        Before recognizing path obj in log data, the regex pattern to be subtracted
    """

    collection_regex = dict()

    collection_regex["SUBTRACT_PATH_REGEX"] = SUBTRACT_PATH_GROK.regex_obj
    collection_regex["URI_REGEX"] = URI_GROK.regex_obj
    collection_regex["IP_REGEX"] = IP_GROK.regex_obj

    return collection_regex
