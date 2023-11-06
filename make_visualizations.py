from generics_python.make_plots import generic_histogram, generic_3D_plot, generic_2D_plot
import random
import numpy as np
import matplotlib.pyplot as plt
from plot_wcsim import calculate_wcsim_wall_variables, load_geofile, convert_values, convert_label, get_cherenkov_threshold

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

    ratio = num_visualization/max
    random.seed(0)

    x_pos=(np.ravel(h5_file['positions'][:,:,0]))
    y_pos=(np.ravel(h5_file['positions'][:,:,1]))
    z_pos=(np.ravel(h5_file['positions'][:,:,2]))
    x_stop_pos=[]
    y_stop_pos=[]
    z_stop_pos=[]


    for i,index in enumerate(h5_file['event_hits_index']):
        if i < max-1:
            #x_pos.append(float(h5_file['positions'][i][:,0])) 
            #y_pos.append(float(h5_file['positions'][i][:,1])) 
            #z_pos.append(float(h5_file['positions'][i][:,2])) 
            #x_stop_pos.append(float(h5_file['stop_positions'][i][:,0])) 
            #y_stop_pos.append(float(h5_file['stop_positions'][i][:,1])) 
            #z_stop_pos.append(float(h5_file['stop_positions'][i][:,2])) 
            if decision(ratio) and (h5_file['event_hits_index'][i+1]- h5_file['event_hits_index'][i])> 0:
                print(i)
                print(h5_file['labels'][i])
                charges = h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]
                pmt_positions = np.array(convert_values(geofile,h5_file['hit_pmt'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                x = pmt_positions[:,0]
                y = pmt_positions[:,1]
                z = pmt_positions[:,2]

                if h5_file['decay_electron_exists'][i] and h5_file['decay_electron_energy'][i] >30:
                    print("DECAY ELECTRON!")
                    output_name = 'decay_electron_time_'+str(i)
                    generic_histogram(h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]], "PMT Time [ns]", output_path, output_name, bins=20, label = f"e time: {h5_file['decay_electron_time'][i]}")


                output_name = 'digi_500MeV_vis_'+str(i)
                generic_3D_plot(x,y,z, charges, 'X [cm]', 'Y [cm]', 'Z [cm]', 'PMT charge', output_path, output_name)
    
    generic_2D_plot(x_pos,y_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_pos,z_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_pos,z_pos,[-1800,1800], 100, 'Y [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)

    generic_2D_plot(x_stop_pos,y_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_stop_pos,z_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_stop_pos,z_stop_pos,[-3000,3000], 100, 'Y [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)

    generic_3D_plot(x_pos,y_pos,z_pos, np.ones(len(x_pos)), 'X [cm]', 'Y [cm]', 'Z [cm]', 'Arbitrary', output_path, 'truth_position')
    #generic_3D_plot(x_stop_pos,y_stop_pos,z_stop_pos, np.ones(len(x_stop_pos)), 'Stop X [cm]', 'Stop Y [cm]', 'Stop Z [cm]', 'Arbitrary', output_path, 'truth_stop_position')

def vis_pmt_charge(x,y,z,strength, x_label, y_label, z_label, strength_label, output_path, output_name):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    p = ax.scatter3D(x, y, z, c=strength, cmap='plasma', s=2)
    ax.set_box_aspect([np.ptp(i) for i in [x,y,z]])
    cbar = fig.colorbar(p, ax=ax)
    cbar.set_label(strength_label)
    plt.savefig(output_path+'/'+output_name+'.png', format='png', transparent=False)
    # from generic_3D_plot(

def make_visualizations_lowWall(h5_file, output_path):
    """
    """
    geofile = load_geofile('data/geofile.npz')
    print("Keys: %s" % h5_file.keys())
    print(h5_file['event_hits_index'].shape)
    #How many event displays to make
    num_visualization = 50

    max = h5_file['event_hits_index'].shape[0]

    ratio = num_visualization/max
    random.seed(0)

    x_pos=(np.ravel(h5_file['positions'][:,:,0]))
    y_pos=(np.ravel(h5_file['positions'][:,:,1]))
    z_pos=(np.ravel(h5_file['positions'][:,:,2]))
    x_stop_pos=[]
    y_stop_pos=[]
    z_stop_pos=[]


    wall_vars = list(map(calculate_wcsim_wall_variables,np.array(h5_file['positions']), np.array(h5_file['directions'])))
    wall_vars = list(zip(*wall_vars))
    wall = wall_vars[0]
    towall = wall_vars[1]
    temp_num_pmt = np.subtract(np.ravel(h5_file['event_hits_index']), np.insert(np.delete(np.ravel(h5_file['event_hits_index']), -1),0,0))

    for i,index in enumerate(h5_file['event_hits_index']):

        if temp_num_pmt[i] > 1000 and towall[i] < 20: 
        # none found in this if h5_file['event_hits_index'][i] > 3000 and towall[i] < 10 and  wall[i] < 10: # need to calcualte these correctly? save in new file?
            # SAVE THE WALL INFO ON THE PLOT
            print('found one, plotting....')
            if True: # i < max-1:
                #x_pos.append(float(h5_file['positions'][i][:,0])) 
                #y_pos.append(float(h5_file['positions'][i][:,1])) 
                #z_pos.append(float(h5_file['positions'][i][:,2])) 
                #x_stop_pos.append(float(h5_file['stop_positions'][i][:,0])) 
                #y_stop_pos.append(float(h5_file['stop_positions'][i][:,1])) 
                #z_stop_pos.append(float(h5_file['stop_positions'][i][:,2])) 
                # ask what line below here means
                #if decision(ratio) and (h5_file['event_hits_index'][i+1]- h5_file['event_hits_index'][i])> 0: # towall is in dir its going, dwall is distance to nearest wall
                if True:
                    #print(i)
                    print(h5_file['labels'][i])
                    charges = h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]
                    pmt_positions = np.array(convert_values(geofile,h5_file['hit_pmt'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                    x = pmt_positions[:,0]
                    y = pmt_positions[:,1]
                    z = pmt_positions[:,2]

                    if h5_file['decay_electron_exists'][i] and h5_file['decay_electron_energy'][i] >30:
                        print("DECAY ELECTRON!")
                        output_name = 'decay_electron_time_'+str(i)
                        generic_histogram(h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]], "PMT Time [ns]", output_path, output_name, bins=20, label = f"e time: {h5_file['decay_electron_time'][i]}")


                    output_name = 'digi_500MeV_vis_'+str(i) # should save more than one here
                    print('saving to ', output_name)
                    vis_pmt_charge(x,y,z, charges, 'X [cm]', 'Y [cm]', 'Z [cm]', 'PMT charge', output_path, output_name)
    
    generic_2D_plot(x_pos,y_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_pos,z_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_pos,z_pos,[-1800,1800], 100, 'Y [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)

    generic_2D_plot(x_stop_pos,y_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_stop_pos,z_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_stop_pos,z_stop_pos,[-3000,3000], 100, 'Y [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)

    generic_3D_plot(x_pos,y_pos,z_pos, np.ones(len(x_pos)), 'X [cm]', 'Y [cm]', 'Z [cm]', 'Arbitrary', output_path, 'truth_position')
    #generic_3D_plot(x_stop_pos,y_stop_pos,z_stop_pos, np.ones(len(x_stop_pos)), 'Stop X [cm]', 'Stop Y [cm]', 'Stop Z [cm]', 'Arbitrary', output_path, 'truth_stop_position')