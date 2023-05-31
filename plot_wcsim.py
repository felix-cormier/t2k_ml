import h5py
import numpy as np
import glob
import os
import math
from operator import truediv
import matplotlib.pyplot as plt
import statistics

from generics_python.make_plots import generic_histogram
from generics_python.make_plots import generic_histogram2
from generics_python.make_plots import generic_histogram_ratio
from generics_python.make_plots import generic_histogram_d
from generics_python.make_plots import square
from generics_python.make_plots import sqrt
from generics_python.make_plots import sub


def calculate_wcsim_wall_variables(position, direction):
    """Generates wall and towall variables for input position and direction

    Args:
        position (_type_): three-coordinate position
        direction (_type_): three-coordinate direction

    Returns:
        float, float: wall, towall variables
    """

    #Calculate wall variables
    position = position[0]
    #position_gev = gamma_end_vtx[0]
    direction = direction[0]
    min_vertical_wall = 1810-abs(position[2])
    #min_vertical_wall_gev = 1810-abs(gamma_end_vtx[2])
    min_horizontal_wall = 1690 - math.sqrt(position[0]*position[0] + position[1]*position[1])
    #min_horiziontal_wall_gev = 1690 - math.sqrt(gamma_end_vtx[0]*gamma_end_vtx[0] + gamma_end_vtx[1]*gamma_end_vtx[1])
    wall = min(min_vertical_wall,min_horizontal_wall)
    #wall_gev = min(min_vertical_wall_gev, min_horiziontal_wall_gev)

    #Calculate towall
    point_1 = [position[0], position[1]]
    point_2 = [position[0] + direction[0],position[1] + direction[1]]
    coefficients = np.polyfit([point_1[0], point_2[0]],[point_1[1], point_2[1]],1)
    for_quadratic = [1+coefficients[0]*coefficients[0],2*coefficients[0]*coefficients[1],coefficients[1]*coefficients[1]-(1690*1690)]
    quad_sols_x = np.roots(for_quadratic)
    quad_sols_y = [coefficients[0]*quad_sols_x[0] + coefficients[1], coefficients[0]*quad_sols_x[1] + coefficients[1] ]
    small_index = np.argmin([quad_sols_x[0], quad_sols_x[1]])
    large_index = np.argmax([quad_sols_x[0], quad_sols_x[1]])
    if direction[0] > 0:
        right_index = large_index
    else:
        right_index = small_index

    time_to_horizontal = abs(position[0] - quad_sols_x[right_index])/direction[0]
    vertical_towall_distance = np.min([abs(position[2]-1810),abs(position[2]+1810)])
    time_to_vertical = abs(vertical_towall_distance/direction[2])

    if time_to_horizontal < time_to_vertical:
        new_z = position[2] + time_to_horizontal*direction[2]
        try:
            towall =  math.sqrt( (position[0] - quad_sols_x[right_index])**2 + (position[1] - quad_sols_y[right_index])**2 + (position[2]-new_z)**2) 
        except ValueError:
            print(f'towall had a math domain error')
            new_x = position[0] + time_to_vertical*direction[0]
            new_y = position[1] + time_to_vertical*direction[1]
            towall = math.sqrt( (position[0] - new_x)**2 + (position[1] - new_y)**2 + vertical_towall_distance**2 )

    else:
        new_x = position[0] + time_to_vertical*direction[0]
        new_y = position[1] + time_to_vertical*direction[1]
        towall = math.sqrt( (position[0] - new_x)**2 + (position[1] - new_y)**2 + vertical_towall_distance**2 )


    return wall, towall#, wall_gev
    
    #dist_pt_1 = math.sqrt()
    '''
    delta_x = point_2[0] - point_1[0]
    delta_y = point_2[1] - point_1[1]

    if delta_x == 0:
        pass
    '''

def load_geofile(geofile_name):

    with np.load(geofile_name) as data:
        return data['position']

def convert_values(geofile,input):
    return [geofile[x] for x in input]


def convert_label(label):
    if label == 2:
        return 'Gamma'
    if label == 1:
        return 'Electron'
    if label == 0:
        return 'Muon'
    else:
        return label

def get_cherenkov_threshold(label):
    threshold_dict = {0: 160., 1:0.8, 2: 0.}
    return threshold_dict[label]

