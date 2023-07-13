from generics_python.make_plots import generic_3D_plot, generic_2D_plot, generic_det_unraveler
import random
import numpy as np
from angle_between import *
from plot_wcsim import calculate_wcsim_wall_variables
from tqdm import tqdm


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

    x_pos=[]
    y_pos=[]
    z_pos=[]
    x_stop_pos=[]
    y_stop_pos=[]
    z_stop_pos=[]
    
    energies_gamma = []
    energies_electron = []
    energies = []
    num_pmt_gamma = []
    num_pmt_elec = []

    temp_towall_gev = []
    towall_gev = []

    r_dir_pos = []
    r_dir_elec = []
    r_dir_gam = []
    r_dir_gen_elec = []
    r_dir_generated_particles = []
    theta = []

    hits = []
    total_charge_gamma = []
    total_charge_electron = []
    mean_time_electron = []
    mean_time_gamma = []

    labels = h5_file['labels']
    energy = h5_file['energies']
    
    for i,index in enumerate(h5_file['event_hits_index'][500000:500500]):
        i = 500000 + i
        if i < max-1:
            #r_dir_elec.append(h5_file['directions_electron'][i][:])
            #r_dir_pos.append(h5_file['directions_positron'][i][:])
            #r_dir_generated_particles.append(h5_file['directions'][i][:])
            #wall_out_gev, towall_out_gev= calculate_wcsim_wall_variables(h5_file['positions'][i], h5_file['directions'][i])
            #temp_towall_gev.append(towall_out_gev)
            if labels[i] == 0:
                num_pmt_gamma.append(h5_file['event_hits_index'][i+1] - h5_file['event_hits_index'][i])
                energies_gamma.append(float(h5_file['energies'][i]))
                total_charge_gamma.append(np.sum(h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                mean_time_gamma.append(np.mean(h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
            else:
                energies_electron.append(float(h5_file['energies'][i]))
                num_pmt_elec.append(h5_file['event_hits_index'][i+1] - h5_file['event_hits_index'][i])
                total_charge_electron.append(np.sum(h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                mean_time_electron.append(np.mean(h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
            
            energies.append(float(h5_file['energies'][i]))

            #pmt_positions = np.array(convert_values(geofile,h5_file['hit_pmt'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
            x_pos.append(float(h5_file['positions'][i][:,0])) 
            y_pos.append(float(h5_file['positions'][i][:,1])) 
            z_pos.append(float(h5_file['positions'][i][:,2]))
            #r_dir_elec.append((h5_file['directions_electron'][i][:]))
            
            #r_dir_pos.append((h5_file['directions_positron'][i][:]))
            #energies.append(float(h5_file['energies'][i]))
            
            #x_stop_pos.append(float(h5_file['stop_positions'][i][:,0])) 
            #y_stop_pos.append(float(h5_file['stop_positions'][i][:,1])) 
            #z_stop_pos.append(float(h5_file['stop_positions'][i][:,2])) 
            
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
            
    r_dir_generated_particles = np.array(r_dir_generated_particles)
    hits = np.array(hits)
    energies_gamma = np.array(energies_gamma)
    energies_electron = np.array(energies_electron)
    mean_time_gamma = np.array(mean_time_gamma)
    mean_time_electron = np.array(mean_time_electron)
    total_charge_gamma = np.array(total_charge_gamma)
    total_charge_electron = np.array(total_charge_electron)
    energies = np.array(energies)

    r_dir_gen_elec = r_dir_generated_particles[(labels == 1)]
    r_dir_gen_gam = r_dir_generated_particles[(labels == 0)]

    hits_gamma = []
    hits_elec = []

    hits_gamma = np.array(num_pmt_gamma)
    hits_elec = np.array(num_pmt_elec)
    
    tot_charge_gamma_lt100 = []
    tot_charge_gamma_12 = []
    tot_charge_gamma_23 = []
    tot_charge_gamma_34 = []
    tot_charge_gamma_45 = []
    tot_charge_gamma_56 = []
    tot_charge_gamma_67 = []
    tot_charge_gamma_78 = []
    tot_charge_gamma_89 = []
    tot_charge_gamma_910 = []
    tot_charge_gamma_gt10 = []

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

    mean_time_gamma_lt100 = []
    mean_time_gamma_12 = []
    mean_time_gamma_23 = []
    mean_time_gamma_34 = []
    mean_time_gamma_45 = []
    mean_time_gamma_56 = []
    mean_time_gamma_67 = []
    mean_time_gamma_78 = []
    mean_time_gamma_89 = []
    mean_time_gamma_910 = []
    mean_time_gamma_gt10 = []

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

    hits_gamma_lt100 = []
    hits_gamma_12 = []
    hits_gamma_23 = []
    hits_gamma_34 = []
    hits_gamma_45 = []
    hits_gamma_56 = []
    hits_gamma_67 = []
    hits_gamma_78 = []
    hits_gamma_89 = []
    hits_gamma_910 = []
    hits_gamma_gt10 = []
    
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

    mean_time_gamma_lt100 = mean_time_gamma[energies_gamma < 100]
    mean_time_gamma_12 = mean_time_gamma[(energies_gamma > 100) & (energies_gamma < 200)]
    mean_time_gamma_23 = mean_time_gamma[(energies_gamma > 200) & (energies_gamma < 300)]
    mean_time_gamma_34 = mean_time_gamma[(energies_gamma > 300) & (energies_gamma < 400)]
    mean_time_gamma_45 = mean_time_gamma[(energies_gamma > 400) & (energies_gamma < 500)]
    mean_time_gamma_56 = mean_time_gamma[(energies_gamma > 500) & (energies_gamma < 600)]
    mean_time_gamma_67 = mean_time_gamma[(energies_gamma > 600) & (energies_gamma < 700)]
    mean_time_gamma_78 = mean_time_gamma[(energies_gamma > 700) & (energies_gamma < 800)]
    mean_time_gamma_89 = mean_time_gamma[(energies_gamma > 800) & (energies_gamma < 900)]
    mean_time_gamma_910 = mean_time_gamma[(energies_gamma > 900) & (energies_gamma < 1000)]
    mean_time_gamma_gt10 = mean_time_gamma[(energies_gamma > 1000)]

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

    tot_charge_gamma_lt100 = total_charge_gamma[(energies_gamma < 100)]
    tot_charge_gamma_12 = total_charge_gamma[(energies_gamma > 100) & (energies_gamma < 200)]
    tot_charge_gamma_23 = total_charge_gamma[(energies_gamma > 200) & (energies_gamma < 300)]
    tot_charge_gamma_34 = total_charge_gamma[(energies_gamma > 300) & (energies_gamma < 400)]
    tot_charge_gamma_45 = total_charge_gamma[(energies_gamma > 400) & (energies_gamma < 500)]
    tot_charge_gamma_56 = total_charge_gamma[(energies_gamma > 500) & (energies_gamma < 600)]
    tot_charge_gamma_67 = total_charge_gamma[(energies_gamma > 600) & (energies_gamma < 700)]
    tot_charge_gamma_78 = total_charge_gamma[(energies_gamma > 700) & (energies_gamma < 800)]
    tot_charge_gamma_89 = total_charge_gamma[(energies_gamma > 800) & (energies_gamma < 900)]
    tot_charge_gamma_910 = total_charge_gamma[(energies_gamma > 900) & (energies_gamma < 1000)]
    tot_charge_gamma_gt10 = total_charge_gamma[(energies_gamma > 1000)]

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
    
    time_hist(mean_time_gamma, mean_time_electron, bins = 50, xlimit = (1000, 1100), name = 'All', title = 'All')
    time_hist(mean_time_gamma_lt100, mean_time_electron_lt100, bins = 50, xlimit = (1000, 1100), name = 'lt100', title = 'E<100')
    time_hist(mean_time_gamma_12, mean_time_electron_12, bins = 50, xlimit = (1000, 1100), name = '12', title = '100<E<200')
    time_hist(mean_time_gamma_23, mean_time_electron_23, bins = 50, xlimit = (1000, 1100), name = '23', title = '200<E<300')
    time_hist(mean_time_gamma_34, mean_time_electron_34, bins = 50, xlimit = (1000, 1100), name = '34', title = '300<E<400')
    time_hist(mean_time_gamma_45, mean_time_electron_45, bins = 50, xlimit = (1000, 1100), name = '45', title = '400<E<500')
    time_hist(mean_time_gamma_56, mean_time_electron_56, bins = 50, xlimit = (1000, 1100), name = '56', title = '500<E<600')
    time_hist(mean_time_gamma_67, mean_time_electron_67, bins = 50, xlimit = (1000, 1100), name = '67', title = '600<E<700')
    time_hist(mean_time_gamma_78, mean_time_electron_78, bins = 50, xlimit = (1000, 1100), name = '78', title = '700<E<800')
    time_hist(mean_time_gamma_89, mean_time_electron_89, bins = 50, xlimit = (1000, 1100), name = '89', title = '800<E<900')
    time_hist(mean_time_gamma_910, mean_time_electron_910, bins = 50, xlimit = (1000, 1100), name = '910', title = '900<E<1000')
    time_hist(mean_time_gamma_gt10, mean_time_electron_gt10, bins = 50, xlimit = (1000, 1100), name = 'gt10', title = '1000<E')

    charge_hist(total_charge_gamma, total_charge_electron, bins = 50, xlimit = (0, 13000), name = 'All', title = 'All')
    charge_hist(tot_charge_gamma_lt100, tot_charge_electron_lt100, bins = 50, xlimit = None, name = 'lt100', title = 'E<100')
    charge_hist(tot_charge_gamma_12, tot_charge_electron_12, bins = 50, xlimit = (500, 3000), name = '12', title = '100<E<200')
    charge_hist(tot_charge_gamma_23, tot_charge_electron_23, bins = 50, xlimit = (1500, 4000), name = '23', title = '200<E<300')
    charge_hist(tot_charge_gamma_34, tot_charge_electron_34, bins = 50, xlimit = (2500, 5000), name = '34', title = '300<E<400')
    charge_hist(tot_charge_gamma_45, tot_charge_electron_45, bins = 50, xlimit = (3000, 6000), name = '45', title = '400<E<500')
    charge_hist(tot_charge_gamma_56, tot_charge_electron_56, bins = 50, xlimit = (4000, 7000), name = '56', title = '500<E<600')
    charge_hist(tot_charge_gamma_67, tot_charge_electron_67, bins = 50, xlimit = (5000, 8000), name = '67', title = '600<E<700')
    charge_hist(tot_charge_gamma_78, tot_charge_electron_78, bins = 50, xlimit = (6000, 9000), name = '78', title = '700<E<800')
    charge_hist(tot_charge_gamma_89, tot_charge_electron_89, bins = 50, xlimit = (7000, 10000), name = '89', title = '800<E<900')
    charge_hist(tot_charge_gamma_910, tot_charge_electron_910, bins = 50, xlimit = (7500, 11000), name = '910', title = '900<E<1000')
    charge_hist(tot_charge_gamma_gt10, tot_charge_electron_gt10, bins = 50, xlimit = (8000, 13000), name = 'gt10', title = '1000<E')

    
    hits_gamma_lt100 = hits_gamma[(energies_gamma < 100)]
    hits_gamma_12 = hits_gamma[(energies_gamma > 100) & (energies_gamma < 200) & (hits_gamma > 700)]
    hits_gamma_23 = hits_gamma[(energies_gamma > 200) & (energies_gamma < 300) & (hits_gamma > 700)]
    hits_gamma_34 = hits_gamma[(energies_gamma > 300) & (energies_gamma < 400) & (hits_gamma > 700)]
    hits_gamma_45 = hits_gamma[(energies_gamma > 400) & (energies_gamma < 500) & (hits_gamma > 700)]
    hits_gamma_56 = hits_gamma[(energies_gamma > 500) & (energies_gamma < 600) & (hits_gamma > 700)]
    hits_gamma_67 = hits_gamma[(energies_gamma > 600) & (energies_gamma < 700) & (hits_gamma > 700)]
    hits_gamma_78 = hits_gamma[(energies_gamma > 700) & (energies_gamma < 800) & (hits_gamma > 700)]
    hits_gamma_89 = hits_gamma[(energies_gamma > 800) & (energies_gamma < 900) & (hits_gamma > 700)]
    hits_gamma_910 = hits_gamma[(energies_gamma > 900) & (energies_gamma < 1000) & (hits_gamma > 700)]
    hits_gamma_gt10 = hits_gamma[(energies_gamma > 1000) & (hits_gamma > 700)]

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
    
    #print(num_pmt_gamma)
    #print('hits_elec', hits_gamma)
    
    hits_hist(hits_gamma, hits_elec, bins = 50, xlimit = None, name = 'All', title = 'All')
    hits_hist(hits_gamma_lt100, hits_elec_lt100, bins = 50, xlimit = None, name = 'lt100', title = 'E < 100')
    hits_hist(hits_gamma_12, hits_elec_12, bins = 50, xlimit = (400, 1600), name = '12', title = '100<E<200')
    hits_hist(hits_gamma_23, hits_elec_23, bins = 50, xlimit = (1000, 2400), name = '23', title = '200<E<300')
    hits_hist(hits_gamma_34, hits_elec_34, bins = 50, xlimit = (1500, 3000), name = '34', title = '300<E<400')
    hits_hist(hits_gamma_45, hits_elec_45, bins = 50, xlimit = (1700, 3300), name = '45', title = '400<E<500')
    hits_hist(hits_gamma_56, hits_elec_56, bins = 50, xlimit = (2000, 3600), name = '56', title = '500<E<600')
    hits_hist(hits_gamma_67, hits_elec_67, bins = 50, xlimit = (2300, 4000), name = '67', title = '600<E<700')
    hits_hist(hits_gamma_78, hits_elec_78, bins = 50, xlimit = (3000, 4500), name = '78', title = '700<E<800')
    hits_hist(hits_gamma_89, hits_elec_89, bins = 50, xlimit = (3000, 4500), name = '89', title = '800<E<900')
    hits_hist(hits_gamma_910, hits_elec_910, bins = 50, xlimit = (3500, 5000), name = '910', title = '900<E<1000')
    hits_hist(hits_gamma_gt10, hits_elec_gt10, bins = 50, xlimit = (3500, 6000), name = 'gt10', title = 'E > 1000')
    
    

    #r_dir_gen_elec = r_dir_gen_elec[hits == 0.8]
    #r_dir_gen_gam = r_dir_gen_gam[hits == 0.8]

    towall_gev = temp_towall_gev

    towall_gevlt100 = []
    towall_gev12 = []
    towall_gev23 = []
    towall_gev34 = []
    towall_gev45 = []
    towall_gev56 = []
    towall_gev67 = []
    towall_gev78 = []
    towall_gev89 = []
    towall_gev910 = []
    towall_gevgt100 = []
    

    r_dir_pos_lt100 = []
    r_dir_pos_12 = []
    r_dir_pos_23 = []
    r_dir_pos_34 = []
    r_dir_pos_45 = []
    r_dir_pos_56 = []
    r_dir_pos_67 = []
    r_dir_pos_78 = []
    r_dir_pos_89 = []
    r_dir_pos_910 = []
    r_dir_pos_gt10 = []
    
    r_dir_pos = np.array(r_dir_pos)
    r_dir_elec = np.array(r_dir_elec)
    towall_gev = np.array(towall_gev)
'''
    #print('towall_gev len', (towall_gev))
    towall_gevlt100 = towall_gev[energies < 100]
    towall_gev12 = towall_gev[(energies > 100) & (energies < 200)]
    towall_gev23 = towall_gev[(energies > 200) & (energies < 300)]
    towall_gev34 = towall_gev[(energies > 300) & (energies < 400)]
    towall_gev45 = towall_gev[(energies > 400) & (energies < 500)]
    towall_gev56 = towall_gev[(energies > 500) & (energies < 600)]
    towall_gev67 = towall_gev[(energies > 600) & (energies < 700)]
    towall_gev78 = towall_gev[(energies > 700) & (energies < 800)]
    towall_gev89 = towall_gev[(energies > 800) & (energies < 900)]
    towall_gev910 = towall_gev[(energies > 900) & (energies < 1000)]
    towall_gevgt10 = towall_gev[(energies > 1000)]
    
    r_dir_pos_lt100 = r_dir_pos[energies < 100]
    r_dir_pos_12 = r_dir_pos[(energies > 100) & (energies < 200)]
    r_dir_pos_23 = r_dir_pos[(energies > 200) & (energies < 300)]
    r_dir_pos_34 = r_dir_pos[(energies > 300) & (energies < 400)]
    r_dir_pos_45 = r_dir_pos[(energies > 400) & (energies < 500)]
    r_dir_pos_56 = r_dir_pos[(energies > 500) & (energies < 600)]
    r_dir_pos_67 = r_dir_pos[(energies > 600) & (energies < 700)]
    r_dir_pos_78 = r_dir_pos[(energies > 700) & (energies < 800)]
    r_dir_pos_89 = r_dir_pos[(energies > 800) & (energies < 900)]
    r_dir_pos_910 = r_dir_pos[(energies > 900) & (energies < 1000)]
    r_dir_pos_gt10 = r_dir_pos[(energies > 1000)]

    r_dir_elec_lt100 = r_dir_elec[energies < 100]
    r_dir_elec_12 = r_dir_elec[(energies > 100) & (energies < 200)]
    r_dir_elec_23 = r_dir_elec[(energies > 200) & (energies < 300)]
    r_dir_elec_34 = r_dir_elec[(energies > 300) & (energies < 400)]
    r_dir_elec_45 = r_dir_elec[(energies > 400) & (energies < 500)]
    r_dir_elec_56 = r_dir_elec[(energies > 500) & (energies < 600)]
    r_dir_elec_67 = r_dir_elec[(energies > 600) & (energies < 700)]
    r_dir_elec_78 = r_dir_elec[(energies > 700) & (energies < 800)]
    r_dir_elec_89 = r_dir_elec[(energies > 800) & (energies < 900)]
    r_dir_elec_910 = r_dir_elec[(energies > 900) & (energies < 1000)]
    r_dir_elec_gt10 = r_dir_elec[(energies > 1000)]

    anglelt100 = []
    angle12 = []
    angle23 = []
    angle34 = []
    angle45 = []
    angle56 = []
    angle67 = []
    angle78 = []
    angle89 = []
    angle910 = []
    anglegt10 = []

    for i in range(len(r_dir_pos_lt100)):
        anglelt100.append(angle_try4(r_dir_pos_lt100[i], r_dir_elec_lt100[i]))
    for i in range(len(r_dir_pos_12)):
        angle12.append(angle_try4(r_dir_pos_12[i], r_dir_elec_12[i]))
    for i in range(len(r_dir_pos_23)): 
        angle23.append(angle_try4(r_dir_pos_23[i], r_dir_elec_23[i]))
    for i in range(len(r_dir_pos_34)): 
        angle34.append(angle_try4(r_dir_pos_34[i], r_dir_elec_34[i]))
    for i in range(len(r_dir_pos_45)): 
        angle45.append(angle_try4(r_dir_pos_45[i], r_dir_elec_45[i]))
    for i in range(len(r_dir_pos_56)): 
        angle56.append(angle_try4(r_dir_pos_56[i], r_dir_elec_56[i]))
    for i in range(len(r_dir_pos_67)): 
        angle67.append(angle_try4(r_dir_pos_67[i], r_dir_elec_67[i]))
    for i in range(len(r_dir_pos_78)): 
        angle78.append(angle_try4(r_dir_pos_78[i], r_dir_elec_78[i]))
    for i in range(len(r_dir_pos_89)): 
        angle89.append(angle_try4(r_dir_pos_89[i], r_dir_elec_89[i]))
    for i in range(len(r_dir_pos_910)): 
        angle910.append(angle_try4(r_dir_pos_910[i], r_dir_elec_910[i]))
    for i in range(len(r_dir_pos_gt10)): 
        anglegt10.append(angle_try4(r_dir_pos_gt10[i], r_dir_elec_gt10[i]))
    #print(angle)
    angle_hist(anglelt100, bins = 100, name = 'lt100', title = ' E < 100')
    angle_hist(angle12, bins = 100, name = 12, title = ' E = (100, 200)')
    angle_hist(angle23, bins = 100, name = 23, title = ' E = (200, 300)')
    angle_hist(angle34, bins = 100, name = 34, title = ' E = (300, 400)')
    angle_hist(angle45, bins = 100, name = 45, title = ' E = (400, 500)')
    angle_hist(angle56, bins = 100, name = 56, title = ' E = (500, 600)')
    angle_hist(angle67, bins = 100, name = 67, title = ' E = (600, 700)')
    angle_hist(angle78, bins = 100, name = 78, title = ' E = (700, 800)')
    angle_hist(angle89, bins = 100, name = 89, title = ' E = (800, 900)')
    angle_hist(angle910, bins = 100, name = 910, title = ' E = (900, 1000)')
    angle_hist(anglegt10, bins = 100, name = 'gt10', title = ' E > 1000')

    #print('towall ndim', type(towall_gev))
    
    #print(angle23)
    #print(towall_gev23)

    detector_percentlt100 = detector_percent(towall_gevlt100, anglelt100)
    detector_percent12 = detector_percent(towall_gev12, angle12)
    detector_percent23 = detector_percent(towall_gev23, angle23)
    detector_percent34 = detector_percent(towall_gev34, angle34)
    detector_percent45 = detector_percent(towall_gev45, angle45)
    detector_percent56 = detector_percent(towall_gev56, angle56)
    detector_percent67 = detector_percent(towall_gev67, angle67)
    detector_percent78 = detector_percent(towall_gev78, angle78)
    detector_percent89 = detector_percent(towall_gev89, angle89)
    detector_percent910 = detector_percent(towall_gev910, angle910)
    detector_percentgt10 = detector_percent(towall_gevgt10, anglegt10)
    #print(detector_percentlt100)
    #print(detector_percent)
    #print(distance)
    distance_hist(detector_percentlt100, bins = 100, name = 'lt100', title = ' E < 100')
    distance_hist(detector_percent12, bins = 100, name = 12, title = ' E = (100, 200)')
    distance_hist(detector_percent23, bins = 100, name = 23, title = ' E = (200, 300)')
    distance_hist(detector_percent34, bins = 100, name = 34, title = ' E = (300, 400)')
    distance_hist(detector_percent45, bins = 100, name = 45, title = ' E = (400, 500)')
    distance_hist(detector_percent56, bins = 100, name = 56, title = ' E = (500, 600)')
    distance_hist(detector_percent67, bins = 100, name = 67, title = ' E = (600, 700)')
    distance_hist(detector_percent78, bins = 100, name = 78, title = ' E = (700, 800)')
    distance_hist(detector_percent89, bins = 100, name = 89, title = ' E = (800, 900)')
    distance_hist(detector_percent910, bins = 100, name = 910, title = ' E = (900, 1000)')
    distance_hist(detector_percentgt10, bins = 100, name = 'gt10', title = ' E > 1000')
    '''


    #generic_2D_plot(x_pos,y_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    #generic_2D_plot(x_pos,z_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    #generic_2D_plot(y_pos,z_pos,[-1800,1800], 100, 'Y [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)

    #generic_2D_plot(x_stop_pos,y_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    #generic_2D_plot(x_stop_pos,z_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    #generic_2D_plot(y_stop_pos,z_stop_pos,[-3000,3000], 100, 'Y [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)
    
#    theta = []
#    theta = angle_try2(r_dir_elec, r_dir_pos)

#    x_pos = np.array(x_pos)
#    y_pos = np.array(y_pos)
#    z_pos = np.array(z_pos)
#    angle_pos = np.arctan(x_pos/y_pos)
#    
#    x_pos = list(x_pos)
#    y_pos = list(y_pos)
#    z_pos = list(z_pos)
#    angle_pos = list(angle_pos)
    
 #   generic_det_unraveler(angle_pos, z_pos, np.ones(len(angle_pos)), 'angle [deg]', 'Z [cm]', 'PMT charges', output_path, 'shrunken')

    #print('x_pos = ', x_pos[0:10])
    #print('y_pos = ', y_pos[0:10])
    #print('r_pos = ', r_pos[0:10])

    #generic_3D_plot(x_pos,y_pos,z_pos, np.ones(len(x_pos)), 'X [cm]', 'Y [cm]', 'Z [cm]', 'Arbitrary', output_path, 'truth_position')
    #generic_3D_plot(x_stop_pos,y_stop_pos,z_stop_pos, np.ones(len(x_stop_pos)), 'Stop X [cm]', 'Stop Y [cm]', 'Stop Z [cm]', 'Arbitrary', output_path, 'truth_stop_position')


