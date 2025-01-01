#!/bin/bash -l

#PBS -A SEEr-Polaris
#PBS -l walltime=1:00:00
#PBS -l filesystems=home:eagle:grand
#PBS -N TG_UM
#PBS -m bea
#PBS -M rstrin4@uic.edu
#PBS -V
#PBS -l select=1:ncpus=4:ngpus=4
#PBS -r y

module load craype-accel-nvidia80

# Number of GPUs per rank --> 1:1
ngpus=1
# Number of ranks per node
nranks=4
# Log dir path
log_path="$HOME/cuDecomp/tg_log"

if [ ! -d "$log_path" ]; then
    mkdir -p "$log_path"
fi

NNODES=$(wc -l < $PBS_NODEFILE)
NTOTRANKS=$(( NNODES * nranks ))

cd $HOME/cuDecomp/bin/examples/cc/taylor_green

# Execute 5 times
for size in 128 256 512;do
    for i in {1..10}; do
        mpirun --envall --np ${NTOTRANKS} --ppn ${nranks} \
            --hostfile $PBS_NODEFILE --cpu-bind list:0,8,16,24 \
            ./tg --skip -n ${size} -u > "${log_path}/UM_gpus_${NTOTRANKS}_size_${size}_iter_${i}.txt"
    done
done