def plot_wcsim(input_path, output_path, wcsim_options, text_file=False, truthOnly = True):
    """Plots PMT and event variables

    Args:
        input_path (_type_): Path to either .hy file or text file with multiple paths and names of .hy files
        output_path (_type_): Where to save plots
        wcsim_options (_type_): options class
        text_file (bool, optional): If the input is in text file or string to single .hy file. Defaults to False.
    """

    num_files=1
    geofile = load_geofile('geofile.npz')
    file_paths=input_path
    #Behaviour different depending on format of input (single or multiple files)
    if text_file:
        print(f'Getting files from: {str(input_path)}')
        text_file = open(input_path, "r")
        file_paths = text_file.readlines()
        num_files = len(file_paths)

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
    wall_gev = []
    towall_gev = []

    direction_x = []
    direction_y = []
    direction_z = []
    direction_r = []

    position_x = []
    position_y = []
    position_z = []
    position_r = []

    gamma_end_vtx_x = []
    gamma_end_vtx_y = []
    gamma_end_vtx_z = []
    gamma_end_vtx_r = []

    decay_distance = []

    truth_energy = []
    truth_visible_energy = []
    truth_veto = []
    truth_labels = []

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
        with h5py.File(path+'/digi_combine_50k.hy',mode='r') as h5fw:

            #Temporary list of variables for each event
            temp_mean_charge = []
            temp_total_charge = []
            temp_mean_time = []
            temp_mean_x = []
            temp_mean_y = []
            temp_mean_z = []
            temp_mean_r = []
            temp_weighted_mean_x = []
            temp_weighted_mean_y = []
            temp_weighted_mean_z = []
            temp_weighted_mean_r = []
            temp_std_x = []
            temp_std_y = []
            temp_std_z = []
            temp_std_r = []
            temp_num_pmt = []
            temp_wall = []
            temp_towall = []
            temp_wall_gev = []
            temp_towall_gev = []

            temp_direction_x = []
            temp_direction_y = []
            temp_direction_z = []
            temp_direction_r = []
            temp_position_x = []
            temp_position_y = []
            temp_position_z = []
            temp_position_r = []
            

            temp_gamma_end_vtx_x = []
            temp_gamma_end_vtx_y = []
            temp_gamma_end_vtx_z = []
            temp_gamma_end_vtx_r = []

            temp_decay_distance = []
            
            temp_truth_energy = [] 
            temp_truth_visible_energy = [] 
            temp_truth_veto = [] 
            temp_truth_labels = [] 

            #Get label from options, if not, take median of labels in file
            if options_exists:
                temp_label = wcsim_options.particle[0]
                print('options exist', options_exists)
                print('temp label = ', temp_label)
            else:
                print('options dont exist')
                temp_label = convert_label(np.median(h5fw['labels']))
                print('temp label = ', temp_label)

            max = h5fw['event_hits_index'].shape[0]
            #Loop through all events in file
            for i,index in enumerate(h5fw['event_hits_index']):
                #Stop at 5000 events, to make it go faster
                if i > 5000:
                    continue
                if i>=(len(h5fw['event_hits_index'])-1):
                    break
                if h5fw['event_hits_index'][i]==h5fw['event_hits_index'][i+1]:
                    continue
                if i < max-1:
                    wall_out, towall_out = calculate_wcsim_wall_variables(h5fw['gamma_start_vtx'][i], h5fw['directions'][i])
                    wall_out_gev, towall_out_gev= calculate_wcsim_wall_variables(h5fw['positions'][i], h5fw['directions'][i])

                    if ((abs(float(h5fw['positions'][i][:,0])) + abs(float(h5fw['positions'][i][:,1]))+ abs(float(h5fw['positions'][i][:,2]))) < 1.0):
                        continue
                    if 'g' in temp_label and ((abs(float(h5fw['gamma_start_vtx'][i][:,0])) + abs(float(h5fw['gamma_start_vtx'][i][:,1])) + abs(float(h5fw['gamma_start_vtx'][i][:,2]))) < 1.0):
                        continue
                    #print('wall_out', wall_out)
                    temp_wall.append(wall_out)
                    temp_towall.append(towall_out)
                    temp_wall_gev.append(wall_out_gev)
                    temp_towall_gev.append(towall_out_gev)
                    temp_truth_energy.append(float(h5fw['energies'][i]))

                    temp_truth_visible_energy.append(float(h5fw['energies'][i])-get_cherenkov_threshold(h5fw['labels'][i]))
                    temp_truth_labels.append(float(h5fw['labels'][i]))
                    temp_truth_veto.append(float(h5fw['veto'][i]))


                    temp_direction_x.append(float(h5fw['directions'][i][:,0]))
                    temp_direction_y.append(float(h5fw['directions'][i][:,1]))
                    temp_direction_z.append(float(h5fw['directions'][i][:,2]))


                    temp_position_x.append(float(h5fw['gamma_start_vtx'][i][:,0]))
                    temp_position_y.append(float(h5fw['gamma_start_vtx'][i][:,1]))
                    temp_position_z.append(float(h5fw['gamma_start_vtx'][i][:,2]))
                    


                    temp_gamma_end_vtx_x.append(float(h5fw['positions'][i][:,0]))
                    temp_gamma_end_vtx_y.append(float(h5fw['positions'][i][:,1]))
                    temp_gamma_end_vtx_z.append(float(h5fw['positions'][i][:,2]))
                    if ((abs(float(h5fw['gamma_start_vtx'][i][:,0])) + abs(float(h5fw['gamma_start_vtx'][i][:,1]))+ abs(float(h5fw['gamma_start_vtx'][i][:,2]))) < 1.0):
                        pass
                        #print(float(h5fw['positions'][i][:,0]))
                    

                    if ((abs(float(h5fw['positions'][i][:,0])) + abs(float(h5fw['positions'][i][:,1])) + abs(float(h5fw['positions'][i][:,2]))) < 1.0):
                        pass
                        #print(float(h5fw['gamma_end_vtx'][i][:,0]))

                    temp_num_pmt.append(h5fw['event_hits_index'][i+1] - h5fw['event_hits_index'][i])

                    if truthOnly:
                        continue

                    pmt_positions = np.array(convert_values(geofile,h5fw['hit_pmt'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))

                    temp_mean_charge.append(np.mean(h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                    temp_total_charge.append(np.sum(h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                    temp_mean_time.append(np.mean(h5fw['hit_time'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                    temp_mean_x.append(np.mean(pmt_positions[:,0]))
                    temp_mean_y.append(np.mean(pmt_positions[:,1]))
                    temp_mean_z.append(np.mean(pmt_positions[:,2]))
                    if np.sum(h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]) > 0:
                        temp_weighted_mean_x.append(np.average(pmt_positions[:,0],weights=h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                        temp_weighted_mean_y.append(np.average(pmt_positions[:,1],weights=h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                        temp_weighted_mean_z.append(np.average(pmt_positions[:,2],weights=h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]]))
                    temp_std_x.append(np.std(pmt_positions[:,0]))
                    temp_std_y.append(np.std(pmt_positions[:,1]))
                    temp_std_z.append(np.std(pmt_positions[:,2]))
                    '''
                    n_pmt = h5fw['event_hits_index'][i+1] - h5fw['event_hits_index'][i]
                    tot_charge = np.sum(h5fw['hit_charge'][h5fw['event_hits_index'][i]:h5fw['event_hits_index'][i+1]])
                    if n_pmt < 300 and tot_charge < 500: 
                        print(i)
                        print(f'num pmt: {n_pmt}, total charge: {tot_charge}')
                        event_label = float(h5fw['labels'][i])
                        print(f'label: {event_label}')
                    '''

            
        mean_charge.append(temp_mean_charge)
        total_charge.append(temp_total_charge)
        wall.append(temp_wall)
        #print('wall = ', wall)
        wall_gev.append(temp_wall_gev)
        towall.append(temp_towall)
        towall_gev.append(temp_towall_gev)
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
        truth_visible_energy.append(temp_truth_visible_energy)
        truth_veto.append(temp_truth_veto)
        truth_labels.append(temp_truth_labels)
        label.append(temp_label)
        #print('label = ', truth_labels)

        #mean_r.append(sqrt(square(mean_x) + square(mean_y)))

        temp_direction_x = np.array(temp_direction_x)
        temp_direction_y = np.array(temp_direction_y)
        #temp_direction_z = np.array(temp_direction_z)
        temp_position_x = np.array(temp_position_x)
        temp_position_y = np.array(temp_position_y)
        temp_position_z = np.array(temp_position_z)
        temp_gamma_end_vtx_x = np.array(temp_gamma_end_vtx_x)
        temp_gamma_end_vtx_y = np.array(temp_gamma_end_vtx_y)
        temp_gamma_end_vtx_z = np.array(temp_gamma_end_vtx_z)
        #print('temp position y', len(temp_position_y))
        temp_direction_r = np.sqrt(np.square(temp_direction_x) + np.square(temp_direction_y))
        #print('temp direction r', len(temp_direction_r))
        direction_x.append(temp_direction_x)
        direction_y.append(temp_direction_y)
        direction_z.append(temp_direction_z)
        #direction_r.append(sqrt(square(temp_direction_x) + square(temp_direction_y)))
        direction_r.append(temp_direction_r)       
        temp_position_r = (np.sqrt(np.square(temp_position_x) + np.square(temp_position_y)))
        #print('temp position r', len(temp_position_r))
        position_x.append(temp_position_x)
        position_y.append(temp_position_y)
        position_z.append(temp_position_z)
        #position_r.append(sqrt(square(temp_position_x) + square(temp_position_y)))
        position_r.append(temp_position_r)
        print('gamma_end_vtx_xyz.append')
        temp_gamma_end_vtx_r = (np.sqrt(np.square(temp_gamma_end_vtx_x) + np.square(temp_gamma_end_vtx_y)))
        gamma_end_vtx_x.append(temp_gamma_end_vtx_x)
        #print('temp gamma end vtx r', len(temp_gamma_end_vtx_r))
        gamma_end_vtx_y.append(temp_gamma_end_vtx_y)
        gamma_end_vtx_z.append(temp_gamma_end_vtx_z)
        #gamma_end_vtx_r.append(sqrt(square(temp_gamma_end_vtx_x) + square(temp_gamma_end_vtx_y)))
        gamma_end_vtx_r.append(temp_gamma_end_vtx_r)
        #decay_distance.append(sub(gamma_end_vtx_r, position_r))
        decay_distance.append(np.sqrt(np.square((temp_gamma_end_vtx_x - temp_position_x)) + np.square(temp_gamma_end_vtx_y - temp_position_y) + np.square((temp_gamma_end_vtx_z - temp_position_z))))
    position_y = list(position_y)
    position_x = list(position_x)
    position_z = list(position_z)
    position_r = list(position_r)
    #print('electrons', position_x[1])
    #print('gammas', position_x[0])
    electron_prod_x = gamma_end_vtx_x[1]
    electron_prod_y = gamma_end_vtx_y[1]
    electron_prod_z = gamma_end_vtx_z[1]
    print(electron_prod_x)
    electron_prod_r = np.sqrt(np.square(electron_prod_x) + np.square(electron_prod_y))
    #print('electron_prod = ', electron_prod)
    #print('electron_prod dim = ', electron_prod.ndim)
    electron_prod_x = list(electron_prod_x)
    electron_prod_y = list(electron_prod_y)
    electron_prod_z = list(electron_prod_z)
    decay_distance = list(decay_distance)
    direction_y = list(direction_y)
    direction_x = list(direction_x)
    direction_z = list(direction_z)
    direction_r = list(direction_r)
    gamma_end_vtx_x = list(gamma_end_vtx_x)
    gamma_end_vtx_y = list(gamma_end_vtx_y)
    gamma_end_vtx_z = list(gamma_end_vtx_z)
    gamma_end_vtx_r = list(gamma_end_vtx_r)
    towall = list(towall)
    towall_gev = list(towall_gev)
        
    #Plot all
    decay_distance = np.array(decay_distance)
    decay_distance.flatten()
    decay_distance.reshape(-1)
    decay_distance = np.ravel(decay_distance)
    print('decay distance dimension:', decay_distance.ndim)
    #print('wall_gev[1]', wall_gev[1])
    yname="Num. Events"
    #np array everything needed
    #print('position_r = ',position_r)
    position_r = np.array(position_r[0])
    position_z = np.array(position_z[0])
    gamma_end_vtx_z = np.array(gamma_end_vtx_z[0])
    towall = np.array(towall[0])
    wall0 = np.array(wall[0])
    wall1 = np.array(wall_gev[1])
    wall_gev = np.array(wall_gev[0])
    gamma_end_vtx_r = np.array(gamma_end_vtx_r[0])
    truth_veto = np.array(truth_veto[0])
    towall_gev = np.array(towall_gev[0])
    electron_prod_r = np.array(electron_prod_r)
    #print(wall)
    #print(electron_prod.shape, electron_prod.ndim)
    #print(electron_prod)
    #print(wall_gev)
    #electron_prod = np.delete(electron_prod, -1)
    #apply cuts
    #print('wall = ', wall)
    #print('wall_gev = ', wall_gev)
    #print('types ', type(wall), type(position_r), type(100))
    position_r_distance = position_r[wall0 > 150]
    position_r_gev = gamma_end_vtx_r[wall_gev > 150]
    #wall_gev_cut = wall_gev[wall > 200 & veto < 1]
    #wall_cut = wall[wall > 200 & veto < 1]
    position_z_cut = position_z[wall0 > 150]
    position_z_gev_cut = gamma_end_vtx_z[wall_gev > 150]
    electron_prod_distance = electron_prod_r[wall1 > 150]
    #printa('wall1', wall1)

    #print('types ', type(wall), type(position_r), type(100))
    position_r_distance_100 = position_r[wall0 > 100]
    position_r_gev_100 = gamma_end_vtx_r[wall_gev > 100]
    #wall_gev_cut = wall_gev[wall > 200 & veto < 1]
    #wall_cut = wall[wall > 200 & veto < 1]
    position_z_cut_100 = position_z[wall0 > 100]
    position_z_gev_cut_100 = gamma_end_vtx_z[wall_gev > 100]
    electron_prod_distance_100 = electron_prod_r[wall1 > 100]



    #print('types ', type(wall), type(position_r), type(100))
    position_r_distance_50 = position_r[wall0 > 50]
    position_r_gev_50 = gamma_end_vtx_r[wall_gev > 50]
    #wall_gev_cut = wall_gev[wall > 200 & veto < 1]
    #wall_cut = wall[wall > 200 & veto < 1]
    position_z_cut_50 = position_z[wall0 > 50]
    position_z_gev_cut_50 = gamma_end_vtx_z[wall_gev > 50]
    electron_prod_distance_50 = electron_prod_r[wall1 > 50]

    
    wall2 = wall0[wall0 > 50]
    towall2 = towall_gev[wall0 > 50]
    wall3 = wall0[wall0 > 100]
    towall3 = towall_gev[wall0 > 100]
    wall4 = wall0[wall0 > 150]
    towall4 = towall_gev[wall0 > 150]


    #position_r_distance = position_r[truth_veto <1]
    #position_r_gev = gamma_end_vtx_r[truth_veto < 1]
    #wall_gev_cut = wall_gev[wall > 200 & veto < 1]
    #wall_cut = wall[wall > 200 & veto < 1]
    #position_z_cut = position_z[truth_veto < 1]
    #position_z_gev_cut = gamma_end_vtx_z[truth_veto < 1]

    #turn every nparray into a list to optimize histogram making
    towall = list(towall)
    towall_gev = list(towall_gev)
    position_r_distance = list(position_r_distance)
    position_r_distance_100 = list(position_r_distance_100)
    position_r_distance_50 = list(position_r_distance_50)
    position_r_gev_100 = list(position_r_gev_100)
    position_r_gev_50 = list(position_r_gev_50)
    position_r_gev = list(position_r_gev)
    position_r = list(position_r)
    gamma_end_vtx_r = list(gamma_end_vtx_r)
    gamma_end_vtx_z = list(gamma_end_vtx_z)
    wall = list(wall)
    wall_gev = list(wall_gev)
    position_z = list(position_z)
    position_z_cut_100 = list(position_z_cut_100)
    position_z_cut_50 = list(position_z_cut_50)
    position_z_cut = list(position_z_cut)
    position_z_gev_cut = list(position_z_gev_cut)
    position_z_gev_cut_100 = list(position_z_gev_cut_100)
    position_z_gev_cut_50 = list(position_z_gev_cut_50)
    print('length of wall:', len(wall))
    truth_veto = list(truth_veto)
    electron_prod_r = list(electron_prod_r)
    electron_prod_distance = list(electron_prod_distance)
    electron_prod_distance_100 = list(electron_prod_distance_100)
    electron_prod_distance_50 = list(electron_prod_distance_50)
    towall2 = list(towall2)
    towall3 = list(towall2)
    towall4 = list(towall4)
    wall2 = list(wall2)
    wall3 = list(wall3)
    wall4 = list(wall4)
   # generic_histogram(wall, 'Wall [cm]', output_path, 'wall', range=[0,2000], y_name = yname, label=label, bins=20)
   # generic_histogram(wall_gev, 'Wall [cm]', output_path, 'wall_gev', range=[0,2000], y_name = yname, label=label, bins=20)
   # generic_histogram(wall_gev, 'Wall [cm]', output_path, 'wall_gev smal', range=[0,100], y_name = yname, label=label, bins=20)
   # print('1')
   # generic_histogram(towall, 'Towall [cm]', output_path, 'towall', range = [0,5000], y_name = yname, label=label, bins=20)
   # print('2')
   # generic_histogram(towall, 'Towall [cm]', output_path, 'towall small', range = [0,100], y_name = yname, label=label, bins=20)
    #print('2.5')
    #generic_histogram(towall_gev, 'Towall [cm]', output_path, 'towall_gev', range = [0,2000], y_name = yname, label=label, bins=20)
    #generic_histogram(towall_gev, 'Towall [cm]', output_path, 'towall_gev small', range = [0,100], y_name = yname, label=label, bins=20)
    #generic_histogram(truth_energy, 'Truth Energy [MeV]', output_path, 'truth_energy', y_name = yname, label=label, bins=20)
    #print('3')
    #generic_histogram(truth_visible_energy, 'Truth Visible Energy [MeV]', output_path, 'truth_visible_energy', y_name = yname, label=label, bins=20)
    #print('4')
    #generic_histogram(truth_veto, 'Truth veto', output_path, 'truth_veto', y_name = yname, label=label, bins=20)
   # print('5')
   # generic_histogram(truth_labels, 'Truth label', output_path, 'truth_label', y_name = yname, label=label, bins=20)
   # print('6')
   # generic_histogram(direction_x, 'Truth Direction X', output_path, 'truth_direction_x', y_name = yname, label=label, bins=20)
   # print('7')
   # generic_histogram(direction_y, 'Truth Direction Y', output_path, 'truth_direction_y', y_name = yname, label=label, bins=20)
   # print('8')
   # generic_histogram(direction_z, 'Truth Direction Z', output_path, 'truth_direction_z', y_name = yname, label=label, bins=20)
   # print('9')
   # generic_histogram(direction_r, 'Truth Direction R', output_path, 'truth_direction_r', y_name = yname, label=label, bins=20)
   # print('10')
   # generic_histogram(position_x, 'Truth position X [cm]', output_path, 'truth_position_x', y_name = yname, label=label, bins=20)
    #print('11')
    #generic_histogram(position_y, 'Truth position Y [cm]', output_path, 'truth_position_y', y_name = yname, label=label, bins=20)
    #print('12')
    #generic_histogram(position_z, 'Truth position Z [cm]', output_path, 'truth_position_z', y_name = yname, label=label, bins=20)
    #print('13')
    #generic_histogram(position_r, 'Truth position R [cm]', output_path, 'truth_position_r', y_name = yname, label=label, bins=20)
    #print('14')
    
    #print(position_r_gev)
    #print('elect', electron_prod_distance)

    decay_distance = decay_distance[0]
    gamma_end_vtx_x = gamma_end_vtx_x[0]
    gamma_end_vtx_y = gamma_end_vtx_y[0]
    gamma_end_vtx_z = gamma_end_vtx_z[0]
    position_x = position_x[0]
    position_y = position_y[0]
    position_z = position_z[0]
    

    generic_histogram2(np.abs(position_r_gev), np.abs(position_r_distance), 'Truth position R [cm]', output_path, 'towall and dwall with 150 cut', y_name = yname, label=label, bins=20, range = (1400, 1750), label2 = 'gamma generation with 150 cut', label1 = 'gamma end vertex with cut')
    generic_histogram2(np.abs(position_r_gev_100), np.abs(position_r_distance_100), 'Truth position R [cm]', output_path, 'towall and dwall with 100 cut', y_name = yname, label=label, bins=20, range = (1400, 1750), label2 = 'gamma generation with 100 cut', label1 = 'gamma end vertex with 100 cut')
    generic_histogram2(np.abs(position_r_gev_50), np.abs(position_r_distance_50), 'Truth position R [cm]', output_path, 'towall and dwall with 50 cut', y_name = yname, label=label, bins=20, range = (1400, 1750), label2 = 'gamma generation with 50 cut', label1 = 'gamma end vertex with 50 cut')
    print('15')
    #generic_histogram_d(decay_distance, 'Truth decay distance [cm]', output_path, 'truth_decay_distance_r', y_name = yname, label = label, bins=40, range = (0, 400))
    print('16')
    generic_histogram2(np.abs(position_z_gev_cut), np.abs(position_z_cut), 'truth position z cut [cm]', output_path, 'position z 150 cut', y_name = yname, label=label, bins=20, range = (1400, 1750), label1 = 'gamma end vertex with 150 cut', label2 = 'electron generation with 150 cut')
    generic_histogram2(np.abs(position_z_gev_cut_50), np.abs(position_z_cut_50), 'Truth position Z cut [cm]', output_path, 'position z 50 cut', y_name = yname, label=label, bins=20, range = (1400, 1750), label1 = 'gamma end vertex with 50 cut', label2 = 'electron generation with 50 cut')
    generic_histogram2(np.abs(position_z_gev_cut_100), np.abs(position_z_cut_100), 'Truth position Z cut [cm]', output_path, 'position z 100 cut', y_name = yname, label=label, bins=20, range = (1400, 1750), label1 = 'gamma end vertex with 100 cut', label2 = 'electron generation with 100 cut')
    print('17')
    #generic_histogram2(wall_gev_cut, wall_cut, 'dwall [cm]', output_path, 'dwall cut', y_name = yname, label = label, bins=20, range = (0, 400), label1 = 'gamma end vertex d_wall with towall <100 cut', label2 = 'gamma generation d_wall with towall <100 cut')
    generic_histogram2(np.abs(electron_prod_distance), np.abs(position_r_gev), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx cut', y_name = yname, label=label, bins=20, range = (1400, 1800), label2 = 'gamma end vertex with 150 cut', label1 = '$e^{-}$ generation with 150 cut')
    generic_histogram2(np.abs(electron_prod_distance), np.abs(position_r_gev), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx cut', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'gamma end vertex with 150 cut', label1 = '$e^{-}$ generation with 150 cut')
    generic_histogram2(np.abs(electron_prod_r), np.abs(position_r), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx cut zoomed out', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'gamma end vertex no cut', label1 = '$e^{-}$ generation with 150 cut')
    generic_histogram2(np.abs(electron_prod_r), np.abs(position_r), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx no cut zoomed out', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'gamma end vertex with no cut', label1 = '$e^{-}$ generation with no cut')


    generic_histogram2(np.abs(electron_prod_distance_100), np.abs(position_r_gev_100), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx with 100 cut', y_name = yname, label=label, bins=20, range = (1400, 1800), label2 = 'gamma end vertex with 100 cut', label1 = '$e^{-}$ generation with 100 cut')
    generic_histogram2(np.abs(electron_prod_distance_100), np.abs(position_r_gev_100), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx with 100 cut zoomed out', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'gamma end vertex with 100 cut', label1 = '$e^{-}$ generation with 100 cut')
    generic_histogram2(np.abs(electron_prod_distance_50), np.abs(position_r_gev_50), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx 50 cut', y_name = yname, label=label, bins=20, range = (1400, 1800), label2 = 'gamma end vertex with 50 cut', label1 = '$e^{-}$ generation with 50 cut')
    generic_histogram2(np.abs(electron_prod_distance_50), np.abs(position_r_gev_50), 'Truth position R cut [cm]', output_path, 'electron gamma_end_vtx 50 cut zoomed out', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'gamma end vertex with 50 cut', label1 = '$e^{-}$ generation with 50 cut')

    
    
    
    generic_histogram2(np.abs(wall2), np.abs(towall2), 'Wall [cm]', output_path, 'wall towall 50 cut', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'towall 50 cut', label1 = 'wall 50 cut')
    generic_histogram2(np.abs(wall3), np.abs(towall3), 'Wall [cm]', output_path, 'wall towall 100 cut', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'towall 100 cut', label1 = 'wall 100 cut')
    generic_histogram2(np.abs(wall4), np.abs(towall4), 'Wall [cm]', output_path, 'wall towall 150 cut', y_name = yname, label=label, bins=20, range = (0, 1800), label2 = 'towall 150 cut', label1 = 'wall 150 cut')
    
    
    
    #generic_histogram2(wall_gev_cut, wall_cut, 'dwall [cm]', output_path, 'dwall cut but smaller', y_name = yname, label = label, bins=20, range = (0, 200), label1 = 'gamma end vertex d_wall with towall <100 cut', label2 = 'gamma generation d_wall with towall <100 cut')
    #generic_histogram2(wall_gev, wall, 'dwall [cm]', output_path, 'dwall no cut', y_name = yname, label = label, bins=20, range = (0, 400), label1 = 'gamma end vertex d_wall', label2 = 'gamma generation d_wall')
    #generic_histogram2(wall_gev, wall, 'dwall [cm]', output_path, 'dwall no cut but smaller', y_name = yname, label = label, bins=20, range = (0, 200), label1 = 'gamma end vertex d_wall', label2 = 'gamma generation d_wall')
    print('18')
    #generic_histogram(gamma_end_vtx_x, 'e+/e- pair production position X [cm]', output_path, 'truth_gamma_end_vtx_x', y_name = yname, label=label, bins = 20)
    print('19')
    #generic_histogram(gamma_end_vtx_y, 'e+/e- pair production position Y [cm]', output_path, 'truth_gamma_end_vtx_y', y_name = yname, label=label, bins=20)
    print('20')
    #generic_histogram(gamma_end_vtx_z, 'e+/e- pair production position Z [cm]', output_path, 'truth_gamma_end_vtx_z', y_name = yname, label=label, bins=20)
    print('21')
    #generic_histogram(gamma_end_vtx_r, 'e+/e- pair production position R [cm]', output_path, 'truth_gamma_end_vtx_R', y_name=yname, label=label, bins=20)
    print('22')
    #generic_histogram2(gamma_end_vtx_x, position_x, 'Position X [cm]', output_path, 'vertex vs position X', y_name = yname, label=label, range = (-2000, 2000), bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('23')
    #generic_histogram2(gamma_end_vtx_y, position_y, 'Position Y [cm]', output_path, 'vertex vs position Y', y_name = yname, range = (-2000, 2000) ,label=label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('24')
    #generic_histogram2(gamma_end_vtx_z, position_z, 'Position Z [cm]', output_path, 'vertex vs position Z', range = (-2000, 2000), y_name = yname, label=label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    #generic_histogram2(gamma_end_vtx_z, position_z, 'Position Z [cm]', output_path, 'vertex vs position Z absolute smallest', range = (1700, 1850), y_name = yname, label=label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('25')
    #generic_histogram2(gamma_end_vtx_r, position_r, 'Position r [cm]', output_path, 'vertex vs position R', y_name = yname, range = (0, 2000), label = label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('26')
    #generic_histogram2(gamma_end_vtx_r, position_r, 'Position r [cm]', output_path, 'vertex vs position R small', y_name = yname, range = (1500, 1800), label = label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('27')
    #generic_histogram2(gamma_end_vtx_r, position_r, 'Position r [cm]', output_path, 'vertex vs position R smaller', y_name = yname, range = (1650, 1750), label = label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('28')

    #generic_histogram2(towall_gev, towall, 'Towall [cm]', output_path, 'towall_gev and towall', range = [0,2000], y_name = yname, label=label, bins=20, label1 = 'Position of $e^{+}/e^{-}$ generation towall', label2 = 'Position of gamma generation towall')
    print('29')
    #generic_histogram2(towall_gev, towall, 'Towall [cm]', output_path, 'towall_gev and towall small', range = [0,100], y_name = yname, label=label, bins=20, label1 = 'Position of $e^{+}/e^{-}$ generation towall', label2 = 'Position of gamma generation towall')
    print('30')
    #generic_histogram2(wall_gev, wall, 'd_wall [cm]', output_path, 'wall_gev and wall', range = [0,2000], y_name = yname, label=label, bins=20, label1 = 'Position of $e^{+}/e^{-}$ generation d_wall', label2 = 'Position of gamma generation d_wall')
    print('31')
    #generic_histogram2(wall_gev, wall, 'd_wall [cm]', output_path, 'wall_gev and wall small', range = [0,100], y_name = yname, label=label, bins=20, label1 = 'Position of $e^{+}/e^{-}$ generation d_wall', label2 = 'Position of gamma generation d_wall')
    print('32')
    #generic_histogram2(gamma_end_vtx_z, position_z, 'Position Z [cm]', output_path, 'vertex vs position Z smaller', y_name = yname, range = (1550, 1800), label = label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('33')
    #generic_histogram2(gamma_end_vtx_x, position_x, 'Position X [cm]', output_path, 'vertex vs position X small', y_name = yname, label=label, range = (1500, 1800), bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('34')
    #generic_histogram2(gamma_end_vtx_y, position_y, 'Position Y [cm]', output_path, 'vertex vs position Y small', y_name = yname, range = (1500, 1800) ,label=label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('35')
    #generic_histogram2(gamma_end_vtx_z, position_z, 'Position Z [cm]', output_path, 'vertex vs position Z small', range = (1500, 1800), y_name = yname, label=label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    print('36')
    #generic_histogram2(gamma_end_vtx_r, position_r, 'Position R [cm]', output_path, 'vertex vs position R small', range = (1500, 1800), y_name = yname, label=label, bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')


   # generic_histogram_ratio(gamma_end_vtx_x, position_x, 'Position X [cm]', output_path, 'vertex vs position X_ratio', label=label, y_name=yname ,range = (-2000, 2000), bins = 20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    #generic_histogram_ratio(gamma_end_vtx_y, position_y, 'Position Y [cm]', output_path, 'vertex vs position Y_ratio',  range = (-2000, 2000), y_name=yname, label=label, bins=20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    #generic_histogram_ratio(gamma_end_vtx_z, position_z, 'Position Z [cm]', output_path, 'vertex vs position Z_ratio', y_name=yname, label=label,  range = (-2000, 2000), bins=20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    #generic_histogram_ratio(gamma_end_vtx_r, position_r, 'Position R [cm]', output_path, 'vertex vs position R_ratio', y_name=yname, label=label,  range = (0, 2000), bins=20, label1 = 'Position of $e^{+}/e^{-}$ generation', label2 = 'Position of gamma generation')
    if truthOnly:
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
    generic_histogram(num_pmt, 'Number of PMTs', output_path, 'num_pmt', y_name = yname, label=label, range=[0,4000], bins=20)

