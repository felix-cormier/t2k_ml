import argparse
from wcsim_options import WCSimOptions
from DataTools.root_utils.event_dump import dump_file

parser = argparse.ArgumentParser()
parser.add_argument("--doWCSim", help="run WCSim", action="store_true")
parser.add_argument("--doTransform", help="transform WCSim root file to numpy", action="store_true")
args = parser.parse_args()

if args.doWCSim:
    print("Running WCSim")
    wcsim_options = WCSimOptions(num_events=10, output_directory='/scratch/fcormier/t2k/ml/output_wcsim/test/')
    wcsim_options.set_options(filename='WCSim_toEdit.mac')
    wcsim_options.run_local_wcsim()

if args.doTransform:
    wcsim_options = WCSimOptions()


test=1
print(test)
print(test)