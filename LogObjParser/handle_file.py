import os
import csv


def get_filenames(dir_path: str):
    """ Extract all file names from that directory """

    if not os.path.isdir(dir_path):
        print("해당 디렉터리가 존재하지 않습니다.")
        return 0
    file_list = os.listdir(dir_path)

    return file_list


def extract_log_from_path(in_path: str):
    """
        Extract from the path to log data str object
    """

    if os.path.isfile(in_path):  # in_path 가 file 인 경우 : 파일 전체 log data
        log_data = extract_log_from_file(in_path)
    elif os.path.isdir(in_path):  # in_path 가 directory 인 경우 : 각 파일 50 줄 log data
        log_data = extract_log_from_dir(in_path)
    else:  # 해당 경로에 파일 혹은 디렉터리가 존재 X
        print("해당 경로에 파일 혹은 디렉터리가 존재하지 않습니다.")
        return None
    return log_data


def extract_log_from_dir(in_dir: str):
    """
        Extract from directory to log data str object

        각 파일 내 로그 한 줄씩 리스트 추가
    """

    log_data = list()

    if in_dir[-1] == "/":  # in_dir 가 "./logdata/" 의 형태를 띄는 경우
        in_dir = in_dir[:-1]

    files = get_filenames(in_dir)
    for file in files:
        log_file = open(f"{in_dir}/{file}", "rt")
        log_lines = log_file.readlines()[:20000]
        log_data.extend(log_lines)

    return log_data


def extract_log_from_file(in_file: str):
    """
        Extract from a file to log data str object
    """

    log_data = list()

    log_file = open(f"{in_file}", "rt")
    log_lines = log_file.readlines()
    log_data.extend(log_lines)

    return log_data


def output_obj_to_csv(datas, out_dir="./result/"):
    """ Show obj in csv format """

    file = open(f"{out_dir}result.csv", "w")
    writer = csv.writer(file)

    for data in datas:
        writer.writerow(data)

    file.close()
