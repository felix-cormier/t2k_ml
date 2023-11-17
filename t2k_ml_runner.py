import argparse
import subprocess
import time
import os

from wcsim_options import WCSimOptions
from skdetsim_options import SKDETSimOptions
from DataTools.root_utils.merge_h5 import combine_files
from fitqun_class import fitqun

import h5py
import numpy as np

parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
parser.add_argument("--doWCSim", help="run WCSim", action="store_true")
parser.add_argument("--dofiTQun", help="run fiTQun", action="store_true")
parser.add_argument("--doSKDETSim", help="run SKDETSim", action="store_true")
parser.add_argument("--skdetsim", help="run SKDETSim", action="store_true")
parser.add_argument("--doTransform", help="transform WCSim root file to numpy", action="store_true")
#parser.add_argument("--skdetsim", help="Use if transforming skdetsim file (will be wcsim if left off)", action="store_true")
parser.add_argument("--doBatch", help="use the batch system", action="store_true")
parser.add_argument("--doCombination", help="use the batch system", action="store_true")
parser.add_argument("--makeVisualizations", help="make 3D plots of events", action="store_true")
parser.add_argument("--makeInputPlots", help="make 3D plots of events", action="store_true")
parser.add_argument("--useIndexFile", help="use index file to select events when making input plots", action="store_true")
parser.add_argument("--dumpOptions", help="make 3D plots of events", action="store_true")
parser.add_argument("--transformPath", help="path to files to transform")
parser.add_argument("--transformName", help="Name of files to transform")
parser.add_argument("--output_path", help="Path to output for batch jobs")
parser.add_argument("--input_vis_file_path", help="Where to output visualizations")
parser.add_argument("--input_plot_path", help="Directory where to get .hy files from which to make plots")
parser.add_argument("--index_file_path", help="Directory where to get index file")
parser.add_argument("--output_vis_path", help="Where to output visualizations")
parser.add_argument("--output_plot_path", help="Where to output plots")
parser.add_argument("--input_combination_path", help="Path to directory to combine .hy files")
parser.add_argument("--output_combination_path", help="Path to directory where the output of combination is saved ")
parser.add_argument("--input_fitqun_path", help="Path to directory where fitqun file is")
parser.add_argument("--output_fitqun_path", help="Where to output fitqun results")
parser.add_argument("--fitqun_directories", help="Where to find .root files to run fitqun on (should be .txt file of paths)")
parser.add_argument("--eventsPerJob", help="Batch Generation: number to generate per job")
parser.add_argument("--numJobs", help="Batch Generation: Number of jobs to submit")
parser.add_argument("--doSKGeofile", help="Convert SKDETSIM .txt geofile to numpy format", action="store_true")
parser.add_argument("--inputSKGeofile", help="Convert SKDETSIM .txt geofile to numpy format")
parser.add_argument("--outputSKGeofile", help="Convert SKDETSIM .txt geofile to numpy format")
parser.add_argument("--makeEnergyFlat", help="Re-sample data to create a flat visible menergy distribution", action="store_true")
args = parser.parse_args(['--transformPath','foo','@args_ml.txt',
                   '--output_path','foo','@args_ml.txt',
                   '--input_vis_file_path','foo','@args_ml.txt',
                   '--output_vis_path','foo','@args_ml.txt',
                   '--input_plot_path','foo','@args_ml.txt',
                   '--output_plot_path','foo','@args_ml.txt',
                   '--input_combination_path','foo','@args_ml.txt',
                   '--output_combination_path','foo','@args_ml.txt',
                   '--input_fitqun_path','foo','@args_ml.txt',
                   '--output_fitqun_path','foo','@args_ml.txt',
                   '--fitqun_directories','foo','@args_ml.txt',
                   '--eventsPerJob','foo','@args_ml.txt',
                   '--numJobs','foo','@args_ml.txt',
                   '--inputSKGeofile','foo','@args_ml.txt',
                   '--outputSKGeofile','foo','@args_ml.txt',
                   '--transformName','foo','@args_ml.txt'])

