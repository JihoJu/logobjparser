import ast
import pandas as pd
from LogObjParser.parser import get_path_objs


def compare(list1, list2):
    """ Compare list1 with list2

    :param list1: str type obj 를 지닌 리스트
    :param list2: str type obj 를 지닌 리스트
    :return: True: 두 리스트가 같은 경우 / False: 두 리스트가 다른 경우
    """
    list1.sort()
    list2.sort()

    return list1 == list2


class EvaluateAccuracy:
    """ Evaluate the Obj identification function's result accuracy """

    def __init__(self, path, function):
        self.correct_dataset_path = path  # 정답 데이터 셋의 파일 경로
        self.correct_dataset_size = None  # 정답 데이터 개수
        self.correct_answer_cnt = 0  # 인식 결과가 정답인 경우
        self.function = function  # 정확성 평가를 위한 함수

    def read_data(self):
        """ Return log data & correct list after reading correct dataset

        :return: (log: str, answer: list) => answer: 정답 obj 리스트
        """
        dataset = pd.read_csv(self.correct_dataset_path)  # 정답 데이터 셋을 읽음
        self.correct_dataset_size = len(dataset)  # 정답 데이터 개수 객체 속성에 저장

        for row in dataset.itertuples():
            yield row[1], ast.literal_eval(row[2])  # row[2]: str type -> ast.literal_eval 로 파이썬 리스트 객체로 변환

    def evaluate(self):
        """ Evaluate the function's result accuracy """

        data = self.read_data()  # data: Generator

        for d in data:
            if compare(self.function(d[0]), d[1]):
                self.correct_answer_cnt += 1  # 인식 결과가 정답과 같은 경우

        print("{0}%".format(round((self.correct_answer_cnt / self.correct_dataset_size) * 100), 3))


obj = EvaluateAccuracy("../dataset/answer.csv", get_path_objs)
obj.evaluate()
