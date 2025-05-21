import sys
import os
from DataTools.root_utils.event_dump import dump_file_secondaries
    


if __name__ == '__main__':

    name, file, output_directory, file_num = sys.argv
    #print(f"num events: {num_events}, output directory: {output_directory}")
    test = dump_file_secondaries(file, str(output_directory) + '/' + 'secondaries_transform_' + file_num +'.hy')

def transform_secondaries(file, output_directory, file_num):
    test = dump_file_secondaries(file, str(output_directory) + '/' + 'secondaries_transform_' + file_num +'.hy')
