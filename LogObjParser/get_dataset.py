import os
import csv
from LogObjParser.pattern import PATH_GROK
from LogObjParser.parser import get_path_objs


def read_data(path):
    """ Read log files line_by_line by creating a generator
    :param path: log files 가 있는 directory path
    :return: log line
    """
    for filename in os.listdir(path):
        with open(os.path.join(path, filename)) as f:
            for rd in f.readlines():
                yield rd.strip()


def get_dataset(function, regex, dataset_name):
    """
    :param function: log data 에서 인식할 obj 함수
    :param regex: 인식할 type obj 의 regex object
    :param dataset_name: 결과를 저장할 dataset name
    """
    dataset = open('../dataset/{0}'.format(dataset_name), "w")
    writer = csv.writer(dataset)

    log_data = read_data("../logdata")
    for log in log_data:
        is_objs = function(log, regex)
        writer.writerow([log, is_objs])

    dataset.close()


get_dataset(get_path_objs, PATH_GROK.regex_obj, "path_dataset.csv")
