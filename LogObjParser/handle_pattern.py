import re
from pygrok import Grok

""" Grok Pattern """
TIME_PATTERN = "(?<time>%{TIME:time}([+]([0-9]*))?)"
DATE_PATTERN = "(?<date>%{YEAR}[/-]%{MONTHNUM}[/-]%{MONTHDAY}[T ]|%{DAY}([\S])? %{MONTHDAY} %{MONTH} %{YEAR}|%{MONTHDAY} %{MONTH} %{YEAR}|%{MONTH} %{YEAR}|%{YEAR} %{MONTH} %{MONTHDAY}|%{DAY} %{MONTH} %{MONTHDAY}|%{MONTH} %{MONTHDAY})"  # Custom Date pattern : 날짜 뒤 T 까지 추출
URI_PATTERN = "(?<url>%{URI}|GET %{PATH}[\S]*|POST %{PATH}[\S]*|PUT %{PATH}[\S]*|DELETE %{PATH}[\S]*)"
IP_PATTERN = "(?<ip>%{HOSTNAME}[/:]%{IPV4}([:]%{POSINT})?|[/]%{IPV4}([:]%{POSINT})?|[^-]%{IPV4}([:]%{POSINT})?)"  # 마지막 pattern 은 수정이 필요 : =155.~~ -를 제외한 특수문자를 다 가져옴.
PATH_PATTERN = "(?<path>[^A-Za-z0-9]%{PATH}[\S]+)"

TIME_GROK = Grok(TIME_PATTERN)
DATE_GROK = Grok(DATE_PATTERN)
URI_GROK = Grok(URI_PATTERN)
IP_GROK = Grok(IP_PATTERN)
PATH_PATTERN = Grok(PATH_PATTERN)

""" Regrex Pattern """
MASTER_REGEX = re.compile(
    r"(/?([a-z.A-Z0-9\-_]+/)+[@a-zA-Z0-9\-_+.]+\.[a-zA-Z0-9]{1,10})[:-]?(\d+)?"
)

MASTER_REGEX_MORE_EXTENSIONS = re.compile(
    r"(/?([a-z.A-Z0-9\-_]+/)+[@a-zA-Z0-9\-_+.]+\.[a-zA-Z0-9-~]{1,30})[:-]?(\d+)?"
)
HOMEDIR_REGEX = re.compile(
    r"(~/([a-z.A-Z0-9\-_]+/)+[@a-zA-Z0-9\-_+.]+\.[a-zA-Z0-9]{1,10})[:-]?(\d+)?"
)
OTHER_BGS_RESULT_REGEX = re.compile(
    r"(/?([a-z.A-Z0-9\-_]+/)+[a-zA-Z0-9_.]{3,})[:-]?(\d+)"
)
ENTIRE_TRIMMED_LINE_IF_NOT_WHITESPACE = re.compile(r"(\S.*\S|\S)")
JUST_FILE_WITH_NUMBER = re.compile(
    r"([@%+a-z.A-Z0-9\-_]+\.[a-zA-Z]{1,10})[:-](\d+)(\s|$|:)+"
)
JUST_FILE = re.compile(r"([@%+a-z.A-Z0-9\-_]+\.[a-zA-Z]{1,10})(\s|$|:)+")
JUST_EMACS_TEMP_FILE = re.compile(r"([@%+a-z.A-Z0-9\-_]+\.[a-zA-Z]{1,10}~)(\s|$|:)+")
JUST_VIM_TEMP_FILE = re.compile(r"(#[@%+a-z.A-Z0-9\-_]+\.[a-zA-Z]{1,10}#)(\s|$|:)+")

""" Time Regrex Pattern for validation """
SUBTRACT_TIME_PATTERN = "(?<sub_time>0{3,}:0{2,}:|0{3,}:|%{MAC}([:]\d*)*)"
SUBTRACT_TIME_GROK = Grok(SUBTRACT_TIME_PATTERN)

""" File Path Regrex Pattern for validation """
SUBTRACT_PATH_PATTERN = "(?<sub_path>( [^/ ]+/[^/ ]+ ){1})"
SUBTRACT_PATH_GROK = Grok(SUBTRACT_PATH_PATTERN)


def upload_grok_obj():
    """ Returns grok objects after converting them to a dict """

    collection_grok = dict()

    collection_grok["TIME"] = TIME_GROK
    collection_grok["DATE"] = DATE_GROK
    collection_grok["URI"] = URI_GROK
    collection_grok["IP"] = IP_GROK
    collection_grok["PATH"] = PATH_PATTERN

    return collection_grok


def upload_regex_obj():
    """ Returns regrex objects after converting them to a dict """

    collection_regex = dict()

    collection_regex["MASTER_REGEX"] = MASTER_REGEX
    collection_regex["MASTER_REGEX_MORE_EXTENSIONS"] = MASTER_REGEX_MORE_EXTENSIONS
    collection_regex["HOMEDIR_REGEX"] = HOMEDIR_REGEX
    collection_regex["OTHER_BGS_RESULT_REGEX"] = OTHER_BGS_RESULT_REGEX
    collection_regex["ENTIRE_TRIMMED_LINE_IF_NOT_WHITESPACE"] = ENTIRE_TRIMMED_LINE_IF_NOT_WHITESPACE
    collection_regex["JUST_FILE_WITH_NUMBER"] = JUST_FILE_WITH_NUMBER
    collection_regex["JUST_FILE"] = JUST_FILE
    collection_regex["JUST_EMACS_TEMP_FILE"] = JUST_EMACS_TEMP_FILE
    collection_regex["JUST_VIM_TEMP_FILE"] = JUST_VIM_TEMP_FILE

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
