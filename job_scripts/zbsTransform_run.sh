cd $SLURM_TMPDIR/t2k_ml/


if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

python job_scripts/zbsTransform_batch.py $ARG1 "$SLURM_TMPDIR/t2k_ml/data/"