if args.doBatch and args.dofiTQun and args.doTransform:
    #Making output directory if it doesn't exist already
    if not(os.path.exists(args.output_fitqun_path) and os.path.isdir(args.output_fitqun_path)):
        try:
            os.makedirs(args.output_fitqun_path)
        except FileExistsError as error:
            print("path " + str(args.output_fitqun_path) +" already exists")
    fitqun_settings = fitqun(args.input_fitqun_path, args.output_fitqun_path, args.fitqun_directories)
    for i, (file, label) in enumerate(zip(fitqun_settings.zbs_files, fitqun_settings.labels)):
        if file is None:
            continue
        temp_number = fitqun_settings.get_number_from_rootfile(file)
        talk = ('sbatch  --account=rpp-blairt2k --mem-per-cpu=4096M --nodes=1 --ntasks-per-node=1 --time=03:00:00 --export=ALL,ARG1='+str(file)+',ARG2='+str(args.output_fitqun_path)+',ARG3='+str(temp_number)+',ARG4=' + str(label)+' fitqun_job.sh')
        subprocess.call(talk, shell=True)
        #print([m.start() for m in re.finditer('\\n', str(subprocess.check_output(["squeue", "-u", "fcormier"])))])
        if i%50==0:
            num_jobs = str(subprocess.check_output(["squeue", "-u", "fcormier"])).count('\\n')
            while num_jobs > 950:
                time.sleep(10)
                num_jobs = str(subprocess.check_output(["squeue", "-u", "fcormier"])).count('\\n')
                print(f'Num Jobs: {num_jobs}, waiting until < 950')

elif args.dofiTQun and args.doTransform:
    from DataTools.root_utils.event_dump import dump_file_fitqun
    os.system('export LD_LIBRARY_PATH=')
    dump_file_fitqun(args.output_fitqun_path + 'test_fitqun.root ', args.output_fitqun_path+'test', label=1)

elif args.dofiTQun:
    if not(os.path.exists(args.output_fitqun_path) and os.path.isdir(args.output_fitqun_path)):
        try:
            os.makedirs(args.output_fitqun_path)
        except FileExistsError as error:
            print("path " + str(args.output_fitqun_path) +" already exists")

    os.system('source /project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/setup.sh')
    os.system('/project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/fitqun/fiTQun/runfiTQun -r '+args.output_fitqun_path + 'test_fitqun.root ' +args.input_fitqun_path )
    print("Finished running fitqun")


elif args.doSKGeofile:
    print("Converting SKDETSIM geofile to numpy format")
    with open(args.inputSKGeofile) as f:
        num_pmts = sum(1 for _ in open(args.inputSKGeofile))
        print(f'num pmts: {num_pmts}')
        positions = np.empty((num_pmts,3))
        orientations = np.empty((num_pmts,3))
        i=0
        for line in f:
            line_array = line.strip().split(",")
            positions[i][0] = float(line_array[0])
            positions[i][1] = float(line_array[1])
            positions[i][2] = float(line_array[2])
            orientations[i][0] = float(line_array[3])
            orientations[i][1] = float(line_array[4])
            orientations[i][2] = float(line_array[5])
            i=i+1

    print(f'Positions: {positions}')
    print(f'Orientations: {orientations}')

    np.savez('data/geofile_skdetsim',position=positions, orientation=orientations)


elif args.doWCSim and args.doTransform and args.doBatch and args.output_path is not None:
    print("Submitting WCSim jobs")
    num_jobs = int(args.numJobs)
    events_per_job = int(args.eventsPerJob)
    wcsim_options = WCSimOptions(output_directory=args.output_path, save_input_options=False,  energy=[50,400,'MeV'], radius=[1590.,'cm'], halfz=[1710.,'cm'], generator = 'gps', particle='e-')
    #wcsim_options = WCSimOptions(output_directory=args.output_path, save_input_options=False,  energy=[100,1200,'MeV'], radius=[100.,'cm'], halfz=[100.,'cm'], generator = 'gps', particle='gamma')
    wcsim_options.set_output_directory()
    wcsim_options.save_options(args.output_path,'wc_options.pkl')
    print(wcsim_options.particle)

    for i in range(num_jobs):
        talk = ('sbatch  --account=rpp-blairt2k --mem-per-cpu=2G --nodes=1 --ntasks-per-node=1 --time=01:00:00 --export=ALL,ARG1='+str(events_per_job)+',ARG2='+str(args.output_path)+' wcsim_job.sh')
        subprocess.call(talk, shell=True)

elif args.doSKDETSim and args.doTransform and args.doBatch and args.output_path is not None:
    print("Submitting SKDETSim jobs")
    num_jobs = int(args.numJobs)
    events_per_job = int(args.eventsPerJob)
    #particle 11 (e-), 13 (mu-), 22 (gamma), 211 (pion+)
    skdetsim_options = SKDETSimOptions(output_directory=args.output_path, save_input_options=False,  energy=[0.,1000.,'MeV'], particle=211, wall=0.)
    skdetsim_options.set_output_directory()
    skdetsim_options.save_options(args.output_path,'sk_options.pkl')
    print(skdetsim_options.particle)

    for i in range(num_jobs):
        talk = ('sbatch  --account=rpp-blairt2k --mem-per-cpu=4G --nodes=1 --ntasks-per-node=1 --time=00:30:00 --export=ALL,ARG1='+str(events_per_job)+',ARG2='+str(args.output_path)+' skdetsim_job.sh')
        subprocess.call(talk, shell=True)
        print(f'job: {i}/{num_jobs} ({(i/num_jobs)*100:.2f}%)')
        #print([m.start() for m in re.finditer('\\n', str(subprocess.check_output(["squeue", "-u", "fcormier"])))])
        if i%50==0:
            current_num_jobs = str(subprocess.check_output(["squeue", "-u", "fcormier"])).count('\\n')
            while current_num_jobs > 950:
                time.sleep(10)
                current_num_jobs = str(subprocess.check_output(["squeue", "-u", "fcormier"])).count('\\n')
                print(f'Num Jobs: {current_num_jobs}, waiting until < 950')


