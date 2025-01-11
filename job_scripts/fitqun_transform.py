import sys

from DataTools.root_utils.event_dump import dump_file_fitqun

from fitqun_class import get_filename_no_type
    
if __name__ == '__main__':
    if len(sys.argv) == 4:
        name, output_directory, job_id, label = sys.argv
        dump_file_fitqun(output_directory + 'test_'+str(job_id)+'_fitqun.root ', output_directory+'test_'+job_id, label=label)
    elif len(sys.argv) == 3:
        name, output_directory, input_file = sys.argv
        output_filename = get_filename_no_type(input_file)
        print(input_file)
        print(output_directory)
        print(output_filename)
        dump_file_fitqun(input_file, output_directory+'/'+output_filename, label=-1, customTree=False)