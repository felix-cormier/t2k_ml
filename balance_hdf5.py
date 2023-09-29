import h5py
from tqdm import tqdm
import numpy as np
from plot_wcsim import get_cherenkov_threshold, convert_label
import matplotlib.pyplot as plt

'''
There are a couple different approaches to this problem:
1. Take the minimum bin size and just sample everything to that bin size. 
   This should work since stuff is generated randomly and we can try a few different
   bin sizes to make sure its not too sensitive. Min 1000 events in a bin.
    --> then resave a new HDF5 file (this approach is taken for now)
2. Similar to above but instead resave the indicies file
    --> I'm scared of messing with train/test/valid split here 


- need to also balance for classes in each
- need to make cut on dwall, wall vs lightup # of pmts

The [balance_hdf5.py](balance_hdf5.py) script has been added by Ashley to create a flat distribution in truth visible energy and ensure an equal numbetr classes. More information will be added when it is complete.
'''

def sample_lowest_min_energy(input_path, output_path=None, text_file=False):
    """
    Args:
        input_path (_type_): Path to either .hy file or text file with multiple paths and names of .hy files
        output_path (_type_): Where to save new .hy file
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
    """
    file_paths=input_path
    #Behaviour different depending on format of input (single or multiple files)
    if text_file:
        print(f'Getting files from: {str(input_path)}')
        text_file = open(input_path, "r")
        file_paths = text_file.readlines()

    label = []
    truth_visible_energy = []
    truth_labels = []

    #Loop through all .hy files
    file_paths = file_paths if text_file else [file_paths]
    for j, path in enumerate(file_paths):
        path = path.strip('\n')
        print(f'New path: {path}')
    
        with h5py.File(path+'/digi_combine.hy',mode='r') as h5fw:
            temp_truth_visible_energy = [] 

            temp_truth_labels = [] 

            temp_label = convert_label(np.median(h5fw['labels']))
            temp_truth_labels = np.ravel(h5fw['labels'])

            cheThr = list(map(get_cherenkov_threshold, np.ravel(h5fw['labels'])))

            temp_truth_visible_energy = np.ravel(h5fw['energies']) - cheThr

        truth_visible_energy.append(temp_truth_visible_energy)
        truth_labels.append(temp_truth_labels)
        label.append(temp_label)

    ## explain the process

    granularity = 10
    manual_bins = range(0, 1000+granularity, granularity)
    (n, bins, patches) = plt.hist(truth_visible_energy, label=label, bins=manual_bins, alpha=0.6, histtype='stepfilled')

    min_bin_fill = np.inf
    for i1, i2 in zip(n[0], n[1]):
        if i1 < min_bin_fill:
            min_bin_fill = i1
        if i2 < min_bin_fill:
            min_bin_fill = i2

    print(f'the minimum bin size at a bin size of {granularity} is {min_bin_fill}')

    bin_counts0 = {}
    bin_counts1 = {}
    for right_bound in manual_bins[1:]:
        bin_counts0[f'{right_bound}'] = 0
        bin_counts1[f'{right_bound}'] = 0

    new_truth_visible_energy = [[],[]]
    new_indicies_to_save = [[],[]]

    # can combine loops to assure same # of each class, right now its off by 1
    for i in range(len(truth_visible_energy[0])):
        i0 = truth_visible_energy[0][i]
        if i0 < 0: 
            i0 = 0

        i0_temp = int((abs(i0)//10)*10+10)

        if bin_counts0[f'{i0_temp}'] <= min_bin_fill:
            bin_counts0[f'{i0_temp}'] += 1
            new_truth_visible_energy[0].append(i0) 
            new_indicies_to_save[0].append(i)

    for i in range(len(truth_visible_energy[1])):
        i1 = truth_visible_energy[1][i]
        if i1 < 0: 
            i1 = 0
        i1_temp = int((abs(i1)//10)*10+10) 

        if bin_counts1[f'{i1_temp}'] <= min_bin_fill:
            bin_counts1[f'{i1_temp}'] += 1
            new_truth_visible_energy[1].append(i1)
            new_indicies_to_save[1].append(i)

    # save the new hdf5 file (optional argument)
    if output_path != None: 
        for j, path in enumerate(file_paths):
            path = path.strip('\n')
            print(f'Revisiting: {path}')

            with h5py.File(path+'/digi_combine.hy', mode='r') as h5fw:
                ## THIS MEHTOD ASUMES THE FILE IS ALWAYS TRAVERSED IN THE SAME 
                ## WAY BUT I WILL TEST THIS LATER ON
                keys = h5fw.keys()
                with h5py.File(output_path+f'/digi_combine_balanced_{j}.hy', "w") as new_h5fw:
                    for k in tqdm(keys):
                        new_h5fw[k] = h5fw[k][new_indicies_to_save[j]]

    return truth_visible_energy, label


sample_lowest_min_energy(input_path='plotting_paths.txt', output_path='/fast_scratch_2/aferreira/t2k/ml/data/', text_file=True)