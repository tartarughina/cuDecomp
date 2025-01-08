#!/bin/bash -l

#PBS -A SEEr-Polaris
#PBS -l walltime=1:00:00
#PBS -l filesystems=home:eagle:grand
#PBS -N c2c_UM_1
#PBS -m bea
#PBS -M rstrin4@uic.edu
#PBS -V
#PBS -l select=1:ncpus=4:ngpus=4
#PBS -r y


export LD_LIBRARY_PATH=$HOME/cuDecomp/lib:$LD_LIBRARY_PATH


module load craype-accel-nvidia80

# Number of GPUs per rank --> 1:1
ngpus=1
# Number of ranks per node
nranks=4
# Medium batch size is the only one picked for multinode tests



# Log dir path
log_path=$HOME/cuDecomp/c2c_log

if [ ! -d "$log_path" ]; then
    mkdir -p "$log_path"
fi

NNODES=$(wc -l < $PBS_NODEFILE)
NTOTRANKS=$(( NNODES * nranks ))

cd $HOME/cuDecomp/bin/benchmark


for size in 256 512 1024; do

for i in {1..10}; do
    mpirun --envall --np "${NTOTRANKS}" --ppn "${nranks}" \
    --hostfile "$PBS_NODEFILE" --cpu-bind list:0,8,16,24 \
    ./benchmark_c2c -b 4 --skip -x ${size} -y ${size} -z ${size} --use-managed-memory > "${log_path}/UM_gpus_${NTOTRANKS}_size_${size}_iter_${i}.txt"
done

done
