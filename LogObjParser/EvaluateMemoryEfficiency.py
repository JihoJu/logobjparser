import ast
import csv
import pandas as pd


def read_data(path: str):
    """ Return log data & correct list after reading correct dataset

    :return: (log: str, answer: list) => answer: 정답 obj 리스트
    """
    dataset = pd.read_csv(path)  # 정답 데이터 셋을 읽음

    for row in dataset.itertuples():
        yield row[1], ast.literal_eval(row[2])  # row[2]: str type -> ast.literal_eval 로 파이썬 리스트 객체로 변환


def masking(log: str, labeled_obj: list, mask_obj: str):
    for obj in labeled_obj:
        log = log.replace(obj, mask_obj)

    return log


class EvaluateMemoryEfficiency:
    def __init__(self, read_path, write_path, mask_obj):
        self.read_path = read_path
        self.write_path = write_path
        self.mask_obj = mask_obj

    def run(self):
        data = read_data(self.read_path)

        masked_dataset = open(self.write_path, "w")
        writer = csv.writer(masked_dataset)

        for log, labeled_obj in data:
            masked_log = masking(log, labeled_obj, self.mask_obj)
            writer.writerow([masked_log])

        masked_dataset.close()


eme = EvaluateMemoryEfficiency("../dataset/mongodb/mongodb_labeled.csv", '../dataset/masked_dataset.csv', "@path")
eme.run()
