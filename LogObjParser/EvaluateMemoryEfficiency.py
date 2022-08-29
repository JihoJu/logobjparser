from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from LogObjParser.parser import get_path_objs


def read_data(path: str):
    """ Return log data after reading log dataset (Generator)

    :return: log -> str
    """
    with open(path, 'r') as f:
        for log in f.readlines():
            yield log.strip()


def masking(log: str):
    """ Masking file path obj to specified obj in a log

    :param log: A log data
    :return: 특정 str 객체로 치환된 log data
    """
    for path_obj in get_path_objs(log):  # file path obj 인식
        log = log.replace(path_obj, '@path')  # mask_obj: 치환 string 객체

    return log + '\n'  # 비효율,,, -> 문자열 객체를 다시 생성하기에,,,


def evaluate_memory_efficiency(origin_path, masked_path):
    """ Evaluate memory efficiency between two files """

    original_file = Path(origin_path).stat().st_size
    masked_file = Path(masked_path).stat().st_size

    return ((masked_file - original_file) / original_file) * 100


if __name__ == '__main__':
    data = read_data('../logdata/openstack_clean_seorin.log')

    # Multi-processing process 개수 8개
    with Pool(8) as p:
        result = p.map(masking, data)

    # iter 객체를 파일에 쓰는 IO-bound Task
    # 쓰레드 사용 x: 1.8795 / 멀티 스레드(8) 사용: 0.0323
    with open("../dataset/masked_openstack.log", 'w') as wf:
        with ThreadPoolExecutor(8) as executor:
            executor.map(wf.write, result)

    print(round(evaluate_memory_efficiency('../logdata/openstack_clean_seorin.log', "../dataset/masked_openstack.log"), 4))
