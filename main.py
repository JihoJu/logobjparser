from LogObjParser import handle_file, LogObjParser

INPUT_DIR = "./logdata/"

if __name__ == '__main__':
    log_data = handle_file.extract_log_from_files(INPUT_DIR)
    logparser = LogObjParser.LogParser(log_data)
    obj_data = logparser.parse()
    handle_file.output_obj_to_csv(obj_data)
