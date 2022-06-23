import argparse
from wcsim_options import WCSimOptions

parser = argparse.ArgumentParser()
parser.add_argument("--doWCSim", help="run WCSim", action="store_true")
parser.add_argument("--doTransform", help="transform WCSim root file to numpy", action="store_true")
args = parser.parse_args()

if args.doWCSim:
    print("Running WCSim")
    wcsim_options = WCSimOptions(num_events=10)
    wcsim_options.set_options(filename='WCSim_toEdit.mac')
    wcsim_options.run_local_wcsim()


test=1
print(test)
print(test)