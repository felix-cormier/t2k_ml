cd $SLURM_TMPDIR/t2k_ml/

export LD_LIBRARY_PATH=/opt/HyperK/geant4.10.01.p03-install/lib64:/opt/HyperK/geant4.10.01.p03-install/lib64:/opt/HyperK/root/lib:/.singularity.d/libs
export G4LEDATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/G4EMLOW6.41/
export G4LEVELGAMMADATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/PhotonEvaporation3.1
export G4SAIDXSDATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/G4SAIDDATA1.1
export G4NEUTRONXSDATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/G4NEUTRONXS1.4
export G4NEUTRONHPDATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/G4NDL4.5
export G4PIIDATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/G4PII1.3
export G4RADIOACTIVEDATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/RadioactiveDecay4.2
export G4REALSURFACEDATA=/opt/HyperK/geant4.10.01.p03-install/share/Geant4-10.1.3/data/RealSurface1.0

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
python wcsim_batch.py $ARG1 "$SLURM_TMPDIR/t2k_ml/data/" $SLURM_JOBID