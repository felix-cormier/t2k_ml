from wcsim_options import WCSimOptions
import sys
    
if __name__ == '__main__':

    name, num_events, output_directory, job_id = sys.argv
    #print(f"num events: {num_events}, output directory: {output_directory}")

    wcsim_options = WCSimOptions(num_events=num_events, generator = 'gps', particle='e-', output_directory=output_directory, output_name = 'wcsim_'+job_id+'.root', batch=True)
    wcsim_options.set_options(filename='WCSim_toEdit.mac')
    wcsim_options.run_local_wcsim()