#!/bin/bash
#SBATCH --output=/scratch/fcormier/t2k/ml/output_wcsim/logfiles/%j.out
#SBATCH --error=/scratch/fcormier/t2k/ml/output_wcsim/logfiles/%j.err

cp -r ../t2k_ml/ $SLURM_TMPDIR
cd $SLURM_TMPDIR/t2k_ml/
cp $ARG2/sk_options.pkl .
mkdir data/
ls -hltr
pwd

old_PATH=$PATH
old_LDPATH=$LD_LIBRARY_PATH

if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

source /home/fcormier/ml_root_3p10/bin/activate

source /project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/setup.sh
bash $SLURM_TMPDIR/t2k_ml/skdetsim_run.sh
#bash "/home/fcormier/t2k/t2k_ml_base/t2k_ml/singularity_run.sh"
#python wcsim_batch.py $ARG1 $ARG2
echo "finished skdetsim"

export LD_LIBRARY_PATH=$old_LDPATH
export PATH=$old_PATH

module load StdEnv/2020
module load python/3.10.2
module load scipy-stack
module load gcc/9.3.0
module load root/6.20.04

source /home/fcormier/ml_root_3p10/bin/activate

ls -l data/


python transform_batch.py "$SLURM_TMPDIR/t2k_ml/data/" $SLURM_JOBID 1
echo "finished transform"
cp data/*.hy $ARG2
cp data/*.zbs $ARG2
#cp data/*.root $ARG2
cp *.card $ARG2
cd $SLURM_TMPDIR
rm -rf t2k_ml/

