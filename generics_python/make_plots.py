import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import statistics
import numpy as np

###To make plots




def generic_histogram(x, x_name, output_path, output_name, y_name = None, y_lim = None, y_axis = None, label=None, range=None, bins=None, in_chain=False):
    fig, ax = plt.subplots()
    alpha=1
    if len(x) > 1:
        alpha=0.6
    ax.hist(x, bins=bins, range=range, label=label, alpha=alpha, histtype='stepfilled')
    ax.set_xlabel(x_name)
    if y_lim is not None:
        ax.set_ylim(y_lim)
    if y_axis is not None:
        ax.set_yscale('log')
    if y_name is not None:
        ax.set_ylabel('Counts')
    ax.legend(loc='best')
    ax.grid(linestyle = '--')
    if not in_chain:
        plt.savefig(output_path+'/'+output_name+'.png', format='png', transparent=False)
        plt.close()
        plt.clf()

def generic_histogram2(x, x2, x_name, output_path, output_name, y_name = None, range=None, bins=None, in_chain=False, label1 = None, label2 = None):
    plt.hist(x, bins=bins, range=range, alpha=0.5, histtype='stepfilled', label = label1)
    plt.hist(x2, bins=bins, range=range, alpha=0.5, histtype='stepfilled', label = label2)
    plt.xlabel(x_name)

    y,binEdges = np.histogram(x,bins=bins, range = range)
    bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    menStd     = np.sqrt(y)
    width      = 0.05

    y2,binEdges2 = np.histogram(x2,bins=bins, range = range)
    bincenters2 = 0.5*(binEdges2[1:]+binEdges2[:-1])
    menStd2     = np.sqrt(y2)
    plt.grid(linestyle = '--')

    if y_name is not None:
        plt.ylabel(y_name)
    if not in_chain:
        plt.errorbar(bincenters, y, yerr=menStd, fmt = ' ', label = f'Error in {label1}')
        plt.errorbar(bincenters2, y2, yerr=menStd2, fmt=' ', label = f'Error in {label2}')
        plt.legend(loc = 'best')
        plt.savefig(output_path+'/'+output_name+'.png', format='png', transparent=False)
        plt.close()
        plt.clf()


def generic_histogram_d(x, x_name, output_path, output_name, y_name = None, label=None, range=None, bins=None, in_chain=False):
    fig, ax = plt.subplots()
    alpha=1
    if len(x) > 1:
        alpha=0.6
    ax.hist(x, bins=bins, range=range, label=label, alpha=alpha, histtype='stepfilled')
    ax.set_xlabel(x_name)
    if y_name is not None:
        ax.set_ylabel(y_name)
    ax.legend(loc='best')
    ax.grid(linestyle = '--')

    mean = statistics.mean(x.flatten())
    sd = statistics.stdev(x.flatten())
    plt.axvline(mean, color = 'k', linestyle = '--')
    plt.axvline(mean+(2*sd), color = 'y', linestyle = '--')
    plt.axvline(mean+sd, color = 'y', linestyle = '--')
    plt.text(250, 5000, f'$Mean = $ {np.round(mean,1)} cm', fontsize=14, bbox=dict(alpha=0.5))

    if not in_chain:
        plt.savefig(output_path+'/'+output_name+'.png', format='png', transparent=False)
        plt.close()
        plt.clf()



def generic_histogram_ratio(x, x2, x_name, output_path, output_name, y_name = None,  range=None, label=None, bins=None, in_chain=False, label1 = None, label2 = None):    
    fig, (ax1, ax2) = plt.subplots(2, figsize = (10, 10))

    val_of_bins_x1, edges_of_bins_x1, patches_x1 = ax1.hist(x, bins=bins, range=range,  alpha=0.5, histtype='stepfilled', label = label1)
    val_of_bins_x2, edges_of_bins_x2, patches_x2 = ax1.hist(x2, bins=bins, range=range,  alpha=0.5, histtype='stepfilled', label = label2)
    y,binEdges = np.histogram(x,bins=bins, range = range)
    y2,binEdges2 = np.histogram(x2,bins=bins, range = range)
    
    print(len(x))
    print(len(x2))
    #ax2 = ax1.twinx()
    
    menStd     = np.sqrt(y)
    width      = 0.05   
    
    ax1.set_xlabel(x_name)

    ratio = np.divide(val_of_bins_x1,
                  val_of_bins_x2,
                  where=(val_of_bins_x2 != 0))
    #print("ratio:", ratio)

    error = np.divide(val_of_bins_x1 * np.sqrt(val_of_bins_x2) + val_of_bins_x2 * np.sqrt(val_of_bins_x1),
                  np.power(val_of_bins_x2, 2),
                  where=(val_of_bins_x2 != 0))    
    
    #print("error:", error)
    bincenter = 0.5 * (edges_of_bins_x1[1:] + edges_of_bins_x1[:-1])
    bincenter2 = 0.5 * (edges_of_bins_x2[1:] + edges_of_bins_x2[:-1])
    #bincenters2 = 0.5*(binEdges2[1:]+binEdges2[:-1])
    menStd2     = np.sqrt(y2)
    ax2.errorbar(bincenter, ratio, yerr=error, fmt='.', color='r', label = 'Error in ratio')
    
    ax1.set_ylabel('Counts')
    ax2.set_ylabel('ratio')
    ax2.set_xlim(-2000, 2000)
    ax2.set_ylim(0, 1.5)
    ax1.grid(linestyle = '--')
    ax2.grid(linestyle = '--')
    print(len(x))
    print(len(x2))
    if not in_chain:
        ax1.errorbar(bincenter, y, yerr=menStd, fmt = ' ', label = 'Error in $e^{+}/e^{-}$ production')
        ax1.errorbar(bincenter2, y2, yerr=menStd2, fmt=' ', label = 'Error in generated photon position')
        ax1.legend(loc = 'best')
        ax2.legend(loc = 'best')
        plt.savefig(output_path+'/'+output_name+'.png', format='png', transparent=False)
        plt.close()
        plt.clf()
        


def square(list):
    return [np.power(i, 2) for i in list]


def sqrt(list):
    return [np.sqrt(i) for i in list]

#result = []
def sub(list1, list2):
    return [np.abs(np.array(list1) - np.array(list2))]

#print(result)

def generic_2D_plot(x,y,x_range, x_bins, x_name, y_range, y_bins, y_name, label, output_path, output_name, title = None, normalization=False, weights=None, xLog=False, yLog=False, save_plot=True, return_hist=False):

    fig, ax = plt.subplots()
    hh, xedges, yedges, _ = ax.hist2d(x,y, [x_bins, y_bins], [x_range,y_range], density=normalization, weights=weights , label=label)
    fig.colorbar(_, ax=ax)
    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    if title is not None:
        plt.title = title
    plt.legend()
    if xLog:
        plt.xscale('log', nonposx='clip')
    if yLog:
        plt.yscale('log', nonposy='clip')
    if save_plot:
        plt.savefig(output_path+'/'+output_name+'.png', format='png', transparent=False)


    if return_hist:
        return hh, xedges, yedges

def generic_det_unraveler(x,y,strength, x_label, y_label, strength_label, output_path, output_name):
    fig, ax = plt.subplots()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    p = ax.scatter(x, y, c = strength, cmap = 'plasma', s = 2)
    cbar = fig.colorbar(p, ax=ax)
    ax.grid(linestyle = '--')
    cbar.set_label(strength_label)
    plt.savefig(output_path+'/'+output_name+'.png', format='png', transparent=False)

def generic_3D_plot(x,y,z,strength, x_label, y_label, z_label, strength_label, output_path, output_name):
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
