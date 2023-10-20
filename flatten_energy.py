import h5py
from tqdm import tqdm
import numpy as np
from plot_wcsim import get_cherenkov_threshold, convert_label
import matplotlib.pyplot as plt

# can make this more general to flatten along any key given if thats helpful
def flatten_energy(input_path, output_path=None, text_file=False, overwrite=False): 
    """ Introduces new key called 'keep_event' to dataset such that events with keep_event = True 
        constitute a set of events flat in truth visible energy. I've tried to write the code 
        for a general number of labels but it has only been tested for cases of two unique labels.
        This is used within t2l_ml_training.runner_util.make_split_file.

    Args:
        input_path (str): Path to either .hy file or text file with multiple paths and names of .hy files.
        output_path (str, optional): Where to save new .hy file that is more flat in truth visible energy. 
                                     Defaults to None, which means that the outputted file will be under the same 
                                     path as the input file path but with an appended '_flatE' before the .hy.
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
        overwrite (bool, optional): True if instead of creating new file, the 'keep_event' key is added to the input
                                    file. In this case the output file path is disregarded. Defaults to False.       

    Returns:
        truth_visible_energy (list of float): original visible energy values
        label (list of int): original label values
        min_bin_fill (int): minimum bin fill at 10 MeV bin size, forced to be starting from 0

    """

    #Behaviour different depending on format of input (single or multiple files)
    if text_file:
        print(f'Getting files from: {str(input_path)}')
        text_file = open(input_path, "r")
        input_path = text_file.readlines()

    label = []
    truth_visible_energy = []
    truth_labels = []

    #Loop through all .hy files
    input_path = input_path if text_file else [input_path]
    for j, path in enumerate(input_path):
        path = path.strip('\n')
        print(f'New path: {path}')
    
        # read in origional visible energy and label values
        with h5py.File(path+'/digi_combine.hy',mode='r') as h5fw:
            temp_truth_visible_energy, temp_truth_labels = [], []
            temp_label = convert_label(np.median(h5fw['labels']))
            temp_truth_labels = np.ravel(h5fw['labels'])
            cheThr = list(map(get_cherenkov_threshold, np.ravel(h5fw['labels'])))
            temp_truth_visible_energy = np.ravel(h5fw['energies']) - cheThr

        truth_visible_energy.append(temp_truth_visible_energy)
        truth_labels.append(temp_truth_labels)
        label.append(temp_label)

    # create histogram bins and fill them with truth_visible_energy values
    granularity = 10 # MeV/bin
    manual_bins = range(0, 1000+granularity, granularity)
    (n, bins, patches) = plt.hist(truth_visible_energy, label=label, bins=manual_bins)

    # just tested for 2 labels
    unique_labels = len(n) 
    print(f'{unique_labels} unique labels found') 

    # find minimim size of a bin
    min_bin_fill = np.inf
    for i in range(unique_labels):
        for j in range(len(n[i])):
            temp_bin_fill = int(n[i][j])
            if temp_bin_fill < min_bin_fill:
                min_bin_fill = temp_bin_fill
    print(f'the minimum bin fill at a bin size of {granularity} is {min_bin_fill}')

    # make dictionaries to keep track of bins as we refill them
    bin_count_dicts = []
    # save values of truth visible energy to keep and their indicies
    new_truth_visible_energy = []
    new_indicies_to_save = [] 
    for i in range(unique_labels):
        temp_bin_count_dict = {}
        for right_bound in manual_bins[1:]: 
            temp_bin_count_dict[f'{right_bound}'] = 0

        bin_count_dicts.append(temp_bin_count_dict)
        new_truth_visible_energy.append([])
        new_indicies_to_save.append([])

    # loop over each label seperately
    for i in range(unique_labels): 
        for j in range(len(truth_visible_energy[i])):
            temp_energy_val = truth_visible_energy[i][j]
            if temp_energy_val < 0.0: 
                temp_energy_val = 0.0 # set energies a bit below 0 to 0
            temp_bin = int((abs(temp_energy_val)//granularity)*granularity+granularity) # only tested for granularity=10 
            if bin_count_dicts[i][f'{temp_bin}'] < min_bin_fill:
                bin_count_dicts[i][f'{temp_bin}'] += 1
                new_truth_visible_energy[i].append(temp_energy_val) 
                new_indicies_to_save[i].append(j)

        # these numbers should be equal, thats what I observe on my end.
        print(f'number of events for label {i} = {len(new_indicies_to_save[i])}')
    
    # save the hdf5 file(s) with key 'keep_event' key
    for i, path in enumerate(input_path):
        path = path.strip('\n')
        print(f'Revisiting: {path}')

        # create a boolean area where values are True for events to keep
        bool_array = np.zeros(len(truth_visible_energy[i]), dtype=bool)
        bool_array[new_indicies_to_save[i]] = True

        # if overwrite is True then add the 'keep_event' key to input file
        if overwrite:
            output_path = path + '/digi_combine.hy'
            with h5py.File(output_path, mode='a') as h5fw: 
                h5fw.create_dataset('keep_event', data=bool_array)

            print(f'"keep_event" key added to original HDF5 file: {output_path}') 
            
        # otherwise create copy of the input file and add the 'keep_event' key to the copy
        else:
            # give default output file name if none are specified
            if output_path == None:
                temp_output_path = path + '/digi_combine_flatE.hy' # this is the issue

            # read in original file 
            with h5py.File(path+'/digi_combine.hy', mode='r') as h5fw:
                keys = h5fw.keys()

                # open new file to save data to 
                with h5py.File(temp_output_path, 'w') as new_h5fw:
                    
                    # save data from selected indicies for each of the keys in original data
                    for k in tqdm(keys):
                        new_h5fw.create_dataset(k, data=h5fw[k])

                    # add in the new key
                    new_h5fw.create_dataset('keep_event', data=bool_array)

            print(f'new HDF5 file with "keep_event" key saved to: {temp_output_path}') 
                        
    return truth_visible_energy, label, min_bin_fill

# run the function only if program is run directly, not called on to import the function
if __name__ == '__main__':
    truth_visible_energy, label, min_bin_fill = flatten_energy(input_path='plotting_paths.txt', 
                                                                output_path=None, 
                                                                text_file=True, overwrite=False)