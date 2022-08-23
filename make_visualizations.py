from generics_python.make_plots import generic_3D_plot, generic_2D_plot
import random
import numpy as np

def decision(probability):
    return random.random() < probability


def make_visualizations(h5_file, output_path):
    print("Keys: %s" % h5_file.keys())
    print(h5_file['event_hits_index'].shape)
    num_visualization = 50

    max = h5_file['event_hits_index'].shape[0]

    ratio = num_visualization/max
    random.seed(1)

    x_pos=[]
    y_pos=[]
    z_pos=[]

    for i,index in enumerate(h5_file['event_hits_index']):
        if i < max-1:
            x_pos.append(float(h5_file['positions'][i][:,0])) 
            y_pos.append(float(h5_file['positions'][i][:,1])) 
            z_pos.append(float(h5_file['positions'][i][:,2])) 
            if decision(ratio) and (h5_file['event_hits_index'][i+1]- h5_file['event_hits_index'][i])> 0:
                charges = h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]
                x = h5_file['hit_pmt_pos'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]][:,0]
                y = h5_file['hit_pmt_pos'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]][:,1]
                z = h5_file['hit_pmt_pos'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]][:,2]


                output_name = 'digi_500MeV_vis_'+str(i)
                generic_3D_plot(x,y,z, charges, 'X [cm]', 'Y [cm]', 'Z [cm]', 'PMT charge', output_path, output_name)
    
    generic_2D_plot(x_pos,y_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Y [cm]', '', output_path, 'radial', save_plot=True)
    generic_2D_plot(x_pos,z_pos,[-1800,1800], 100, 'X [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_x', save_plot=True)
    generic_2D_plot(y_pos,z_pos,[-1800,1800], 100, 'Y [cm]', [-1800,1800], 100, 'Z [cm]', '', output_path, 'long_y', save_plot=True)
    print(len(x_pos))
    generic_3D_plot(x_pos,y_pos,z_pos, np.ones(len(x_pos)), 'X [cm]', 'Y [cm]', 'Z [cm]', 'Arbitrary', output_path, 'truth_position')