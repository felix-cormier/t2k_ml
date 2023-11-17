import sys

from DataTools.root_utils.event_dump import dump_file_fitqun
    
if __name__ == '__main__':
    name, output_directory, job_id, label = sys.argv
    dump_file_fitqun(output_directory + 'test_'+str(job_id)+'_fitqun.root ', output_directory+'test_'+job_id, label=label)