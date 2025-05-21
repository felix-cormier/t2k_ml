from wcsim_options import WCSimOptions
import sys
    
if __name__ == '__main__':

    name, num_events, output_directory, job_id = sys.argv
    #print(f"num events: {num_events}, output directory: {output_directory}")

    wcsim_options = WCSimOptions()
    wcsim_options = wcsim_options.load_options('./', 'wc_options.pkl')
    #wcsim_options = WCSimOptions(num_events=num_events, output_directory=output_directory, output_name = 'wcsim_'+job_id+'.root', batch=True)
    wcsim_options.seed = job_id
    wcsim_options.num_events = num_events
    wcsim_options.output_directory = output_directory
    wcsim_options.output_name ='data/wcsim_'+job_id+'.root' 
    wcsim_options.batch = True
    wcsim_options.set_options(filename='WCSim_toEdit.mac')
    wcsim_options.run_local_wcsim()