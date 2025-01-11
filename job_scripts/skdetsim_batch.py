from skdetsim_options import SKDETSimOptions
import sys

import numpy as np
    
if __name__ == '__main__':

    name, num_events, output_directory, job_id = sys.argv
    #print(f"num events: {num_events}, output directory: {output_directory}")

    skdetsim_options = SKDETSimOptions()
    skdetsim_options = skdetsim_options.load_options('./', 'sk_options.pkl')
    #skdetsim_options = skdetsimOptions(num_events=num_events, output_directory=output_directory, output_name = 'skdetsim_'+job_id+'.root', batch=True)
    skdetsim_options.seed = job_id
    rng = np.random.default_rng(int(job_id))
    skdetsim_options.seed_2 = rng.integers(low=0, high=10000000)
    skdetsim_options.seed_3 = rng.integers(low=0, high=10000000)
    skdetsim_options.num_events = num_events
    skdetsim_options.output_directory = output_directory
    skdetsim_options.output_name ='data/skdetsim_'+job_id+'.root' 
    skdetsim_options.batch = True
    skdetsim_options.set_options(filename='sk4_odtune_toEdit.card')
    skdetsim_options.run_local_skdetsim()