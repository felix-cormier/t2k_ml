import h5py
from tqdm import tqdm
import numpy as np
from plot_wcsim import get_cherenkov_threshold, convert_label
import matplotlib.pyplot as plt

def sample_lowest_min_energy(input_path, output_path=None, text_file=False, overwrite=False): 
    """ Introduces new key called 'keep_event' to dataset such that events with keep_event = True 
        constitute a set of events balanced in truth visible energy. I've tried to write the code 
        for a general number of labels but it has only been tested for cases of two unique labels.
        This is used within t2l_ml_training.runner_util.make_split_file.

    Args:
        input_path (str): Path to either .hy file or text file with multiple paths and names of .hy files.
        output_path (str, optional): Where to save new .hy file that is more balanced in truth visible energy. 
                                     Defaults to None, which means that the outputted file will be under the same 
                                     path as the input file but with an appended '_balanced' before the .hy.
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
        overwrite (bool, optional): True if instead of creating new file, the 'keep_event' key is added to the input
                                    file. In this case the output file path is disregarded. Defaults to False.       

    Returns:
        truth_visible_energy (list of float): 
        label (list of int):
        min_bin_fill (int):

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

    unique_labels = unique_labels  # check this and use it later on
    print(f'{unique_labels} unique labels found') # name balanxe e

    # find minimim size of a bin
    min_bin_fill = np.inf
    for i in range(unique_labels):
        for j in range(len(n[i])):
            temp_bin_fill = n[i][j]
            if temp_bin_fill < min_bin_fill:
                min_bin_fill = temp_bin_fill
    print(f'the minimum bin fill at a bin size of {granularity} is {min_bin_fill}')

    # make dictionaries to keep track of bins as we refill them
    bin_count_dicts = []
    for i in range(unique_labels):
        temp_bin_count_dict = {}
        for right_bound in manual_bins[1:]: 
            temp_bin_count_dict[f'{right_bound}'] = 0
        bin_count_dicts.append(temp_bin_count_dict)

    # save values of truth visible energy to keep and their indicies
    new_truth_visible_energy = [[],[]]
    new_indicies_to_save = [[],[]]  # append as part of loop

    # up until bins fill to min_bin_fill XXXXXXXXXXXX
    #

    # loop over each label seperately
    for i in range( ) 
    for i in range(len(truth_visible_energy[0])):
        i0 = truth_visible_energy[0][i]
        if i0 < 0: 
            i0 = 0 # set energies a bit below 0 to 0
        i0_temp = int((abs(i0)//10)*10+10) # just works for granularity=10 right now
        if bin_counts0[f'{i0_temp}'] < min_bin_fill:
            bin_counts0[f'{i0_temp}'] += 1
            new_truth_visible_energy[0].append(i0) 
            new_indicies_to_save[0].append(i)

        # deal with data from second label (may want to combine more)
    for i in range(len(truth_visible_energy[1])):
        i1 = truth_visible_energy[1][i]
        if i1 < 0: 
            i1 = 0
        i1_temp = int((abs(i1)//10)*10+10) 
        if bin_counts1[f'{i1_temp}'] < min_bin_fill:
            bin_counts1[f'{i1_temp}'] += 1
            new_truth_visible_energy[1].append(i1)
            new_indicies_to_save[1].append(i)

    # these numbers should be equal, thats what I observe on my end.
    print(f'number of events for label 0 = {len(new_indicies_to_save[0])}\n number of events for label 1 = {len(new_indicies_to_save[1])}')
    
    
    ## save the new hdf5 file (if optional argument is included)
    if output_path != None: 

        # loop over file list again
        for j, path in enumerate(input_path):
            path = path.strip('\n')
            print(f'Revisiting: {path}')

            # 
            bool_array = np.zeros(len(truth_visible_energy[j]), dtype=bool)
            bool_array[new_indicies_to_save[j]] = True

            if overwrite: # not tested yet
                with h5py.File(path+'/digi_combine.hy', mode='a') as h5fw: 
                    h5fw.create_dataset('keep_event', data=bool_array)

            else:
                with h5py.File(path+'/digi_combine.hy', mode='r') as h5fw:
                    keys = h5fw.keys()

                    # open new file to save data to 
                    with h5py.File(output_path+f'/digi_combine_balanced_0dwallcut_{j}.hy', 'w') as new_h5fw:
                        
                        # save data from selected indicies for each of the keys in original data
                        for k in tqdm(keys):
                            ## THIS DOES NOT WORK NOW, need to revisit it ##
                            new_h5fw[k] = h5fw[k]#[new_indicies_to_save[j]] - not useful option anymore

                        new_h5fw['keep_event'] = bool_array
                        
    
                       
    return truth_visible_energy, label, min_bin_fill # should this be new_truth_visible_energy? what is it used for
    
if __name__ == '__main__':
    # run the function
    sample_lowest_min_energy(input_path='plotting_paths.txt', output_path='/fast_scratch_2/aferreira/t2k/ml/data/', text_file=True, overwrite=True)