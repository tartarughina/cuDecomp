#!/bin/bash -l

#PBS -A SEEr-Polaris
#PBS -l walltime=1:00:00
#PBS -l filesystems=home:eagle:grand
#PBS -N BENCH_noUM_2
#PBS -m bea
#PBS -M rstrin4@uic.edu
#PBS -V
#PBS -l select=2:ncpus=4:ngpus=4
#PBS -r y

export NCCL_NET_GDR_LEVEL=PHB
export NCCL_CROSS_NIC=1
export NCCL_COLLNET_ENABLE=1
export NCCL_NET="AWS Libfabric"
export LD_LIBRARY_PATH=/home/tartarughina/cuDecomp/lib:/soft/libraries/hwloc/lib:/soft/libraries/aws-ofi-nccl/v1.9.1-aws/lib:$LD_LIBRARY_PATH
export FI_CXI_DISABLE_HOST_REGISTER=1
export FI_MR_CACHE_MONITOR=userfaultfd
export FI_CXI_DEFAULT_CQ_SIZE=131072

# Number of GPUs per rank --> 1:1
ngpus=1
# Number of ranks per node
nranks=4
# Medium batch size is the only one picked for multinode tests
size=512
# Log dir path
log_path="$HOME/cuDecomp/bench_log"

if [ ! -d "$log_path" ]; then
    mkdir -p "$log_path"
fi

NNODES=$(wc -l < $PBS_NODEFILE)
NTOTRANKS=$(( NNODES * nranks ))

cd $HOME/cuDecomp/bin/benchmark

# Execute 5 times
for i in {1..10}; do
    mpirun --envall --np "${NTOTRANKS}" --ppn "${nranks}" --hostfile "$PBS_NODEFILE" --cpu-bind list:0,8,16,24 ./benchmark_c2c -b 4 -x ${size} -y ${size} -z ${size} > "${log_path}/noUM_gpus_${NTOTRANKS}_size_${size}_iter_${i}.txt"
done
