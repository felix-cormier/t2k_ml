import h5py
import numpy as np
import glob
import os
import math
from generics_python.make_plots import generic_histogram, generic_2D_plot
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

module_path = '~/clean_git/t2k_ml/'

# import these from plot_wcsim
def get_cherenkov_threshold(label):
    threshold_dict = {0: 160., 1:0.8, 2: 0.}
    return threshold_dict[label]

def sample_lowest_min_energy(input_path, output_path, text_file=False, moreVariables = False):
    """
    Args:
        input_path (_type_): Path to either .hy file or text file with multiple paths and names of .hy files
        output_path (_type_): Where to save plots
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
        moreVariables (bool, optional): Add some variables - they are calculated from PMT vars and take a long time!
    """
    file_paths=input_path
    #Behaviour different depending on format of input (single or multiple files)
    if text_file:
        print(f'Getting files from: {str(input_path)}')
        text_file = open(input_path, "r")
        file_paths = text_file.readlines()

    #Initialize lists of variables
    mean_charge = []
    total_charge = []
    mean_time = []
    mean_x = []
    mean_y = []
    mean_z = []
    weighted_mean_x = []
    weighted_mean_y = []
    weighted_mean_z = []
    std_x = []
    std_y = []
    std_z = []
    num_pmt = []
    label = []
    wall = []
    towall = []
    
    decayE_exists = []
    decayE_energy = []
    decayE_time = []

    direction_x = []
    direction_y = []
    direction_z = []
    position_x = []
    position_y = []
    position_z = []

    all_charge = []
    all_time = []

    primary_charged_range = []


    truth_energy = []
    truth_energy_electron = [] 
    truth_energy_positron = [] 
    epos_energy_difference = []
    epos_energy_sum = []
    truth_visible_energy = []
    truth_veto = []
    truth_labels = []
    eposTotalEDiff = []

    #Loop through all .hy files
    file_paths = file_paths if text_file else [file_paths]
    for j, path in enumerate(file_paths):
        path = path.strip('\n')
        print(f'New path: {path}')
    
        with h5py.File(path+'/digi_combine.hy',mode='r') as h5fw:
            temp_truth_visible_energy = [] 

            '''
            #Temporary list of variables for each event
            temp_mean_charge = []
            temp_total_charge = []
            temp_mean_time = []
            temp_mean_x = []
            temp_mean_y = []
            temp_mean_z = []
            temp_weighted_mean_x = []
            temp_weighted_mean_y = []
            temp_weighted_mean_z = []
            temp_std_x = []
            temp_std_y = []
            temp_std_z = []
            temp_num_pmt = []
            temp_wall = []
            temp_towall = []

            temp_decayE_exists = []
            temp_decayE_energy = []
            temp_decayE_time = []
            
            temp_direction_x = []
            temp_direction_y = []
            temp_direction_z = []
            temp_position_x = []
            temp_position_y = []
            temp_position_z = []

            temp_truth_energy = [] 
            temp_truth_energy_electron = [] 
            temp_truth_energy_positron = [] 
            temp_epos_energy_difference = []
            temp_epos_energy_sum = []
            temp_truth_veto = [] 
            temp_truth_labels = [] 
            temp_primary_charged_range = []

            temp_all_charge = []
            temp_all_time = []

            temp_eposTotalEDiff = []

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
            temp_primary_charged_range = np.ravel(h5fw['primary_charged_range'])
            temp_truth_energy = np.ravel(h5fw['energies'])
            temp_truth_energy_positron = np.ravel(h5fw['energies_positron'])
            temp_truth_energy_electron = np.ravel(h5fw['energies_electron'])
            temp_epos_energy_difference = np.divide(np.subtract(temp_truth_energy_electron, temp_truth_energy_positron), temp_truth_energy)
            temp_epos_energy_sum = np.add(temp_truth_energy_electron, temp_truth_energy_positron)
            temp_eposTotalEDiff = np.divide(np.add(temp_truth_energy_electron, temp_truth_energy_positron), temp_truth_energy)
            temp_truth_labels = np.ravel(h5fw['labels'])
            print(temp_truth_labels)
            wall_vars = list(map(calculate_wcsim_wall_variables,np.array(h5fw['positions']), np.array(h5fw['directions'])))
            wall_vars = list(zip(*wall_vars))
            temp_wall = wall_vars[0]
            temp_towall = wall_vars[1]
            
            '''
            cheThr = list(map(get_cherenkov_threshold, np.ravel(h5fw['labels']))) # need to find this var/func

            temp_truth_visible_energy = np.ravel(h5fw['energies']) - cheThr
            #temp_truth_veto = (np.ravel(h5fw['veto']))

            '''
            temp_decayE_exists = (np.ravel(h5fw['decay_electron_exists']))
            print(np.unique(temp_decayE_exists, return_counts=True))
            temp_decayE_energy = (np.ravel(h5fw['decay_electron_energy'])[temp_decayE_exists==1])
            temp_decayE_time = (np.ravel(h5fw['decay_electron_time'])[temp_decayE_exists==1])
            print(temp_decayE_time)
            '''

            '''
            temp_direction_x = (np.ravel(h5fw['directions'][:,:,0]))
            temp_direction_y = (np.ravel(h5fw['directions'][:,:,1]))
            temp_direction_z = (np.ravel(h5fw['directions'][:,:,2]))
            temp_position_x = (np.ravel(h5fw['positions'][:,:,0]))
            temp_position_y = (np.ravel(h5fw['positions'][:,:,1]))
            temp_position_z = (np.ravel(h5fw['positions'][:,:,2]))

            temp_all_charge = np.ravel(h5fw['hit_charge'])
            temp_all_time = np.ravel(h5fw['hit_time'])

            #TODO:Check that this works
            temp_num_pmt = np.subtract(np.ravel(h5fw['event_hits_index']), np.insert(np.delete(np.ravel(h5fw['event_hits_index']), -1),0,0))

            #Loop through all events in file
            for i,index in enumerate(h5fw['event_hits_index']):
                if i>=(len(h5fw['event_hits_index'])-1):
                    break
                if h5fw['event_hits_index'][i]==h5fw['event_hits_index'][i+1]:
                    continue
                if i < max-1:

                    if ( abs(float(h5fw['positions'][i][:,2])) >  1000 or math.sqrt(float(h5fw['positions'][i][:,0])**2 + float(h5fw['positions'][i][:,1])**2) > 1000):
                        continue

                    #temp_truth_energy.append(float(h5fw['energies'][i]))

                    #temp_truth_labels.append(float(h5fw['labels'][i]))
                    if ((abs(float(h5fw['positions'][i][:,0])) + abs(float(h5fw['positions'][i][:,1]))+ abs(float(h5fw['positions'][i][:,2]))) < 1.0):
                        print(float(h5fw['positions'][i][:,0]))                                        

                    if not moreVariables:
                        continue

                    temp_mean_charge.append(np.mean(h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                    temp_total_charge.append(np.sum(h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                    temp_mean_time.append(np.mean(h5fw['hit_time'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
        '''
        '''
        mean_charge.append(temp_mean_charge)
        total_charge.append(temp_total_charge)
        wall.append(temp_wall)
        towall.append(temp_towall)
        mean_time.append(temp_mean_time)
        mean_x.append(temp_mean_x)
        mean_y.append(temp_mean_y)
        mean_z.append(temp_mean_z)
        weighted_mean_x.append(temp_weighted_mean_x)
        weighted_mean_y.append(temp_weighted_mean_y)
        weighted_mean_z.append(temp_weighted_mean_z)
        std_x.append(temp_std_x)
        std_y.append(temp_std_y)
        std_z.append(temp_std_z)
        num_pmt.append(temp_num_pmt)
        truth_energy.append(temp_truth_energy)
        truth_energy_electron.append(temp_truth_energy_electron)
        truth_energy_positron.append(temp_truth_energy_positron)
        epos_energy_difference.append(temp_epos_energy_difference)
        epos_energy_sum.append(temp_epos_energy_sum)
        '''
        truth_visible_energy.append(temp_truth_visible_energy)
         
        '''
        truth_veto.append(temp_truth_veto)
        truth_labels.append(temp_truth_labels)
        label.append(temp_label)

        decayE_exists.append(temp_decayE_exists)
        decayE_energy.append(temp_decayE_energy)
        decayE_time.append(temp_decayE_time)

        eposTotalEDiff.append(temp_eposTotalEDiff)

        primary_charged_range.append(temp_primary_charged_range)

        direction_x.append(temp_direction_x)
        direction_y.append(temp_direction_y)
        direction_z.append(temp_direction_z)
        position_x.append(temp_position_x)
        position_y.append(temp_position_y)
        position_z.append(temp_position_z)

        all_charge.append(temp_all_charge)
        all_time.append(temp_all_time)
        '''


    # examine truth_visible_energy to find smallest bin
    plt.hist(truth_visible_energy, bins=50)
    plt.show()

    '''
    #Plot all
    yname="Num. Events"
    generic_histogram(wall, 'Wall [cm]', output_path, 'wall', range=[0,2000], y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(towall, 'Towall [cm]', output_path, 'towall', range = [0,5000], y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(truth_energy, 'Truth Energy [MeV]', output_path, 'truth_energy', y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(truth_visible_energy, 'Truth Visible Energy [MeV]', output_path, 'truth_visible_energy', range=[50,1000], y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(truth_veto, 'Truth veto', output_path, 'truth_veto', y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(truth_labels, 'Truth label', output_path, 'truth_label', y_name = yname, label=label, bins=20)#, doNorm=True)

    generic_histogram(direction_x, 'Truth Direction X', output_path, 'truth_direction_x', y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(direction_y, 'Truth Direction Y', output_path, 'truth_direction_y', y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(direction_z, 'Truth Direction Z', output_path, 'truth_direction_z', y_name = yname, label=label, bins=20)#, doNorm=True)

    generic_histogram(position_x, 'Truth position X [cm]', output_path, 'truth_position_x', y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(position_y, 'Truth position Y [cm]', output_path, 'truth_position_y', y_name = yname, label=label, bins=20)#, doNorm=True)
    generic_histogram(position_z, 'Truth position Z [cm]', output_path, 'truth_position_z', y_name = yname, label=label, bins=20)#, doNorm=True)

    generic_histogram(all_charge, 'PMT Charge', output_path, 'all_pmt_charge', y_name = yname, range=[0,10], label=label, bins=100)#, doNorm=True)
    generic_histogram(all_time, 'PMT Time [ns]', output_path, 'all_pmt_time', y_name = yname, range=[500,1500], label=label, bins=100)#, doNorm=True)

    generic_histogram(num_pmt, 'Number of PMTs', output_path, 'num_pmt', y_name = yname, label=label, range=[0,4000])#, bins=20)

    if not moreVariables:
        return 0

    generic_histogram(mean_time, 'Mean Time', output_path, 'mean_time', y_name = yname, label=label, bins=20)
    generic_histogram(mean_charge, 'Mean Charge', output_path, 'mean_charge', y_name = yname, label=label, bins=20)
    generic_histogram(total_charge, 'Total Charge', output_path, 'total_charge', y_name = yname, label=label, bins=20)
    generic_histogram(mean_x, 'Mean PMT X [cm]', output_path, 'mean_x', y_name = yname, label=label, bins=20)
    generic_histogram(mean_y, 'Mean PMT Y [cm]', output_path, 'mean_y', y_name = yname, label=label, bins=20)
    generic_histogram(mean_z, 'Mean PMT Z [cm]', output_path, 'mean_z', y_name = yname, label=label, bins=20)
    generic_histogram(weighted_mean_x, 'Weighted Mean PMT X [cm]', output_path, 'weighted_mean_x', y_name = yname, label=label, bins=20)
    generic_histogram(weighted_mean_y, 'Weighted Mean PMT Y [cm]', output_path, 'weighted_mean_y', y_name = yname, label=label, bins=20)
    generic_histogram(weighted_mean_z, 'Weighted Mean PMT Z [cm]', output_path, 'weighted_mean_z', y_name = yname, label=label, bins=20)
    generic_histogram(std_x, 'std dev PMT X [cm]', output_path, 'std_x', y_name = yname, label=label, bins=20)
    generic_histogram(std_y, 'std dev PMT Y [cm]', output_path, 'std_y', y_name = yname, label=label, bins=20)
    generic_histogram(std_z, 'std dev PMT Z [cm]', output_path, 'std_z', y_name = yname, label=label, bins=20)
    '''


sample_lowest_min_energy(input_path=module_path+'plotting.txt', text_file=True)