from generics_python.make_plots import generic_histogram, generic_3D_plot, generic_2D_plot
import random
import numpy as np

def decision(probability):
    return random.random() < probability

def load_geofile(geofile_name):

    with np.load(geofile_name) as data:
        return data['position']

def convert_values(geofile,input):
    return [geofile[x] for x in input]


def make_visualizations(h5_file, output_path, decayE_study=False):
    """Make event displays for some events in the input h5_file. Visualizations will be of the PMTs, as well as truth positions
    


    Args:
        h5_file (_type_): File to draw events from
        output_path (_type_): Where to save the plots
    """
    geofile = load_geofile('data/geofile_skdetsim.npz')
    print("Keys: %s" % h5_file.keys())
    print(h5_file['event_hits_index'].shape)
    #How many event displays to make
    num_visualization = 500

    max = h5_file['event_hits_index'].shape[0]

    ratio = num_visualization/max
    random.seed(0)

    x_pos=(np.ravel(h5_file['positions'][:,:,0]))
    y_pos=(np.ravel(h5_file['positions'][:,:,1]))
    z_pos=(np.ravel(h5_file['positions'][:,:,2]))
    x_stop_pos=[]
    y_stop_pos=[]
    z_stop_pos=[]

    maxOverMedian_array = []


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
                times = h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]

                output_name = 'time_dist_'+str(i)
                bin_content, bin_edges = generic_histogram(times, "PMT Time [ns]", output_path, output_name, range=[1500,10000], bins=100, return_bins=True, in_chain=True)
                indices = np.argsort(bin_content)
                sorted_bin_content = bin_content[indices]
                sorted_bin_edges = bin_edges[indices]
                n = len(sorted_bin_content)

                if n % 2 == 1:
                    # Odd number of elements: take the middle one
                    tmp_median = sorted_bin_content[n // 2]
                else:
                    # Even number of elements: take the average of the two middle ones
                    tmp_median = (sorted_bin_content[n // 2 - 1] + sorted_bin_content[n // 2]) / 2
                tmp_max = np.amax(sorted_bin_content)
                tmp_time = sorted_bin_edges[-1]
                label = 'med: '+ str(tmp_median)+ ', max: ' + str(tmp_max)+', time: ' +str(tmp_time)
                maxOverMedian_array.append(tmp_max/tmp_median)
                generic_histogram(times, "PMT Time [ns]", output_path, output_name, range=[1500,10000], bins=100, label=label)
                pmt_positions = np.array(convert_values(geofile,h5_file['hit_pmt'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]))
                x = pmt_positions[:,0]
                y = pmt_positions[:,1]
                z = pmt_positions[:,2]

                '''
                if h5_file['decay_electron_exists'][i] and h5_file['decay_electron_energy'][i] >30:
                    print("DECAY ELECTRON!")
                    output_name = 'decay_electron_time_'+str(i)
                    generic_histogram(h5_file['hit_time'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]], "PMT Time [ns]", output_path, output_name, bins=20, label = f"e time: {h5_file['decay_electron_time'][i]}")
                '''


                output_name = 'digi_500MeV_vis_charge'+str(i)
                generic_3D_plot(x,y,z, charges, 'X [cm]', 'Y [cm]', 'Z [cm]', 'PMT charge', output_path, output_name)
                output_name = 'digi_500MeV_vis_time'+str(i)
                generic_3D_plot(x,y,z, times, 'X [cm]', 'Y [cm]', 'Z [cm]', 'PMT time [ns]', output_path, output_name, vmin=0, vmax=10000)

    if decayE_study:
        output_name = 'maxOverMedian'
        generic_histogram(maxOverMedian_array, "max over median", output_path, output_name, range=[0,100], bins=100, xticks=5)
    
    generic_2D_plot(x_pos,y_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_pos,z_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_pos,z_pos,[-1800,1800], 100, 'Y [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)

    generic_2D_plot(x_stop_pos,y_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_stop_pos,z_stop_pos,[-3000,3000], 100, 'X [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_stop_pos,z_stop_pos,[-3000,3000], 100, 'Y [cm]', [-3000,3000], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)


    generic_3D_plot(x_pos,y_pos,z_pos, np.ones(len(x_pos)), 'X [cm]', 'Y [cm]', 'Z [cm]', 'Arbitrary', output_path, 'truth_position')
    #generic_3D_plot(x_stop_pos,y_stop_pos,z_stop_pos, np.ones(len(x_stop_pos)), 'Stop X [cm]', 'Stop Y [cm]', 'Stop Z [cm]', 'Arbitrary', output_path, 'truth_stop_position')
