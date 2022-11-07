import logging
import os
import csv


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for line in rdr:
            yield line


def read_log(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            yield line


class FileManagement:
    """ Class for reading and writing files """

    def __init__(self, read_path=None, write_path=None):
        self.read_path = os.path.join(read_path)
        self.write_path = write_path

    def get_filepath(self):
        """ 객체 read_path에 해당하는 파일 경로 리턴

        주의: 리턴 iterator 을 generator 형태로 반환했지만 아래 코드처럼 수정
            - 같은 폴더 내에 파일을 write 시 무한 반복 이슈를 예방하기 위함
        :return: file path
        """
        # 한 폴더에 또다른 폴더가 존재해 재귀적으로 파일 경로를 얻을 때 사용
        if os.path.isdir(self.read_path):
            file_path_list = []
            for (root, _, files) in os.walk(self.read_path):
                for file in files:
                    if file[0] == ".":
                        continue
                    file_path = os.path.join(root, file)
                    file_path_list.append(file_path)
            return file_path_list
        elif os.path.isfile(self.read_path):  # 파일을 입력으로 받았을 경우
            return [self.read_path]
        else:
            logging.error("해당 디렉토리 및 파일이 존재하지 않습니다.")

    def read(self):
        """ path 내 파일을 읽어 한줄 씩 반환하는 Generator

        :return: file contents line
        """

        filepath_list = self.get_filepath()
        for filepath in filepath_list:
            ext = filepath.split(".")[-1]  # 확장자
            read_function = eval(f"read_{ext}")
            for line in read_function(filepath):
                yield line

    def write_csv(self, data):
        with open(self.write_path, 'w') as file:
            wr = csv.writer(file)
            for d in data:
                wr.writerow(d)
            logging.info(f"{len(data)} rows complete!")
