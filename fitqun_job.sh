#!/bin/bash
#SBATCH --output=/scratch/fcormier/t2k/ml/output_fitqun/logfiles/%j.out
#SBATCH --error=/scratch/fcormier/t2k/ml/output_fitqun/logfiles/%j.err

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

source /home/fcormier/ml_root_3p10/bin/activate

source /project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/setup.sh
/project/rpp-blairt2k/fcormier/skdetsim_szoldosVersion/fitqun/fiTQun/runfiTQun -r data/test_${ARG3}_fitqun.root $ARG1
#bash "/home/fcormier/t2k/t2k_ml_base/t2k_ml/singularity_run.sh"
#python wcsim_batch.py $ARG1 $ARG2
echo "finished fitqun"

export LD_LIBRARY_PATH=$old_LDPATH
export PATH=$old_PATH

source setup.sh

ls -l data/


python fitqun_transform.py "$SLURM_TMPDIR/t2k_ml/data/" $ARG3 $ARG4
echo "finished transform"
cp data/*.hy $ARG2
cp data/*.zbs $ARG2
cp *.card $ARG2
cd $SLURM_TMPDIR
rm -rf t2k_ml/

