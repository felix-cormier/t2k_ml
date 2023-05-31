import argparse
import os
import subprocess

from wcsim_options import WCSimOptions
from DataTools.root_utils.merge_h5 import combine_files

import h5py

parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument("--doWCSim", help="run WCSim", action="store_true")
parser.add_argument("--doTransform", help="transform WCSim root file to numpy", action="store_true")
parser.add_argument("--doBatch", help="use the batch system", action="store_true")
parser.add_argument("--doCombination", help="use the batch system", action="store_true")
parser.add_argument("--makeVisualizations", help="make 3D plots of events", action="store_true")
parser.add_argument("--makeInputPlots", help="make 3D plots of events", action="store_true")
parser.add_argument("--dumpOptions", help="make 3D plots of events", action="store_true")
parser.add_argument("--transformPath", help="path to files to transform")
parser.add_argument("--transformName", help="Name of files to transform")
parser.add_argument("--output_path", help="Path to output for batch jobs")
parser.add_argument("--input_vis_file_path", help="Where to output visualizations")
parser.add_argument("--input_plot_path", help="Directory where to get .hy files from which to make plots")
parser.add_argument("--output_vis_path", help="Where to output visualizations")
parser.add_argument("--output_plot_path", help="Where to output plots")
parser.add_argument("--input_combination_path", help="Path to directory to combine .hy files")
parser.add_argument("--output_combination_path", help="Path to directory where the output of combination is saved ")
parser.add_argument("--eventsPerJob", help="Batch Generation: number to generate per job")
parser.add_argument("--numJobs", help="Batch Generation: Number of jobs to submit")
args = parser.parse_args(['--transformPath','foo','@args_ml.txt',
                   '--output_path','foo','@args_ml.txt',
                   '--input_vis_file_path','foo','@args_ml.txt',
                   '--output_vis_path','foo','@args_ml.txt',
                   '--input_plot_path','foo','@args_ml.txt',
                   '--output_plot_path','foo','@args_ml.txt',
                   '--input_combination_path','foo','@args_ml.txt',
                   '--output_combination_path','foo','@args_ml.txt',
                   '--eventsPerJob','foo','@args_ml.txt',
                   '--numJobs','foo','@args_ml.txt',
                   '--transformName','foo','@args_ml.txt'])


if args.doWCSim and args.doTransform and args.doBatch and args.output_path is not None:
    print("Submitting jobs")
    num_jobs = int(args.numJobs)
    events_per_job = int(args.eventsPerJob)
    wcsim_options = WCSimOptions(output_directory=args.output_path, save_input_options=False,  energy=[0,1200,'MeV'], radius=[1690.,'cm'], halfz=[1750.,'cm'], generator = 'gps', particle='gamma')
    wcsim_options.set_output_directory()
    wcsim_options.save_options(args.output_path,'wc_options.pkl')
    print(wcsim_options.particle)

    for i in range(num_jobs):
        talk = ('sbatch  --account=rpp-blairt2k --mem-per-cpu=4G --nodes=1 --ntasks-per-node=1 --time=02:00:00 --export=ALL,ARG1='+str(events_per_job)+',ARG2='+str(args.output_path)+' wcsim_job.sh')
        subprocess.call(talk, shell=True)


elif args.doWCSim:
    print("Running WCSim")
    wcsim_options = WCSimOptions(num_events=500, energy=[0,1200,'MeV'], radius=[1690.,'cm'], halfz=[1750.,'cm'], generator = 'gps', particle='gamma', output_directory='/scratch/ipress/')
    wcsim_options.set_options(filename='WCSim_toEdit.mac')
    wcsim_options.run_local_wcsim()

elif args.doTransform:
    from DataTools.root_utils.event_dump import dump_file
    print("Transform from ROOT to .h5")
    wcsim_options = WCSimOptions()
    #wcsim_options = wcsim_options.load_options(args.transformPath, 'wc_options.pkl')
    test = dump_file(str(args.transformPath) + '/' + str(args.transformName), str(args.transformPath) + '/' + 'wcsim_transform', create_image_file=False, create_geo_file=False)

if args.makeVisualizations:
    from plot_wcsim import plot_wcsim
    from make_visualizations import make_visualizations
    myfile = h5py.File(args.input_vis_file_path,'r')
    wcsim_options = WCSimOptions(output_directory=args.output_vis_path)
    wcsim_options.set_output_directory()
    make_visualizations(myfile, args.output_vis_path)

if args.doCombination:
    extra_string = 'digi'
    combine_files(args.input_combination_path, args.output_combination_path, extra_string)

if args.makeInputPlots:

    from plot_wcsim import plot_wcsim
    wcsim_options = WCSimOptions()
    use_text_file=False
    if ".txt" in args.input_plot_path:
        use_text_file=True
    else:
        wcsim_options = wcsim_options.load_options(args.input_plot_path, 'wc_options.pkl')
    wcsim_options.output_directory = args.output_plot_path
    wcsim_options.set_output_directory()
    plot_wcsim(args.input_plot_path, args.output_plot_path, wcsim_options, text_file=use_text_file, truthOnly=False)

if args.dumpOptions:
    text_file = open(args.input_plot_path, "r")
    file_paths = text_file.readlines()
    for path in file_paths:
        path = path.strip('\n')
        print(f'New path: {path}')
        wcsim_options = WCSimOptions()
        wcsim_options = wcsim_options.load_options(path, 'wc_options.pkl')
        print(f'Particle: {wcsim_options.particle}')


