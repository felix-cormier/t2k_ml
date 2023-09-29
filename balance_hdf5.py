import h5py
from tqdm import tqdm
import numpy as np
from plot_wcsim import get_cherenkov_threshold, convert_label
import matplotlib.pyplot as plt

def sample_lowest_min_energy(input_path, output_path=None, text_file=False):
    """
    Args:
        input_path (str): Path to either .hy file or text file with multiple paths and names of .hy files
        output_path (str, optional): Where to save new .hy file that is more balanced in truth visible energy
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

    ## create histogra, bins and find minimim size and find minimum one
    granularity = 10 # MeV/bin
    manual_bins = range(0, 1000+granularity, granularity)
    (n, bins, patches) = plt.hist(truth_visible_energy, label=label, bins=manual_bins, alpha=0.6, histtype='stepfilled')

    min_bin_fill = np.inf
    for i1, i2 in zip(n[0], n[1]):
        if i1 < min_bin_fill:
            min_bin_fill = i1
        if i2 < min_bin_fill:
            min_bin_fill = i2

    print(f'the minimum bin size at a bin size of {granularity} is {min_bin_fill}')

    ## make dictionaries to keep track of bins as we refill them
    bin_counts0 = {}
    bin_counts1 = {}
    for right_bound in manual_bins[1:]: 
        bin_counts0[f'{right_bound}'] = 0
        bin_counts1[f'{right_bound}'] = 0

    ## save values of truth visible energy and their indicies up until bins fill to min_bin_fill
    new_truth_visible_energy = [[],[]]
    new_indicies_to_save = [[],[]]

    # to be safe (or else, when they are seperate there seems to be +1 of one of our labels)
    loop_len = min(len(truth_visible_energy[0]), len(truth_visible_energy[1]))

    for i in range(loop_len):
        # deal with data from first label
        i0 = truth_visible_energy[0][i]
        if i0 < 0: 
            i0 = 0
        i0_temp = int((abs(i0)//10)*10+10) # just works for granularity=10 right now
        if bin_counts0[f'{i0_temp}'] <= min_bin_fill:
            bin_counts0[f'{i0_temp}'] += 1
            new_truth_visible_energy[0].append(i0) 
            new_indicies_to_save[0].append(i)

        # deal with data from second label (may want to combine more)
        i1 = truth_visible_energy[1][i]
        if i1 < 0: 
            i1 = 0
        i1_temp = int((abs(i1)//10)*10+10) 
        if bin_counts1[f'{i1_temp}'] <= min_bin_fill:
            bin_counts1[f'{i1_temp}'] += 1
            new_truth_visible_energy[1].append(i1)
            new_indicies_to_save[1].append(i)

    print(f'number of events for label 0 = {len(new_indicies_to_save[0])}\n number of events for label 1 = {len(new_indicies_to_save[1])}')

    # save the new hdf5 file (if optional argument is included)
    if output_path != None: 
        for j, path in enumerate(file_paths):
            path = path.strip('\n')
            print(f'Revisiting: {path}')

            with h5py.File(path+'/digi_combine.hy', mode='r') as h5fw:
                ## THIS MEHTOD ASUMES THE FILE IS ALWAYS TRAVERSED IN THE SAME 
                ## WAY BUT I WILL TEST THIS LATER ON
                # it has a lot of trouble with this second iteration, not sure why
                # --> do it seperately?
                keys = h5fw.keys()
                with h5py.File(output_path+f'/digi_combine_balanced4_{j}.hy', 'w') as new_h5fw:
                    for k in tqdm(keys):
                        new_h5fw[k] = h5fw[k][new_indicies_to_save[j]]
                        print(new_h5fw[k][0])

    return truth_visible_energy, label


sample_lowest_min_energy(input_path='plotting_paths.txt', output_path='/fast_scratch_2/aferreira/t2k/ml/data/', text_file=True)