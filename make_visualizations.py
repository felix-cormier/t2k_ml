from generics_python.make_plots import generic_3D_plot, generic_2D_plot, generic_det_unraveler
import random
import numpy as np
from angle_between import *
from plot_wcsim import *
from tqdm import tqdm
import torch
from generics_python.make_plots import *

def decision(probability):
    return random.random() < probability

def load_geofile(geofile_name):

    with np.load(geofile_name) as data:
        return data['position']

def convert_values(geofile,input):
    return [geofile[x] for x in input]


def make_visualizations(h5_file, output_path):
    """Make event displays for some events in the input h5_file. Visualizations will be of the PMTs, as well as truth positions
    


    Args:
        h5_file (_type_): File to draw events from
        output_path (_type_): Where to save the plots
    """
    geofile = load_geofile('data/geofile.npz')
    print("Keys: %s" % h5_file.keys())
    print(h5_file['event_hits_index'].shape)
    #How many event displays to make
    num_visualization = 50

    max = h5_file['event_hits_index'].shape[0]
    print('uniqueness', np.unique(h5_file['labels'], return_counts = True))
    ratio = num_visualization/max
    random.seed(0)

    x_elec=[]
    y_elec=[]
    z_elec=[]
    
    x_muon=[]
    y_muon=[]
    z_muon=[]

    x_dir_muon, y_dir_muon, z_dir_muon = [], [], []
    x_dir_elec, y_dir_elec, z_dir_elec = [], [], []

    truth_visible_energy_elec, truth_visible_energy_muon = [], []
    energies_muon = []
    energies_electron = []
    energies = []
    num_pmt_muon = []
    num_pmt_elec = []

    temp_towall_gev = []
    towall_gev = []
    yname = 'Counts'
    yaxis = 'log'
    r_dir_muon = []
    r_dir_elec = []
    r_dir_gam = []
    r_dir_gen_elec = []
    r_dir_generated_particles = []
    theta = []
    
    time_muon = []
    time_electron = []

    hits = []
    total_charge_muon = []
    total_charge_electron = []
    mean_time_electron = []
    mean_time_muon = []
    total_charge = []
    mean_time = []
    
    labels = h5_file['labels']
    #time = h5_file['hit_time'][:]
    #dec_elec_exists = h5_file['decay_electron_exists'][:]
    #dec_elec_time = h5_file['decay_electron_time'][:]
    '''
    for i,index in enumerate(h5_file['event_hits_index']):#[999950:1000050]):
        #i = 999950 + i
        #print(h5_file['hit_time'])
        if i < max-1:
            #print(i)
            #wall_out_gev, towall_out_gev= calculate_wcsim_wall_variables(h5_file['positions'][i], h5_file['directions'][i])
            #temp_towall_gev.append(towall_out_gev)
            #print(i)
            if labels[i] == 0:
                time_muon.append(float(h5_file['hit_time'][i]))
                #print('time_muon = ', time_muon)
                
                num_pmt_muon.append(h5_file['event_hits_index'][i+1] - h5_file['event_hits_index'][i])
                energies_muon.append(float(h5_file['energies'][i]))
                total_charge_muon.append(np.sum(h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                mean_time_muon.append(np.mean(h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                x_muon.append(float(h5_file['positions'][i][:,0]))
                y_muon.append(float(h5_file['positions'][i][:,1]))
                z_muon.append(float(h5_file['positions'][i][:,2]))
                x_dir_muon.append(float(h5_file['directions'][i][:,0]))
                y_dir_muon.append(float(h5_file['directions'][i][:,1]))
                z_dir_muon.append(float(h5_file['directions'][i][:,2]))
                truth_visible_energy_muon.append(float(h5_file['energies'][i])-get_cherenkov_threshold(h5_file['labels'][i]))
                
            else:
                time_electron.append(float(h5_file['hit_time'][i]))
                #print('time_electron = ', time_electron)
                
                energies_electron.append(float(h5_file['energies'][i]))
                num_pmt_elec.append(h5_file['event_hits_index'][i+1] - h5_file['event_hits_index'][i])
                total_charge_electron.append(np.sum(h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                mean_time_electron.append(np.mean(h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                x_elec.append(float(h5_file['positions'][i][:,0]))
                y_elec.append(float(h5_file['positions'][i][:,1]))
                z_elec.append(float(h5_file['positions'][i][:,2]))
                x_dir_elec.append(float(h5_file['directions'][i][:,0]))
                y_dir_elec.append(float(h5_file['directions'][i][:,1]))
                z_dir_elec.append(float(h5_file['directions'][i][:,2]))
                truth_visible_energy_elec.append(float(h5_file['energies'][i])-get_cherenkov_threshold(h5_file['labels'][i]))
                
            #energies.append(float(h5_file['energies'][i]))
    
            #pmt_positions = np.array(convert_values(geofile,h5_file['hit_pmt'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
    '''     
    '''
    '''
    '''
            if decision(ratio) and (h5_file['event_hits_index'][i+1]- h5_file['event_hits_index'][i])> 0:
                print(i)
                print(h5_file['labels'][i])
                charges = h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]
                x = pmt_positions[:,0]
                y = pmt_positions[:,1]
                z = pmt_positions[:,2]


                output_name = 'digi_500MeV_vis_'+str(i)
                output_name_xy = 'digi_500MeV_vis_'+str(i)+'X-Y'
                output_name_xz = 'digi_500MeV_vis_'+str(i)+'X-Z'
                output_name_yz = 'digi_500MeV_vis_'+str(i)+'Y-Z'
                generic_3D_plot(x,y,z, charges, 'X [cm]', 'Y [cm]', 'Z [cm]', 'PMT charge', output_path, output_name)
                generic_det_unraveler(x, z, charges, 'X [cm]', 'Z [cm]', 'PMT charge', output_path, output_name_xz)
                generic_det_unraveler(x, y, charges, 'X [cm]', 'Y [cm]', 'PMT charge', output_path, output_name_xy)
                generic_det_unraveler(y, z, charges, 'Y [cm]', 'Z [cm]', 'PMT charge', output_path, output_name_yz)
    '''
    '''
    
    
    hits = np.array(hits)
    energies_muon = np.array(energies_muon)
    energies_electron = np.array(energies_electron)
    mean_time_muon = np.array(mean_time_muon)
    mean_time_electron = np.array(mean_time_electron)
    total_charge_muon = np.array(total_charge_muon)
    total_charge_electron = np.array(total_charge_electron)
    energies = np.array(energies)
    truth_visible_energy_elec = np.array(truth_visible_energy_elec)
    truth_visible_energy_muon = np.array(truth_visible_energy_muon)
    '''
    
    #time_muon = np.array(time_muon)
    #time_electron = np.array(time_electron)
    #print('len time muon = ', len(time_muon))
    #print('len time electron = ', len(time_electron))
    '''
    x_muon = np.array(x_muon)
    y_muon = np.array(y_muon)
    z_muon = np.array(z_muon)

    x_elec = np.array(x_elec)
    y_elec = np.array(y_elec)
    z_elec = np.array(z_elec)

    x_dir_elec = np.array(x_dir_elec)
    y_dir_elec = np.array(y_dir_elec)
    z_dir_elec = np.array(z_dir_elec)
    
    x_dir_muon = np.array(x_dir_muon)
    y_dir_muon = np.array(y_dir_muon)
    z_dir_muon = np.array(z_dir_muon)

    hits_muon = []
    hits_elec = []

    hits_muon = np.array(num_pmt_muon)
    hits_elec = np.array(num_pmt_elec)
    '''
    #generic_histogram(time_muon, 'Truth time', output_path, 'Truth_time_muon', y_name = yname, label = 'time_muon', range = (0, 11000), y_axis = yaxis, bins = 20)
    #generic_histogram(time_electron, 'Truth time', output_path, 'Truth_time_electron', y_name = yname, range = (0, 11000), y_axis = yaxis, label = 'time_electron', bins = 20)
    '''
    generic_histogram(x_dir_elec, 'Truth Direction X', output_path, 'truth_elec_direction_x', y_name = yname, label = 'electron', bins=20)
    generic_histogram(y_dir_elec, 'Truth Direction X', output_path, 'truth_elec_direction_y', y_name = yname, label = 'electron', bins=20)
    generic_histogram(z_dir_elec, 'Truth Direction X', output_path, 'truth_elec_direction_z', y_name = yname, label = 'electron', bins=20)
    generic_histogram(x_dir_muon, 'Truth Direction X', output_path, 'truth_muon_direction_x', y_name = yname, label = 'muon', bins=20)
    generic_histogram(y_dir_muon, 'Truth Direction Y', output_path, 'truth_muon_direction_y', y_name = yname, label = 'muon', bins=20)
    generic_histogram(z_dir_muon, 'Truth Direction Z', output_path, 'truth_muon_direction_z', y_name = yname, label = 'muon', bins=20)
    generic_histogram(x_elec, 'Truth position X [cm]', output_path, 'truth_position_x_elec', y_name = yname, label = 'electron',  bins=20)
    generic_histogram(y_elec, 'Truth position Y [cm]', output_path, 'truth_position_y_elec', y_name = yname, label = 'electron',  bins=20)
    generic_histogram(z_elec, 'Truth position Z [cm]', output_path, 'truth_position_z_elec', y_name = yname, label = 'electron',  bins=20)
    generic_histogram(x_muon, 'Truth position X [cm]', output_path, 'truth_position_x_muon', y_name = yname, label = 'muon',  bins=20)
    generic_histogram(y_muon, 'Truth position Y [cm]', output_path, 'truth_position_y_muon', y_name = yname, label = 'muon',  bins=20)
    generic_histogram(z_muon, 'Truth position Z [cm]', output_path, 'truth_position_z_muon', y_name = yname, label = 'muon',  bins=20)

    generic_histogram(energies_muon, 'Truth Energy [MeV]', output_path, 'truth_energy', y_name = yname, label = 'muon', bins=20)
    generic_histogram(energies_electron, 'Truth Energy [MeV]', output_path, 'truth_energy', y_name = yname, label = 'electron', bins=20)
    generic_histogram(truth_visible_energy_muon, 'Truth Visible Energy [MeV]', output_path, 'truth_visible_energy', y_name = yname, label = 'muon', bins=20)
    generic_histogram(truth_visible_energy_elec, 'Truth Visible Energy [MeV]', output_path, 'truth_visible_energy', y_name = yname, label = 'electron', bins=20)
  
    generic_histogram2(x_dir_elec, x_dir_muon, 'Truth Direction X [cm]', output_path, 'X direction', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    generic_histogram2(y_dir_elec, y_dir_muon, 'Truth Direction Y [cm]', output_path, 'Y direction', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    generic_histogram2(z_dir_elec, z_dir_muon, 'Truth Direction X [cm]', output_path, 'Z direction', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    generic_histogram2(x_elec, x_muon, 'Truth Direction X [cm]', output_path, 'X direction', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    generic_histogram2(y_elec, y_muon, 'Truth Direction Y [cm]', output_path, 'Y direction', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    generic_histogram2(z_elec, z_muon, 'Truth Direction X [cm]', output_path, 'Z direction', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    generic_histogram2(energies_electron, energies_muon, 'Truth Energies', output_path, 'Truth Energies', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    generic_histogram2(truth_visible_energy_elec, truth_visible_energy_muon, 'Truth visible energy', output_path, 'Truth visible energy', y_name = yname, bins=20, label2 = 'muon', label1 = 'electron')
    '''
    '''
    tot_charge_muon_lt100 = []
    tot_charge_muon_12 = []
    tot_charge_muon_23 = []
    tot_charge_muon_34 = []
    tot_charge_muon_45 = []
    tot_charge_muon_56 = []
    tot_charge_muon_67 = []
    tot_charge_muon_78 = []
    tot_charge_muon_89 = []
    tot_charge_muon_910 = []
    tot_charge_muon_gt10 = []

    tot_charge_elec_lt100 = []
    tot_charge_elec_12 = []
    tot_charge_elec_23 = []
    tot_charge_elec_34 = []
    tot_charge_elec_45 = []
    tot_charge_elec_56 = []
    tot_charge_elec_67 = []
    tot_charge_elec_78 = []
    tot_charge_elec_89 = []
    tot_charge_elec_910 = []
    tot_charge_elec_gt10 = []

    mean_time_muon_lt100 = []
    mean_time_muon_12 = []
    mean_time_muon_23 = []
    mean_time_muon_34 = []
    mean_time_muon_45 = []
    mean_time_muon_56 = []
    mean_time_muon_67 = []
    mean_time_muon_78 = []
    mean_time_muon_89 = []
    mean_time_muon_910 = []
    mean_time_muon_gt10 = []

    mean_time_electron_lt100 = []
    mean_time_electron_12 = []
    mean_time_electron_23 = []
    mean_time_electron_34 = []
    mean_time_electron_45 = []
    mean_time_electron_56 = []
    mean_time_electron_67 = []
    mean_time_electron_78 = []
    mean_time_electron_89 = []
    mean_time_electron_910 = []
    mean_time_electron_gt10 = []

    hits_muon_lt100 = []
    hits_muon_12 = []
    hits_muon_23 = []
    hits_muon_34 = []
    hits_muon_45 = []
    hits_muon_56 = []
    hits_muon_67 = []
    hits_muon_78 = []
    hits_muon_89 = []
    hits_muon_910 = []
    hits_muon_gt10 = []
    
    hits_elec_lt100 = []
    hits_elec_12 = []
    hits_elec_23 = []
    hits_elec_34 = []
    hits_elec_45 = []
    hits_elec_56 = []
    hits_elec_67 = []
    hits_elec_78 = []
    hits_elec_89 = []
    hits_elec_910 = []
    hits_elec_gt10 = []
    
    print('mean time muon', mean_time_muon)
    print('energies muon', energies_muon)
    mean_time_muon_lt100 = mean_time_muon[energies_muon < 100]
    mean_time_muon_12 = mean_time_muon[(energies_muon > 100) & (energies_muon < 200)]
    mean_time_muon_23 = mean_time_muon[(energies_muon > 200) & (energies_muon < 300)]
    mean_time_muon_34 = mean_time_muon[(energies_muon > 300) & (energies_muon < 400)]
    mean_time_muon_45 = mean_time_muon[(energies_muon > 400) & (energies_muon < 500)]
    mean_time_muon_56 = mean_time_muon[(energies_muon > 500) & (energies_muon < 600)]
    mean_time_muon_67 = mean_time_muon[(energies_muon > 600) & (energies_muon < 700)]
    mean_time_muon_78 = mean_time_muon[(energies_muon > 700) & (energies_muon < 800)]
    mean_time_muon_89 = mean_time_muon[(energies_muon > 800) & (energies_muon < 900)]
    mean_time_muon_910 = mean_time_muon[(energies_muon > 900) & (energies_muon < 1000)]
    mean_time_muon_gt10 = mean_time_muon[(energies_muon > 1000)]

    mean_time_electron_lt100 = mean_time_electron[(energies_electron < 100)]
    mean_time_electron_12 = mean_time_electron[(energies_electron > 100) & (energies_electron < 200)]
    mean_time_electron_23 = mean_time_electron[(energies_electron > 200) & (energies_electron < 300)]
    mean_time_electron_34 = mean_time_electron[(energies_electron > 300) & (energies_electron < 400)]
    mean_time_electron_45 = mean_time_electron[(energies_electron > 400) & (energies_electron < 500)]
    mean_time_electron_56 = mean_time_electron[(energies_electron > 500) & (energies_electron < 600)]
    mean_time_electron_67 = mean_time_electron[(energies_electron > 600) & (energies_electron < 700)]
    mean_time_electron_78 = mean_time_electron[(energies_electron > 700) & (energies_electron < 800)]
    mean_time_electron_89 = mean_time_electron[(energies_electron > 800) & (energies_electron < 900)]
    mean_time_electron_910 = mean_time_electron[(energies_electron > 900) & (energies_electron < 1000)]
    mean_time_electron_gt10 = mean_time_electron[(energies_electron > 1000)]

    tot_charge_muon_lt100 = total_charge_muon[(energies_muon < 100)]
    tot_charge_muon_12 = total_charge_muon[(energies_muon > 100) & (energies_muon < 200)]
    tot_charge_muon_23 = total_charge_muon[(energies_muon > 200) & (energies_muon < 300)]
    tot_charge_muon_34 = total_charge_muon[(energies_muon > 300) & (energies_muon < 400)]
    tot_charge_muon_45 = total_charge_muon[(energies_muon > 400) & (energies_muon < 500)]
    tot_charge_muon_56 = total_charge_muon[(energies_muon > 500) & (energies_muon < 600)]
    tot_charge_muon_67 = total_charge_muon[(energies_muon > 600) & (energies_muon < 700)]
    tot_charge_muon_78 = total_charge_muon[(energies_muon > 700) & (energies_muon < 800)]
    tot_charge_muon_89 = total_charge_muon[(energies_muon > 800) & (energies_muon < 900)]
    tot_charge_muon_910 = total_charge_muon[(energies_muon > 900) & (energies_muon < 1000)]
    tot_charge_muon_gt10 = total_charge_muon[(energies_muon > 1000)]

    tot_charge_electron_lt100 = total_charge_electron[(energies_electron < 100)]
    tot_charge_electron_12 = total_charge_electron[(energies_electron > 100) & (energies_electron < 200)]
    tot_charge_electron_23 = total_charge_electron[(energies_electron > 200) & (energies_electron < 300)]
    tot_charge_electron_34 = total_charge_electron[(energies_electron > 300) & (energies_electron < 400)]
    tot_charge_electron_45 = total_charge_electron[(energies_electron > 400) & (energies_electron < 500)]
    tot_charge_electron_56 = total_charge_electron[(energies_electron > 500) & (energies_electron < 600)]
    tot_charge_electron_67 = total_charge_electron[(energies_electron > 600) & (energies_electron < 700)]
    tot_charge_electron_78 = total_charge_electron[(energies_electron > 700) & (energies_electron < 800)]
    tot_charge_electron_89 = total_charge_electron[(energies_electron > 800) & (energies_electron < 900)]
    tot_charge_electron_910 = total_charge_electron[(energies_electron > 900) & (energies_electron < 1000)]
    tot_charge_electron_gt10 = total_charge_electron[(energies_electron > 1000)]
    
    time_hist(mean_time_muon, mean_time_electron, bins = 50, xlimit = None, name = 'All', title = 'All')
    time_hist(mean_time_muon_lt100, mean_time_electron_lt100, bins = 50, xlimit = None, name = 'lt100', title = 'E<100')
    time_hist(mean_time_muon_12, mean_time_electron_12, bins = 50, xlimit = None, name = '12', title = '100<E<200')
    time_hist(mean_time_muon_23, mean_time_electron_23, bins = 50, xlimit = None, name = '23', title = '200<E<300')
    time_hist(mean_time_muon_34, mean_time_electron_34, bins = 50, xlimit = None, name = '34', title = '300<E<400')
    time_hist(mean_time_muon_45, mean_time_electron_45, bins = 50, xlimit = None, name = '45', title = '400<E<500')
    time_hist(mean_time_muon_56, mean_time_electron_56, bins = 50, xlimit = None, name = '56', title = '500<E<600')
    time_hist(mean_time_muon_67, mean_time_electron_67, bins = 50, xlimit = None, name = '67', title = '600<E<700')
    time_hist(mean_time_muon_78, mean_time_electron_78, bins = 50, xlimit = None, name = '78', title = '700<E<800')
    time_hist(mean_time_muon_89, mean_time_electron_89, bins = 50, xlimit = None, name = '89', title = '800<E<900')
    time_hist(mean_time_muon_910, mean_time_electron_910, bins = 50, xlimit = None, name = '910', title = '900<E<1000')
    time_hist(mean_time_muon_gt10, mean_time_electron_gt10, bins = 50, xlimit = None, name = 'gt10', title = '1000<E')

    charge_hist(total_charge_muon, total_charge_electron, bins = 50, xlimit = (0, 13000), name = 'All', title = 'All')
    charge_hist(tot_charge_muon_lt100, tot_charge_electron_lt100, bins = 50, xlimit = None, name = 'lt100', title = 'E<100')
    charge_hist(tot_charge_muon_12, tot_charge_electron_12, bins = 50, xlimit = None, name = '12', title = '100<E<200')
    charge_hist(tot_charge_muon_23, tot_charge_electron_23, bins = 50, xlimit = None, name = '23', title = '200<E<300')
    charge_hist(tot_charge_muon_34, tot_charge_electron_34, bins = 50, xlimit = None, name = '34', title = '300<E<400')
    charge_hist(tot_charge_muon_45, tot_charge_electron_45, bins = 50, xlimit = None, name = '45', title = '400<E<500')
    charge_hist(tot_charge_muon_56, tot_charge_electron_56, bins = 50, xlimit = None, name = '56', title = '500<E<600')
    charge_hist(tot_charge_muon_67, tot_charge_electron_67, bins = 50, xlimit = None, name = '67', title = '600<E<700')
    charge_hist(tot_charge_muon_78, tot_charge_electron_78, bins = 50, xlimit = None, name = '78', title = '700<E<800')
    charge_hist(tot_charge_muon_89, tot_charge_electron_89, bins = 50, xlimit = None, name = '89', title = '800<E<900')
    charge_hist(tot_charge_muon_910, tot_charge_electron_910, bins = 50, xlimit = None, name = '910', title = '900<E<1000')
    charge_hist(tot_charge_muon_gt10, tot_charge_electron_gt10, bins = 50, xlimit = None, name = 'gt10', title = '1000<E')

    
    hits_muon_lt100 = hits_muon[(energies_muon < 100)]
    hits_muon_12 = hits_muon[(energies_muon > 100) & (energies_muon < 200) & (hits_muon > 700)]
    hits_muon_23 = hits_muon[(energies_muon > 200) & (energies_muon < 300) & (hits_muon > 700)]
    hits_muon_34 = hits_muon[(energies_muon > 300) & (energies_muon < 400) & (hits_muon > 700)]
    hits_muon_45 = hits_muon[(energies_muon > 400) & (energies_muon < 500) & (hits_muon > 700)]
    hits_muon_56 = hits_muon[(energies_muon > 500) & (energies_muon < 600) & (hits_muon > 700)]
    hits_muon_67 = hits_muon[(energies_muon > 600) & (energies_muon < 700) & (hits_muon > 700)]
    hits_muon_78 = hits_muon[(energies_muon > 700) & (energies_muon < 800) & (hits_muon > 700)]
    hits_muon_89 = hits_muon[(energies_muon > 800) & (energies_muon < 900) & (hits_muon > 700)]
    hits_muon_910 = hits_muon[(energies_muon > 900) & (energies_muon < 1000) & (hits_muon > 700)]
    hits_muon_gt10 = hits_muon[(energies_muon > 1000) & (hits_muon > 700)]

    hits_elec_lt100 = hits_elec[(energies_electron < 100) & (hits_elec > 700)]
    hits_elec_12 = hits_elec[(energies_electron > 100) & (energies_electron < 200) & (hits_elec > 700)]
    hits_elec_23 = hits_elec[(energies_electron > 200) & (energies_electron < 300) & (hits_elec > 700)]
    hits_elec_34 = hits_elec[(energies_electron > 300) & (energies_electron < 400) & (hits_elec > 700)]
    hits_elec_45 = hits_elec[(energies_electron > 400) & (energies_electron < 500) & (hits_elec > 700)]
    hits_elec_56 = hits_elec[(energies_electron > 500) & (energies_electron < 600) & (hits_elec > 700)]
    hits_elec_67 = hits_elec[(energies_electron > 600) & (energies_electron < 700 & (hits_elec > 700))]
    hits_elec_78 = hits_elec[(energies_electron > 700) & (energies_electron < 800) & (hits_elec > 700)]
    hits_elec_89 = hits_elec[(energies_electron > 800) & (energies_electron < 900) & (hits_elec > 700)]
    hits_elec_910 = hits_elec[(energies_electron > 900) & (energies_electron < 1000) & (hits_elec > 700)]
    hits_elec_gt10 = hits_elec[(energies_electron > 1000) & (hits_elec > 700)]
    
    
    hits_hist(hits_muon, hits_elec, bins = 50, xlimit = None, name = 'All', title = 'All')
    hits_hist(hits_muon_lt100, hits_elec_lt100, bins = 50, xlimit = None, name = 'lt100', title = 'E < 100')
    hits_hist(hits_muon_12, hits_elec_12, bins = 50, xlimit = None, name = '12', title = '100<E<200')
    hits_hist(hits_muon_23, hits_elec_23, bins = 50, xlimit = None, name = '23', title = '200<E<300')
    hits_hist(hits_muon_34, hits_elec_34, bins = 50, xlimit = None, name = '34', title = '300<E<400')
    hits_hist(hits_muon_45, hits_elec_45, bins = 50, xlimit = None, name = '45', title = '400<E<500')
    hits_hist(hits_muon_56, hits_elec_56, bins = 50, xlimit = None, name = '56', title = '500<E<600')
    hits_hist(hits_muon_67, hits_elec_67, bins = 50, xlimit = None, name = '67', title = '600<E<700')
    hits_hist(hits_muon_78, hits_elec_78, bins = 50, xlimit = None, name = '78', title = '700<E<800')
    hits_hist(hits_muon_89, hits_elec_89, bins = 50, xlimit = None, name = '89', title = '800<E<900')
    hits_hist(hits_muon_910, hits_elec_910, bins = 50, xlimit = None, name = '910', title = '900<E<1000')
    hits_hist(hits_muon_gt10, hits_elec_gt10, bins = 50, xlimit = None, name = 'gt10', title = 'E > 1000')
    
    


    generic_2D_plot(x_muon,y_muon,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_muon,z_muon,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_muon,z_muon,[-1800,1800], 100, 'Y [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)

    '''
