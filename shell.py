import sys
import click
from LogObjParser import LogObjParser

BASIC_PATH = "./logdata/"


@click.command()
@click.option("--path", '-p', help="Enter the file or directory path in str format", required=True)  # 파일 or 폴더 경로 입력
def main(path=BASIC_PATH):
    return LogObjParser.LogParser(path).run()  # LogObjParser 객체 실행


if __name__ == '__main__':
    sys.exit(main())
