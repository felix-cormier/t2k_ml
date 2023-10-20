# T2K ML

## Repo to simulate and plot SuperK data for T2K machine learning

### Set-up

To clone the repo

```
git clone https://github.com/felix-cormier/t2k_ml.git
```

Since we're using the WatChMaL _DataTools_ submodule, navigate to the repo directory and initialize the submodule by

```
cd t2k_ml/
git submodule update --init --recursive
```

Once you've cloned the repo and initialized the submodule, there is some setup to do.

If you're using Compute Canada:

```
module load StdEnv/2020
module load python/3.10.2
module load scipy-stack
module load gcc/9.3.0
module load root/6.20.04
virtualenv --no-download ~/ml_root_3p10
source ~/ml_root_3p10/bin/activate
pip install --no-index -r requirements.txt
```

This will install the required packages and virtual environment in your home directory.
You can look here for more details: [Compute Canada Python Install](https://docs.alliancecan.ca/wiki/Python#Requirements_file)
Now every time you log back in, in the top directory of this cloned repo run:

```
source setup.sh
```

### Running on Compute Canada Clusters

Preferably run this code on narval.computecanada.ca by

```
ssh username@narval.computecanada.ca
```

For code editing and light work you can run on the login node. But to run these functions with large amounts of data, you should run it in an interactive batch job. Compute Canada uses the slurm scheduler. To run an interactive batch job, do:


```
srun --mem-per-cpu=4G --nodes=1 --ntasks-per-node=4 --time=08:00:00 --pty bash -i
```

where _mem-per-cpu_ is the amount of memory you request per tasks, _nodes_ is the number of entire nodes you request (usually 1), _ntasks-per-node_ is the number of CPUs per node you request, and _time_ is the maximum amount of time your job will take. You should customize these requests to whatever you think you will need, but this is a good baseline. Once you run this command, your shell will now be running in on of the compute nodes, and you will be able to run cod ehtat uses numerous CPUs and larger amounts of memory.

It is possible that large files will use more memory than allocated. If so, the server will kill the process. You will have to exit the interactive job (Ctrl-D) and rerun the _srun_ command with higher _mem-per-cpu_.



### Runner file

The file _t2k\_ml\_runner.py_ is the steering script for everything that can be done using this repo. It parses _args\_ml.txt_ for arguments on what to run and what directories to look into for input/output data. Possible arguments will be outlined in their respective sections.

#### Running WCSim locally

WCSim simulates a particle and runs it through a Water Cherenkov detector. To keep track of what is being simulated it uses a class called WCSimOptions, which is initialized in _t2k\_ml\_runner.py_. You can change the simulation settings there (e.g. simulate electron (_e-_), muons (_mu-_) or photon (_gamma_)). There are other options in _wcsim\_options.py_, such as output directory. To run this, first one must be in the WCSim singularity container. Run

```
source start_wcsim_singularity.sh
conda activate t2k_ml_root_4
```

In _args\_ml.txt_:

```
--doWCSim
--output_path=[...]
```

where output path is where the .root output from WCSim will be saved. WCSim looks for a _WCSim.mac_ file for the options to run. We edit _WCSim\_toEdit.mac_ file and save it as _WCSim.mac_ to change options for WCSim, this is done in WCSim options class.

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

Where input plot path can be either a directory, or the path and name of a text file which then contains multiple paths and names of files (preferably a combination .hy file). The output path is where the plots generated will be stored. 

N.B. If you want to plot multiple different labels (e.g. electrons and muons) at the same time, this code expects to have these in separate .hy files. You will have to provide a text file with multiple paths and names of the files you want to plot. Thus give _input\_plot\_path_ variable a text file with the paths to the multiple files.

Plotting may take lots of memory if you are plotting PMT variables (time and charge). If you're on compute canada you may need to run it on an interactive job to make sure plotting script doesn't get killed. You can launch an interactive job by e.g.

```
srun --account=rpp-blairt2k --mem-per-cpu=12G --nodes=1 --ntasks-per-node=2 --time=04:00:00 --pty bash -i
```
If you have a different sponsor account you will need to change the _--acount_ value. Once in the interactive job proceed as normal (You will need to run _setup.sh_. This particular line reserves 2 CPUs with 12GB of memory each for 4 hours, so modify as needed.


#### Make flat energy distribution

Re-sample the data to create a flat visible energy distribution. Specifically, this adds a new key called 'keep_event' which is used in code from the t2k_ml_training '--makeIndices' workflow.

```
--makeFlatEnergy
--input_plot_path=[...]
```

Where input plot path can be either a directory, or the path and name of a text file which then contains multiple paths and names of files (preferably a combination .hy file). 


#### Make Visualizations

To make some visuals of some data events, and visuals of simulated particles, do

```
--makeVisualizations
--input_vis_path=[...]
--output_vis_path=[...]
```

where the input path is the path and name of a .hy file (could be individual or combination), and the output path is where the plots will be stored. There is a variable called _num\_visualization_ in _make\_visualizations.py_ which sets how many visualizations to make in the whole file - it will choose random N events to visualize.
