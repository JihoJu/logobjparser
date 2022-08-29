from multiprocessing import Pool
from LogObjParser.parser import get_path_objs
from concurrent.futures import ThreadPoolExecutor


def read_data(path: str):
    """ Return log data after reading log dataset (Generator)

    :return: log -> str
    """
    with open(path, 'r') as f:
        for log in f.readlines():
            yield log.strip()


class EvaluateMemoryEfficiency:
    """ Evaluate Memory Efficiency Class

    이후에 확장성을 고려해 일단 class 로 구성
    """

    def __init__(self, mask_obj):
        self.mask_obj = mask_obj

    def masking(self, log: str):
        """ Masking file path obj to specified obj in a log

        :param log: A log data
        :return: 특정 str 객체로 치환된 log data
        """
        for path_obj in get_path_objs(log):  # file path obj 인식
            log = log.replace(path_obj, self.mask_obj)  # mask_obj: 치환 string 객체

        return log + '\n'  # 비효율,,, -> 문자열 객체를 다시 생성하기에,,,


if __name__ == '__main__':
    data = read_data('../logdata/openstack_clean_seorin.log')

    eme = EvaluateMemoryEfficiency('@path')

    # Multi-processing process 개수 8개
    with Pool(8) as p:
        result = p.map(eme.masking, data)

    # iter 객체를 파일에 쓰는 IO-bound Task
    # 쓰레드 사용 x: 1.8795 / 멀티 스레드(8) 사용: 0.0323
    with open("../dataset/masked_openstack.log", 'w') as wf:
        with ThreadPoolExecutor(8) as executor:
            executor.map(wf.write, result)
