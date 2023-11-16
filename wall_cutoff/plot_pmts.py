import h5py
import numpy as np
import os
import sys
sys.path.insert(0, '..')
from plot_wcsim import calculate_wcsim_wall_variables, convert_label
import matplotlib.pyplot as plt

def plot_vs_walls(input_path, output_dir=None, text_file=True, save_plots=False):
    """Plots wall and towall vs num_pmts. Best to use in notebook wall_cutoff_exploration.ipynbd2   
       More of a one-time use thing so it hasn't been thoroughly tested.

    Args:
        input_path (str): Path to either .hy file or text file with multiple paths and names of .hy files
        output_dir (str, optional): Path to directory where plots should be saved to. Defaults to None.
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
        save_plots (bool, optional): If plots should be saved. Defaults to False.

    Returns:
          XXXXXXXXXXX  WCSimOptions class object: Loaded class

    """

    file_paths=input_path

    #Initialize lists of variables
    num_pmt = []
    label = []
    wall = []
    towall = []

    #Behaviour different depending on format of input (single or multiple files)
    if text_file:
        print(f'Getting files from: {str(input_path)}')
        text_file = open(input_path, "r")
        file_paths = text_file.readlines()
        num_files = len(file_paths)

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
                temp_label = convert_label(np.median(h5fw['labels']))
                wall_vars = list(map(calculate_wcsim_wall_variables,np.array(h5fw['positions']), np.array(h5fw['directions'])))
                wall_vars = list(zip(*wall_vars))
                temp_wall = wall_vars[0]
                temp_towall = wall_vars[1]
                #FIXED CALC
                temp_num_pmt = np.subtract(np.ravel(h5fw['event_hits_index']), np.insert(np.delete(np.ravel(h5fw['event_hits_index']), -1),0,0))
                temp_num_pmt = np.roll(temp_num_pmt,shift=-1) 

            wall.append(temp_wall)
            towall.append(temp_towall)
            num_pmt.append(temp_num_pmt)
            label.append(temp_label)

    else:
        print(f'Getting data from: {str(input_path)}')
        path = input_path
        options_exists = os.path.isfile(path+'/'+'wc_options.pkl')
        if options_exists:
            print(f'Loading options from: {path}wc_options.pkl')
            wcsim_options = wcsim_options.load_options(path, 'wc_options.pkl')
            print(f'Particle: {wcsim_options.particle}')
        
        with h5py.File(path,mode='r') as h5fw:
            label = convert_label(np.median(h5fw['labels']))
            wall_vars = list(map(calculate_wcsim_wall_variables,np.array(h5fw['positions']), np.array(h5fw['directions'])))
            wall_vars = list(zip(*wall_vars))
            wall = wall_vars[0]
            towall = wall_vars[1]
            #FIXED CALC
            num_pmt = np.subtract(np.ravel(h5fw['event_hits_index']), np.insert(np.delete(np.ravel(h5fw['event_hits_index']), -1),0,0))
            num_pmt = np.roll(num_pmt,shift=-1) 

    if save_plots == True:
        if output_dir == None:
            output_dir_lst = input_path.split('/')
            output_dir_lst.pop()
            output_dir = "".join(output_dir_lst)

        # create two figrues
        fig1 = plt.figure()
        ax1 = fig1.gca()

        fig2 = plt.figure()
        ax2 = fig2.gca()

        # make scatter plot of wall and towall vs num_pmts for electrons and muons
        ax1.scatter(wall, num_pmt, alpha=0.1, s=0.01, label=label)
        ax2.scatter(towall, num_pmt, alpha=0.1, s=0.01, label=label)

        # make the 2m cutoff line go up to 4000
        y_max = 4000
        nominal_cutoff = 100

        # add labels and stuff to make plots more understandable
        ax1.vlines(nominal_cutoff, ymin=0, ymax=y_max, linestyles='--', label=f'{nominal_cutoff/100} m', color='blue', alpha=0.5)
        ax1.set_xlabel('Wall [cm]')
        ax1.set_ylabel('Number of PMTs')
        ax1.legend(loc='upper right')

        ax2.vlines(nominal_cutoff, ymin=0, ymax=y_max, linestyles='--', label=f'{nominal_cutoff/100} m', color='blue', alpha=0.5)
        ax2.set_xlabel('Towall [cm]')
        ax2.set_ylabel('Number of PMTs')
        ax2.legend(loc='upper right')
        ax2.set_xlim(-80,6000) # some anomolous points way too far out exist

        # save plots
        fig2.savefig(output_dir+'towall_v_pmts.png')
        fig1.savefig(output_dir+'wall_v_pmts.png')

    return wall, towall, num_pmt, label


# what is the diff with this below????????????????????????????????????
def plot_indiv_event(input_path, output_dir, text_file=True):
    """

    Args:
        input_path (str): Path to either .hy file or text file with multiple paths and names of .hy files
        output_dir (str): Path to directory where plots should be saved to.
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
    """
    file_paths=input_path

    #Initialize lists of variables
    num_pmt = []
    label = []
    wall = []
    towall = []

    #Behaviour different depending on format of input (single or multiple files)
    if text_file:
        print(f'Getting files from: {str(input_path)}')
        text_file = open(input_path, "r")
        file_paths = text_file.readlines()
        num_files = len(file_paths)

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
                wall_vars = list(map(calculate_wcsim_wall_variables,np.array(h5fw['positions']), np.array(h5fw['directions']))) # need to check it goes here and saves with different names
                wall_vars = list(zip(*wall_vars))
                temp_wall = wall_vars[0]
                temp_towall = wall_vars[1]
                #TODO:Check that this works
                temp_num_pmt = np.subtract(np.ravel(h5fw['event_hits_index']), np.insert(np.delete(np.ravel(h5fw['event_hits_index']), -1),0,0))

            wall.append(temp_wall)
            towall.append(temp_towall)
            num_pmt.append(temp_num_pmt)
            label.append(temp_label)

    else:
        print(f'Getting data from: {str(input_path)}')
        path = input_path
        options_exists = os.path.isfile(path+'/'+'wc_options.pkl')
        if options_exists:
            print(f'Loading options from: {path}wc_options.pkl')
            wcsim_options = wcsim_options.load_options(path, 'wc_options.pkl')
            print(f'Particle: {wcsim_options.particle}')
        
        with h5py.File(path,mode='r') as h5fw:
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
            
            #temp_primary_charged_range = np.ravel(np.sqrt( np.add( np.add( np.square( np.subtract(h5fw['primary_charged_start'][:,:,0], h5fw['primary_charged_end'][:,:,0])), np.square( np.subtract(h5fw['primary_charged_start'][:,:,1], h5fw['primary_charged_end'][:,:,1]))), np.square( np.subtract(h5fw['primary_charged_start'][:,:,2], h5fw['primary_charged_end'][:,:,2])))))
            truth_labels = np.ravel(h5fw['labels'])
            print(truth_labels)
            wall_vars = list(map(calculate_wcsim_wall_variables,np.array(h5fw['positions']), np.array(h5fw['directions'])))
            wall_vars = list(zip(*wall_vars))
            wall = wall_vars[0]
            towall = wall_vars[1]
            #TODO:Check that this works
            num_pmt = np.subtract(np.ravel(h5fw['event_hits_index']), np.insert(np.delete(np.ravel(h5fw['event_hits_index']), -1),0,0))

    return wall, towall, num_pmt, label