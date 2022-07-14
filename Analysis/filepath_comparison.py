from pygrok import Grok
import LogObjParser.handle_file as hf
from LogObjParser.pattern import PATH_GROK
from LogObjParser.parser import get_path_objs


class Path_Analysis:
    def __init__(self):
        self.result = list()

    def run(self):
        self.extract_log_from_dir("../logdata")
        self.identify_existing_file_path_pattern()
        self.identify_custom_file_path_pattern()
        hf.output_obj_to_csv(self.result, "../result/analysis/")

    def extract_log_from_dir(self, in_dir: str):
        self.result.append(["Where", "Log", "Existing", "Custom"])
        files = hf.get_filenames(in_dir)
        for file in files:
            log_file = open(f"{in_dir}/{file}", "rt")
            log_lines = log_file.readlines()[:10]
            for log in log_lines:
                self.result.append([file, log])

    def identify_existing_file_path_pattern(self):
        existing_path_grok_pattern = "%{PATH:path}"
        existing_path_grok = Grok(existing_path_grok_pattern)

        for log in self.result[1:]:
            is_path_objs = list()
            find_path_objs = existing_path_grok.regex_obj.findall(log[1])
            for path_obj in find_path_objs:
                is_path_objs.append(path_obj[0])
            log.extend([is_path_objs])

    def identify_custom_file_path_pattern(self):
        for log in self.result[1:]:
            is_path_objs = get_path_objs(log[1], PATH_GROK.regex_obj)
            log.extend([is_path_objs])


path_analysis = Path_Analysis()
path_analysis.run()
