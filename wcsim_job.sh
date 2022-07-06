#!/bin/bash
#SBATCH --output=/scratch/fcormier/t2k/ml/output_wcsim/logfiles/%j.out
#SBATCH --error=/scratch/fcormier/t2k/ml/output_wcsim/logfiles/%j.err



if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

__conda_setup="$('/home/fcormier/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/fcormier/miniconda3/etc/profile.d/conda.sh" ]; then
        . "/home/fcormier/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/home/fcormier/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup

conda activate t2k_ml_root_2

/home/fcormier/misc/bashrc

module load singularity/3.8
export SINGULARITY_BINDPATH="/scratch/"
singularity exec /scratch/fcormier/singularity_containers/wcsim.sif bash "/home/fcormier/t2k/t2k_ml_base/t2k_ml/singularity_run.sh"
#bash "/home/fcormier/t2k/t2k_ml_base/t2k_ml/singularity_run.sh"
#python wcsim_batch.py $ARG1 $ARG2
echo "finished wcsim"

source transform_modules.sh
python transform_batch.py $ARG2 $SLURM_JOBID
echo "finished transform"
ls -lhtr

