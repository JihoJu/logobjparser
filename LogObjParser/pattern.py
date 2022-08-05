import re
from pygrok import Grok

""" Grok Pattern """
TIME_PATTERN = r"(?<time>(?!<[0-9])%{HOUR}:%{MINUTE}[Z]|%{TIME:time}([+]([0-9]*))?[Z]?)"
DATE_PATTERN = r"(?<date>%{MONTHDAY}/%{MONTH}/%{YEAR}|%{YEAR}[/-]%{MONTHNUM}[/-]%{MONTHDAY}[T ]|%{DAY}([\S])? %{MONTHDAY} %{MONTH} %{YEAR}|%{MONTHDAY} %{MONTH} %{YEAR}|%{MONTH} %{YEAR}|%{YEAR} %{MONTH} %{MONTHDAY}|%{DAY} %{MONTH} %{MONTHDAY}|%{MONTH} %{MONTHDAY})"  # Custom Date pattern : 날짜 뒤 T 까지 추출
URI_PATTERN = r"(?<url>%{URI}|GET %{PATH}[\S]*|POST %{PATH}[\S]*|PUT %{PATH}[\S]*|DELETE %{PATH}[\S]*)"
IP_PATTERN = r"(?<ip>%{HOSTNAME}[/:]%{IPV4}([:](?:[0-9]*))?|[/]%{IPV4}([:](?:[0-9]*))?(/[0-9]{2})?|[^-]%{IPV4}([/]%{IPV4})?([:](?:[0-9]*))?(/[0-9]+)?|[-]%{IPV4}[-]|%{IPV6}(/[0-9]+)?)"  # 마지막 pattern 은 수정이 필요 : =155.~~ -를 제외한 특수문자를 다 가져옴.
PATH_PATTERN = r"(?<path>[^A-Za-z0-9]%{PATH}[\S]+)"

""" Grok Pattern for Json Exception Case """
OPENSTACK_PATTERN_IN_JSON = r"(?<json>(%{QUOTEDSTRING}: (<[\S\s]*>)+)+)"  # "key": <KeyStone~~>
DATETIME_PATTERN_IN_JSON = r"(?<json>(%{QUOTEDSTRING}: datetime.[A-Za-z]+\([A-Za-z0-9 ,]*\)))"  # "key": datetime.~

TIME_GROK = Grok(TIME_PATTERN)
DATE_GROK = Grok(DATE_PATTERN)
URI_GROK = Grok(URI_PATTERN)
IP_GROK = Grok(IP_PATTERN)
PATH_GROK = Grok(PATH_PATTERN)
OPENSTACK_GROK_IN_JSON = Grok(OPENSTACK_PATTERN_IN_JSON)
DATETIME_GROK_IN_JSON = Grok(DATETIME_PATTERN_IN_JSON)

""" Time Regrex Pattern for validation """
SUBTRACT_TIME_PATTERN = r"(?<sub_time>0{3,}:0{2,}:|0{3,}:|%{MAC}([:]\d*)*)"
SUBTRACT_TIME_GROK = Grok(SUBTRACT_TIME_PATTERN)

""" IP Regrex Pattern for validation """
SUBTRACT_IP_REGEX = re.compile(r'\\n')

""" File Path Regrex Pattern for validation """
SUBTRACT_PATH_PATTERN = r"(?<sub_path>( [^/` ]+/[^/ ]+ ){1}|</\w*>|/>{1})"
SUBTRACT_PATH_GROK = Grok(SUBTRACT_PATH_PATTERN)

""" Exception Regrex Pattern for Json Validation """
OPENSTACK_REGEX = re.compile(r"(<[\S\s]*>)+")  # openstack object: <nova.api.~>, <KeyStone~>
LONG_DIGIT_REGEX = re.compile(r"[\d]+[L|l]+")  # suffix 'L': 0L, 23345L
DATETIME_REGEX = re.compile(r"datetime.[A-Za-z]+\([A-Za-z0-9 ,]*\)")  # datetime object: datetime.datetime(~)

""" STRIP REGEX """
STRIP_PATH = '<>()[]{}\"\'`,.:;=\n '
STRIP_URI = '()=:[]\'\", '  # URI 의 경우 string 처음 or 마지막 :, ", =, ', [, ], (, ), , 제거
STRIP_IP = '-:\"\'[]()=@, '  # IP 의 경우 string 처음 or 마지막 -, :, ", =, ', [, ], (, ), @, , 제거

""" MIME-Type REGEX """
MIMETYPE_REGEX = re.compile(
    r"([^/]((text|image|audio|video|application|\*)/(aac|x-abiword|octet-stream|x-msvideo|vnd.amazon.ebook|x-bzip2?|x-csh|css|csv|msword|epub\+zip|gif|html|x-icon|calendar|java-archive|json|midi|jpeg|javascript|mpeg|vnd\.apple\.installer\+xml|vnd\.oasis\.opendocument\.presentation|vnd\.oasis\.opendocument\.spreadsheet|vnd\.oasis\.opendocument\.text|ogg|pdf|vnd\.ms-powerpoint|x-rar-compressed|rtf|x-sh|svg\+xml|x-shockwave-flash|x-tar|tiff|x-front-ttf|vnd\.visio|x-wav|webm|webp|x-font-woff|xhtml\+tml|vnd\.ms-excel|vnd\.mozilla\.xul\+xml|zip|3gpp2?|x-7z-compressed|\*)){1})[^/]"
)


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

    collection_regex["MIME_TYPE"] = MIMETYPE_REGEX
    collection_regex["SUBTRACT_PATH_REGEX"] = SUBTRACT_PATH_GROK.regex_obj
    collection_regex["URI_REGEX"] = URI_GROK.regex_obj
    collection_regex["IP_REGEX"] = IP_GROK.regex_obj

    return collection_regex


def upload_replace_exception_case_regex_in_json():
    """
        Returns sub regrex objects after converting them to a dict
        Before validating json obj in log data, the regex pattern to be replaced

        - openstack obj: <KeyStone ~~>, <glance.api~>, <nova.api.~> etc...
        - suffix 'L' or 'l': 0L, 34531L etc...
        - datetime obj: datetime.datetime(2014, 8, 11, 8, 18, 47) etc...
    """

    collection_regex = dict()

    collection_regex["OPENSTACK_REGEX"] = OPENSTACK_REGEX
    collection_regex["LONG_DIGIT_REGEX"] = LONG_DIGIT_REGEX
    collection_regex["DATETIME_REGEX"] = DATETIME_REGEX

    return collection_regex
