from wcsim_options import WCSimOptions
from DataTools.root_utils.event_dump import dump_file

import sys
    
if __name__ == '__main__':

    name, output_directory, job_id= sys.argv

    wcsim_options = WCSimOptions()
    wcsim_options = wcsim_options.load_options('./', 'wc_options.pkl')
    test = dump_file(str(output_directory) + '/' +'wcsim_'+job_id+'.root', str(output_directory) + '/' + 'wcsim_transform_' + job_id)