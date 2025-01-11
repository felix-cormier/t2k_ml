from wcsim_options import WCSimOptions
from skdetsim_options import SKDETSimOptions
from DataTools.root_utils.event_dump import dump_file, dump_file_skdetsim

import sys
import os
    
if __name__ == '__main__':

    #WCSim
    if len(sys.argv) == 3:
        name, output_directory, job_id= sys.argv
        wcsim_options = WCSimOptions()
        wcsim_options = wcsim_options.load_options('./', 'wc_options.pkl')
        test = dump_file(str(output_directory) + '/' +'wcsim_'+job_id+'.root', str(output_directory) + '/' + 'wcsim_transform_' + job_id)
    #SKDETSim
    elif len(sys.argv) == 4: 
        print("Running transform batch for SKDETSim")
        name, output_directory, job_id, _= sys.argv
        skdetsim_options = SKDETSimOptions()
        wcsim_options = skdetsim_options.load_options('./', 'sk_options.pkl')
        test = dump_file_skdetsim(str(output_directory) + '/' +'skdetsim_'+job_id+'.root', str(output_directory) + '/' + 'skdetsim_transform_' + job_id)
    #ZBS2ROOT only
    elif len(sys.argv) == 2: 
        print("Running transform batch for ZBS2ROOT")
        name, file_path, = sys.argv
        filename = os.path.basename(file_path)
        skdetsim_options = SKDETSimOptions()
        wcsim_options = skdetsim_options.load_options('./', 'sk_options.pkl')
        test = dump_file_skdetsim('data/'+filename[:-4]+'.root', 'data/'+filename[:-4])
