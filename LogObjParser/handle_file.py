import os
import csv


def get_filenames(dir_path: str):
    """ Extract all file names from that directory """

    if not os.path.isdir(dir_path):
        print("해당 디렉터리가 존재하지 않습니다.")
        return 0
    file_list = os.listdir(dir_path)

    return file_list


def extract_log_from_files(indir: str):

    """
        Extract from all files to log data str object

        각 파일 내 로그 한 줄씩 리스트 추가
    """

    log_data = list()

    files = get_filenames(indir)
    for file in files:
        log_file = open(f"{indir}{file}", "rt")
        log_lines = log_file.readlines()[:50]
        log_data.extend(log_lines)

    return log_data


def output_obj_to_csv(datas, outdir="./"):
    """ Show obj in csv format """

    file = open(f"{outdir}result.csv", "w")
    writer = csv.writer(file)

    for data in datas:
        writer.writerow(data)

    file.close()
