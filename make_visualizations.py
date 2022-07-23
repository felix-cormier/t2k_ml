from generics_python.make_plots import generic_3D_plot
import random

def decision(probability):
    return random.random() < probability


def make_visualizations(h5_file, output_path):
    print("Keys: %s" % h5_file.keys())
    print(h5_file['event_hits_index'].shape)
    num_visualization = 10

    max = h5_file['event_hits_index'].shape[0]

    ratio = num_visualization/max
    random.seed(1)

    for i,index in enumerate(h5_file['event_hits_index']):
        if i < max-1:
            if decision(ratio) or i == 18824:
                charges = h5_file['hit_charge'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]]
                x = h5_file['hit_pmt_pos'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]][:,0]
                y = h5_file['hit_pmt_pos'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]][:,1]
                z = h5_file['hit_pmt_pos'][h5_file['event_hits_index'][i]:h5_file['event_hits_index'][i+1]][:,2]
                output_name = 'digi_500MeV_vis_'+str(i)
                generic_3D_plot(x,y,z, charges, 'X', 'Y', 'Z', 'PMT charge', output_path, output_name)