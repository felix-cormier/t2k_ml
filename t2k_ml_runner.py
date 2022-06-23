import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--doWCSim", help="run WCSim", action="store_true")
parser.add_argument("--doTransform", help="transform WCSim root file to numpy", action="store_true")
args = parser.parse_args()

if args.doWCSim:
    print("Running WCSim")

test=1
print(test)
print(test)