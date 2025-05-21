import sys
sys.path.append(f"{sys.path[0]}/../")
from DataTools.root_utils.merge_h5 import combine_files

name, input_combination_path, output_combination_path, extra_string  = sys.argv
use_text_file=False
file_paths=None
if ".txt" in input_combination_path:
    use_text_file=True
    extra_string = 'multi'
    text_file = open(input_combination_path, "r")
    file_paths = text_file.readlines()
    print(file_paths)
    num_files = len(file_paths)
combine_files(input_combination_path, output_combination_path, extra_string, specific_files=file_paths)