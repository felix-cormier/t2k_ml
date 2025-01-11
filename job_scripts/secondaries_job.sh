#!/bin/bash
#SBATCH --output=/scratch/fcormier/t2k/ml/output_secondaries/logfiles/%j.out
#SBATCH --error=/scratch/fcormier/t2k/ml/output_secondaries/logfiles/%j.err

cp -r ../t2k_ml/ $SLURM_TMPDIR
cd $SLURM_TMPDIR/t2k_ml/
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

module load StdEnv/2020
module load python/3.10.2
module load scipy-stack
module load gcc/9.3.0
module load root/6.20.04

source /home/fcormier/ml_root_3p10/bin/activate

ls -l data/


python secondaries_batch.py $ARG1 $ARG2 $ARG3 
echo "finished transform"
cp data/*.hy $ARG2

