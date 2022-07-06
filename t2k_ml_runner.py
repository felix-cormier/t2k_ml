import argparse
import os
import subprocess

from wcsim_options import WCSimOptions

parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument("--doWCSim", help="run WCSim", action="store_true")
parser.add_argument("--doTransform", help="transform WCSim root file to numpy", action="store_true")
parser.add_argument("--doBatch", help="use the batch system", action="store_true")
parser.add_argument("--transformPath", help="path to files to transform")
parser.add_argument("--transformName", help="Name of files to transform")
parser.add_argument("--output_path", help="Path to output for batch jobs")
parser.add_argument("--eventsPerJob", help="Batch Generation: number to generate per job")
parser.add_argument("--numJobs", help="Batch Generation: Number of jobs to submit")
args = parser.parse_args(['--transformPath','foo','@args_ml.txt',
                   '--output_path','foo','@args_ml.txt',
                   '--eventsPerJob','foo','@args_ml.txt',
                   '--numJobs','foo','@args_ml.txt',
                   '--transformName','foo','@args_ml.txt'])

if args.doWCSim and args.doTransform and args.doBatch and args.output_path is not None:
    print("Submitting jobs")
    num_jobs = int(args.numJobs)
    events_per_job = int(args.eventsPerJob)

    for i in range(num_jobs):
        talk = ('sbatch  --mem-per-cpu=2G --nodes=1 --ntasks-per-node=1 --time=00:05:00 --export=ALL,ARG1='+str(events_per_job)+',ARG2='+str(args.output_path)+' wcsim_job.sh')
        subprocess.call(talk, shell=True)


elif args.doWCSim:
    print("Running WCSim")
    wcsim_options = WCSimOptions(num_events=10, generator = 'gps', particle='e-', output_directory='/scratch/fcormier/t2k/ml/output_wcsim/test/')
    wcsim_options.set_options(filename='WCSim_toEdit.mac')
    wcsim_options.run_local_wcsim()

elif args.doTransform:
    from DataTools.root_utils.event_dump import dump_file
    print("Transform from ROOT to .h5")
    wcsim_options = WCSimOptions()
    wcsim_options = wcsim_options.load_options(args.transformPath, 'wc_options.pkl')
    test = dump_file(str(args.transformPath) + '/' + str(args.transformName), str(args.transformPath) + '/' + 'wcsim_transform')


test=1
print(test)
print(test)