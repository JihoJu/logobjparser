import re
import ast
from typing import List
from FileMangement import FileManagement

PUNCTUATION = r"""!"#$%&'()*+,-.:;<=>?@[\]^_`{|}~ """


class TrainDataGenerator:
    """ Preprocessing or Generate train data for BERT

    [전처리]
    1. file, directory name 에 포함되지 않는 character를 기준으로 split
        - 참고: http://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words
    2. splited word 의 leading, tailing에 '/'를 제외한 모든 punctuation 제거
    3. 정수 혹은 실수로만 이루어진 word 제거

    [문장 생성]
    len_sentence 변수만큼의 word 로 sentence 구성

    [target 값]
    문장 가운데 word 가 filepath obj list(레이블된 값들) 에 포함 -> 1 or not -> 2
    """

    def __init__(self, input_data, len_sentence=5):
        self.data = input_data
        self.output = [["input", "target"]]  # train data set (rows)
        self.sentence_list = []  # 특정 개수의 word 가 포함된 sentence
        self.mid_index = len_sentence // 2  # add_specific_word_to_data에서 추가한 단어를 제외한 word list 시작 index
        self.split_regex = re.compile(r"[\\?%*|\"<>,;=\s{}\[\]]")  # .도 포함 but, 확장자 고려!, ':'를 포함시켜야하나???

    def generate_total_train_set(self):
        """ 전체 train set 생성

        :return: 전체 train set
        """
        for line in self.data:
            train_data = self.transform_train_data(line)
            if train_data:
                self.output += train_data
        return self.output

    def transform_train_data(self, line: list):
        """ A row data 를 train data 변환

        :param line: [log: str, filepath_obj: list]
        :return: train data => [sentence, target] 리스트
        """
        if len(line) != 0:
            log, obj = line
            word_list = self.add_specific_word_to_list(self.preprocessing(log))
            self.sentence_list = self.transform_words_to_sentence(word_list)
            return self.add_target_to_sentence(ast.literal_eval(obj))
        return None

    def check_if_mid_word_is_filepath(self, sentence, path_objs: List):
        """ 문장 내 가운데 단어가 file path list 에 포함되는 지의 여부 확인

        :param sentence: A sentence
        :param path_objs: File path object list
        :return: 문장 내 mid word 가 file path list 에 포함되면 1 or not 0
        """
        return any(sentence.split(" ")[self.mid_index] == path for path in path_objs)

    def add_target_to_sentence(self, filepath_objs: List):
        """ sentence 에 target(정답) 값 추가

        정답: sentence 내 가운데 word 가 filepath -> 1 or not -> 0

        :param filepath_objs: File path object list
        :return: [sentence, target] 리스트
        """
        res = []
        for sentence in self.sentence_list:
            if self.check_if_mid_word_is_filepath(sentence, filepath_objs):
                res.append([sentence, 1])
            else:
                res.append([sentence, 0])
        return res

    def transform_words_to_sentence(self, words) -> List:
        """ 단어 리스트를 특정 개수만큼 sentence 로 변환
        초기 설정한 sentence 에 포함될 단어 개수에 기반해 words -> sentence 변환

        :param words: word list
        :return: sentence list
        """
        return [" ".join(words[i - self.mid_index: i + self.mid_index + 1])
                for i in range(self.mid_index, len(words) - self.mid_index)]

    def add_specific_word_to_list(self, words: List) -> List:
        """ 문장으로 묶을 단어 개수를 고려해 word list 앞, 뒤에 잉여 데이터 추가
        :param words: word list
        :return:
        """
        return ['#'] * self.mid_index + words + ['#'] * self.mid_index

    def split_log_to_word(self, log) -> List:
        """ log split -> strip
        - file, directory name 에 포함되지 않는 character를 기준으로 split
            - 참고: http://en.wikipedia.org/wiki/Filename#Reserved_characters_and_words
        - splited word 의 leading, tailing에 '/'를 제외한 모든 punctuation + 공백 제거

        :param log: A log
        :return: word list
        """
        return [word.strip(PUNCTUATION) for word in self.split_regex.split(log) if word.strip(PUNCTUATION)]

    def preprocessing(self, log) -> List:
        """ log 데이터 전처리
        - splitting log
        - splited word 중 정수/실수인 word 제거

        :param log: A log
        :return: 전처리된 log 내 word list object
        """
        splited_word = self.split_log_to_word(log)
        return [word for word in splited_word if
                not re.match(r'\d*\.?\d+', word) or re.match(r'\d*\.?\d+', word).span()[1] != len(word)]
