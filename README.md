# T2K ML

## Repo to simulate and plot SuperK data for T2K machine learning

### Set-up

Once you've cloned the directory, there is some setup to do.

You want to use anaconda to install some packages. Make a folder in your home directory (e.g. miniconda), navigate to it,  and run

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh 
```

This will download and install miniconda, with prompts to decide where to install. To load the conda environment used here, simply navigate to the top directory of the repo and run

```
conda env create --file=t2k_ml_root_4.yml
conda activate t2k_ml_root_4
```

This conda environment should give you access to most libraries needed in this repo.


### Runner file

The file _t2k\_ml\_runner.py_ is the steering script for everything that can be done using this repo. It parses _args\_ml.txt_ for arguments on what to run and what directories to look into for input/output data. Possible arguments will be outlined in their respective sections.

#### Running WCSim locally

WCSim simulates a particle and runs it through a Water Cherenkov detector. To keep track of what is being simulated it uses a class called WCSimOptions, which is initialized in _t2k\_ml\_runner.py_. You can change the simulation settings there (e.g. simulate electron (_e-_), muons (_mu-_) or photon (_gamma_)). There are other options in _wcsim\_options.py_, such as output directory. To run this, in _args\_ml.txt_:

```
--doWCSim
--output_path=[...]
```

where output path is where the .root output from WCSim will be saved.

#### Transforming WCSim .root output to h5py file format

This uses the DataTools submodule taken from the WatChMaL group. The .root -> h5py is done in one step. To run this, in _args\_ml.txt:

```
--doTransform
--transformPath=[...]
--transformName=[...]
```

Where transform path tells the code where to look for the .root file, and the transform name tells the name of the rootfile to transform

#### Batch jobs for doing a joint WCSim simulation and transform to hyp5 format

Batch jobs serve to send many simulations at once, using the slurm scheduler on Compute Canada cluster. If you are running this on a different type of cluster, you will have to change some of the commands to match your scheduler. To run this, you must include all commands below:

```
--doWCSim
--doTransform
--doBatch
--numJobs=#
--eventsPerJob=#
--output_path=[...]
```

where number of jobs is the number of jobs to be sent to the scheduler, and events per Job is how many will be simulated. Total number of events you will get is thus `numJobs*eventsPerJob`. Output path is where all the hyp5 files from jobs will be sent to, as well as a file which shows which wcsim options were used for the job.

#### Look at saved options

Batch jobs save the WCSimOptions used as _wcsim\_options.pkl_. To read these out, run

```
--dumpOptions
--inputPlotPath=[...]
```

where _input\_plot\_path_ is the path and name of a text file containing paths for WCSimOptions files youw ant to read out. Right now this code is bare-bones and only prints out the particle simualated, but could be expanded based on user's needs.

#### Combine h5py files

You can use this to combine a directory of hypy (.hy) files to one large h5py file. Simply do

```
--doCombination
--input_combination_path=[...]
--output_combination_path=[...]
```

Where the input path is a path to a directory where the .hy files to be merged are, and output path is where the combination output file should be saved to. In _t2k\_ml\_runner.py_, in the line for doing combination, the third options is a common string it will look for in all files to combine. In practice this will usually be 'digi'.

#### Plot input variables

You can plot some of the variables from a WCSim transformed .hy file. To do this use

```
--makeInputPlots
--input_plot_path=[...]
--output_plot_path=[...]
```

Where input plot path can be either a directory, or the path and name of a file which then contains multiple paths and names of files (preferably a combination .hy file). The output path is where the plots generated will be stored. N.B. there is an artificial limit of 5000 on the number of events looked at for each .hy file to speed this up.

#### Make Visualizations

To make some visuals of some data events, and visuals of simulated particles, do

```
--makeVisualizations
--input_vis_path=[...]
--output_vis_path=[...]
```

where the input path is the path and name of a .hy file (could be individual or combination), and the output path is where the plots will be stored.