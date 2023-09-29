import h5py
import numpy as np
import os
from plot_wcsim import calculate_wcsim_wall_variables, load_geofile, convert_values, convert_label, get_cherenkov_threshold
import matplotlib.pyplot as plt

def plot_walls(input_path, output_dir, text_file=True):
    """Plots wall and towall vs num_pmts

    Args:
        input_path (str): Path to either .hy file or text file with multiple paths and names of .hy files
        output_dir (str): Path to directory where plots should be saved to.
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
    """
    file_paths=input_path
    #Behaviour different depending on format of input (single or multiple files)
    if text_file:
        print(f'Getting files from: {str(input_path)}')
        text_file = open(input_path, "r")
        file_paths = text_file.readlines()
        num_files = len(file_paths)

    #Initialize lists of variables
    num_pmt = []
    label = []
    wall = []
    towall = []

    #Loop through all .hy files
    file_paths = file_paths if text_file else [file_paths]
    for j, path in enumerate(file_paths):
        path = path.strip('\n')
        print(f'New path: {path}')
        options_exists = os.path.isfile(path+'/'+'wc_options.pkl')
        if options_exists:
            print(f'Loading options from: {path}wc_options.pkl')
            wcsim_options = wcsim_options.load_options(path, 'wc_options.pkl')
            print(f'Particle: {wcsim_options.particle}')
        
        #with h5py.File(path+'/combine_combine.hy',mode='r') as h5fw:
        with h5py.File(path+'/digi_combine.hy',mode='r') as h5fw:
            temp_num_pmt = []
            temp_wall = []
            temp_towall = []
            temp_truth_labels = [] 

            #Get label from options, if not, take median of labels in file
            if options_exists:
                temp_label = wcsim_options.particle[0]
                if "e" in temp_label:
                    temp_label = "Electrons"
                if "m" in temp_label:
                    temp_label = "Muons"
            else:
                temp_label = convert_label(np.median(h5fw['labels']))
            
            max = h5fw['event_hits_index'].shape[0]


            #temp_primary_charged_range = np.ravel(np.sqrt( np.add( np.add( np.square( np.subtract(h5fw['primary_charged_start'][:,:,0], h5fw['primary_charged_end'][:,:,0])), np.square( np.subtract(h5fw['primary_charged_start'][:,:,1], h5fw['primary_charged_end'][:,:,1]))), np.square( np.subtract(h5fw['primary_charged_start'][:,:,2], h5fw['primary_charged_end'][:,:,2])))))
            temp_truth_labels = np.ravel(h5fw['labels'])
            print(temp_truth_labels)
            wall_vars = list(map(calculate_wcsim_wall_variables,np.array(h5fw['positions']), np.array(h5fw['directions'])))
            wall_vars = list(zip(*wall_vars))
            temp_wall = wall_vars[0]
            temp_towall = wall_vars[1]
            #TODO:Check that this works
            temp_num_pmt = np.subtract(np.ravel(h5fw['event_hits_index']), np.insert(np.delete(np.ravel(h5fw['event_hits_index']), -1),0,0))

        wall.append(temp_wall)
        towall.append(temp_towall)
        num_pmt.append(temp_num_pmt)

    # create two figrues
    fig1 = plt.figure()
    ax1 = fig1.gca()

    fig2 = plt.figure()
    ax2 = fig2.gca()

    # make scatter plot of wall and towall vs num_pmts for electrons and muons
    for wall_i, towall_i, num_pmt_i, label_i in zip(wall, towall, num_pmt, label):
        str_label = convert_label(np.median(label_i))
        ax1.scatter(wall_i, num_pmt_i, alpha=0.2, label=str_label, s=2)
        ax2.scatter(towall_i, num_pmt, alpha=0.2, label=label, s=2)

    # add labels and stuff to make plots more understandable
    ax1.vlines(200, ymin=0, ymax=max(num_pmt[0]), linestyles='--', label='2 m')
    ax1.set_xlabel('Wall [cm]')
    ax1.set_ylabel('Number of PMTs')
    ax1.legend()

    ax2.vlines(200, ymin=0, ymax=max(num_pmt[0]), linestyles='--', label='2 m')
    ax2.set_xlabel('Towall [cm]')
    ax2.set_ylabel('Number of PMTs')
    ax2.legend()
        
    # save
    fig2.savefig(output_dir+'towall_v_pmts.png')
    fig1.savefig(output_dir+'wall_v_pmts.png')

# run the function
plot_walls(input_path='plotting_paths.txt', output_dir='/fast_scratch_2/aferreira/t2k/ml/analysis_plots/')