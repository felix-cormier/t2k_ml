from skdetsim_options import SKDETSimOptions
import sys
import os
    
if __name__ == '__main__':

    name, file, output_directory,  = sys.argv
    #print(f"num events: {num_events}, output directory: {output_directory}")

    skdetsim_options = SKDETSimOptions(output_directory=output_directory)
    skdetsim_options = skdetsim_options.load_options('./', 'sk_options.pkl')
    filename = os.path.basename(file)
    #skdetsim_options = skdetsimOptions(num_events=num_events, output_directory=output_directory, output_name = 'skdetsim_'+job_id+'.root', batch=True)
    skdetsim_options.output_name ='data/'+str(filename[:-4]) 
    skdetsim_options.run_local_zbs2root()