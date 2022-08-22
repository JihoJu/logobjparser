import os
import csv
import time
from LogObjParser.parser import get_path_objs


def read_data(path, filename):
    """ Read log files line_by_line by creating a generator
    :param filename: 읽을 file name
    :param path: log files 가 있는 directory path
    :return: log line
    """

    with open(os.path.join(path, filename)) as f:
        for rd in f.readlines():
            yield rd.strip()


def get_dataset(path, typename, function):
    """
    :param path: 읽을 log file 이 있는 directory path
    :param typename: log file type name ex-hadoop, openstack, etc...
    :param function: obj 를 인식 함수
    """

    # path 에 있는 file 들 중 typename 를 가지고 있는 file 만을 files 변수에 할당 (generator)
    files = (filename for filename in os.listdir(path) if typename in filename)
    # 결과를 저장할 dataset (csv 형태)
    dataset = open('../dataset/{0}/{1}_dataset.csv'.format(typename, typename), "w")
    writer = csv.writer(dataset)

    for filename in files:
        log_data = read_data("../logdata", filename)
        for log in log_data:
            is_objs = function(log)  # obj 인식 함수
            writer.writerow([log, is_objs])

    dataset.close()


types = ["cassandra", "hadoop", "mongodb", "openstack", "spark", "test"]
start = time.time()
for type_name in types:
    get_dataset("../logdata", type_name, get_path_objs)
end = time.time()
print(round(end - start, 3))