elif args.doWCSim:
    print("Running WCSim")
    wcsim_options = WCSimOptions(num_events=500, energy=[0,200,'MeV'], radius=[1590.,'cm'], halfz=[1710.,'cm'], generator = 'gps', particle='mu-', output_directory='/scratch/fcormier/t2k/ml/output_wcsim/test_lowEmuons_jul31/')
    wcsim_options.set_options(filename='WCSim_toEdit.mac')
    wcsim_options.run_local_wcsim()

elif args.doTransform and args.doSKDETSim:
    from DataTools.root_utils.event_dump import dump_file_skdetsim
    print("Transform from .root to .h5")
    skdetsim_options = SKDETSimOptions()
    #wcsim_options = wcsim_options.load_options(args.transformPath, 'wc_options.pkl')
    test = dump_file_skdetsim(str(args.transformPath) + '/' + str(args.transformName), str(args.transformPath) + '/' + 'skdetsim_transform', create_image_file=True, create_geo_file=False)


elif args.doSKDETSim:
    print("Running SKDETSim")
    skdetsim_options = SKDETSimOptions(num_events=1000, energy=[100,1200], wall=200, particle=13, output_directory='/scratch/fcormier/t2k/ml/output_skdetsim/test_muons_wall100_jul4/')
    skdetsim_options.set_options(filename='sk4_odtune_toEdit.card')
    skdetsim_options.run_local_skdetsim()

elif args.doTransform:
    from DataTools.root_utils.event_dump import dump_file, dump_file_skdetsim
    print("Transform from ROOT to .h5")
    wcsim_options = WCSimOptions()
    if args.skdetsim:
        test = dump_file_skdetsim(str(args.transformPath) + '/' + str(args.transformName), str(args.transformPath) + '/' + 'wcsim_transform', create_image_file=False, create_geo_file=False)
    #wcsim_options = wcsim_options.load_options(args.transformPath, 'wc_options.pkl')
    else:
        test = dump_file(str(args.transformPath) + '/' + str(args.transformName), str(args.transformPath) + '/' + 'wcsim_transform', create_image_file=False, create_geo_file=False)

if args.makeVisualizations:
    import h5py
    from plot_wcsim import plot_wcsim
    from make_visualizations import make_visualizations
    myfile = h5py.File(args.input_vis_file_path,'r')
    wcsim_options = WCSimOptions(output_directory=args.output_vis_path)
    wcsim_options.set_output_directory()
    make_visualizations(myfile, args.output_vis_path)

if args.doCombination:
    extra_string = 'fitqun'
    combine_files(args.input_combination_path, args.output_combination_path, extra_string)

if args.makeInputPlots:

    from plot_wcsim import plot_wcsim
    wcsim_options = WCSimOptions()
    use_text_file=False
    if ".txt" in args.input_plot_path:
        use_text_file=True
    else:
        try:
            wcsim_options = wcsim_options.load_options(args.input_plot_path, 'sk_options.pkl')
        except FileNotFoundError:
            print(f"NO sk_options.pkl in {args.input_plot_path}")
    wcsim_options.output_directory = args.output_plot_path
    wcsim_options.set_output_directory()
    if args.useIndexFile:
        plot_wcsim(args.input_plot_path, args.output_plot_path, wcsim_options, index_file_path=args.index_file_path, text_file=use_text_file, moreVariables=False)
    else:
        plot_wcsim(args.input_plot_path, args.output_plot_path, wcsim_options, text_file=use_text_file, moreVariables=False)

if args.dumpOptions:
    text_file = open(args.input_plot_path, "r")
    file_paths = text_file.readlines()
    for path in file_paths:
        path = path.strip('\n')
        print(f'New path: {path}')
        wcsim_options = WCSimOptions()
        wcsim_options = wcsim_options.load_options(path, 'wc_options.pkl')
        print(f'Particle: {wcsim_options.particle}')

if args.makeEnergyFlat:
    from flatten_energy import flatten_energy
    use_text_file=False
    if ".txt" in args.input_plot_path:
        use_text_file=True
    flatten_energy(input_path=args.input_plot_path, text_file=use_text_file, overwrite=True)