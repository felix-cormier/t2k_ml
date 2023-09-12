module load apptainer/1.1.8
export APPTAINER_BINDPATH="/scratch/"
apptainer run /scratch/fcormier/singularity_containers/wcsim.sif
source singularity_script.sh