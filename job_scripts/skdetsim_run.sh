cd $SLURM_TMPDIR/t2k_ml/


if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

python skdetsim_batch.py $ARG1 "$SLURM_TMPDIR/t2k_ml/data/" $SLURM_JOBID