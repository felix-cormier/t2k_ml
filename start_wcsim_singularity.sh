module load singularity/3.8
export SINGULARITY_BINDPATH="/scratch/"
singularity run /scratch/ipress/wc_options.pkl
source singularity_script.sh
