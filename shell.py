import sys
import click
from LogObjParser.LogParser import LogParser
from Analysis import Path_Analysis

BASIC_PATH = "./logdata/"


@click.command()
@click.option("--path", '-p', help="Enter the file or directory path in str format", required=True)  # 파일 or 폴더 경로 입력
@click.option("--test", '-test', help="Enter the file or directory path in str format")
def main(path=BASIC_PATH, test=None):
    if test == "path":
        return Path_Analysis.Path_Analysis().run(path)
    else:
        return LogParser(path).run()  # LogObjParser 객체 실행


if __name__ == '__main__':
    sys.exit(main())
