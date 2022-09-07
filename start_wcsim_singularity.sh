module load singularity/3.8
export SINGULARITY_BINDPATH="/scratch/"
singularity run /scratch/fcormier/singularity_containers/wcsim.sif
source singularity_script.sh