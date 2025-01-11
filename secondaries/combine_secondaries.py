import numpy as np
import glob as glob
import h5py
import awkward as ak

import uproot


def extract_rootfiles(rootfiles):
    """Extracts the name (not path) of rootfile from list of bytes provided from secondaries on sukap

    Returns:
        numpy array: indices of which labels match the unique rootfiles
    """
    #rootfiles, indices = np.unique(rootfiles, return_index=True)
    #rootfiles = [x.decode('UTF-8') for x in rootfiles]
    rootfiles = np.char.split(rootfiles,'/')
    rootfiles = [x[-1] for x in rootfiles]
    rootfiles = np.char.split(rootfiles,'_')
    rootfiles = [x[-1] for x in rootfiles]
    rootfiles = np.char.split(rootfiles,'.')
    rootfiles = [x[0] for x in rootfiles]
    return rootfiles

def combine_secondaries(secondaries_filepath, data_filepath):

    secondaries = glob.glob(secondaries_filepath+"/*.root")
    data_files = np.array(glob.glob(data_filepath+"/*.hy"))

    secondary_rootfile_num = extract_rootfiles(secondaries)

    for sec_file, sec_num, data_file in zip(secondaries, secondary_rootfile_num, data_files):
        print(sec_file)
        print(data_files[np.char.find(data_files, sec_num) > 0])
        with uproot.open(sec_file+':h1') as file:

            primary_variables  = ['npar', 'wallv', 'ipv', 'posv', 'dirv', 'pmomv']
            secondaries_variables = ['nscndprt', 'itrkscnd', 'istakscnd', 'vtxscnd', 'pscnd', 'iprtscnd', 'tscnd', 'iprntprt',
                                     'lmecscnd', 'iprnttrk', 'iorgprt', 'iprntidx', 'nchilds', 'ichildidx', 'pprnt', 
                                     'pprntinit', 'vtxprnt', 'iflgscnd']
            
            primary = file.arrays(primary_variables)
            secondary = file.arrays(secondaries_variables)


            print(data_file)
            with h5py.File(data_file, mode='a') as h5fw: 
                for var in primary_variables:
                    print(var)
                    print(primary[var])
                    #h5fw.create_dataset(var, data=primary[var])
                for var in secondaries_variables:
                    #h5fw.create_dataset(var, data=secondary[var])
                    print(var)
                    if "iprntprt" in var or "iprtscnd" in var or "lmecscnd" in var:
                        print(ak.to_dataframe(secondary[var]).to_string())



