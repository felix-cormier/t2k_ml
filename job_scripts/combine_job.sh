#!/bin/bash
#SBATCH --output=/scratch/fcormier/t2k/ml/output_skdetsim/logfiles/%j.out
#SBATCH --error=/scratch/fcormier/t2k/ml/output_skdetsim/logfiles/%j.err
#SBATCH -J combination

cd /project/rpp-blairt2k/fcormier/t2k_ml/start_skdetsim/t2k_ml

module load StdEnv/2020
module load python/3.10.2
module load scipy-stack
module load gcc/9.3.0
module load root/6.20.04

source /home/fcormier/ml_root_3p10/bin/activate

export PYTHONPATH=/project/rpp-blairt2k/fcormier/t2k_ml/start_skdetsim/t2k_ml:$PYTHONPATH

echo $PYTHONPATH

python job_scripts/combine_job.py $ARG1 $SLURM_TMPDIR $ARG3
cp $SLURM_TMPDIR/*.hy $ARG2/