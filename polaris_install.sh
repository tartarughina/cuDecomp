module load craype-accel-nvidia80

cmake .. \
-DCUDECOMP_BUILD_FORTRAN=OFF \
-DCUDECOMP_BUILD_EXTRAS=ON \
-DCUDECOMP_ENABLE_NVSHMEM=OFF \
-DCMAKE_INSTALL_PREFIX=/home/tartarughina/test/cuDecomp

# UM and Tuning are all implemented as cli parameters there's no need to use preprocessing
# For the multinode runs of Taylor-Green the process, after the successful initialization of NCCL, hangs during the trnaspose autotuning
# CUDECOMP: Running transpose autotuning...
# CUDECOMP:	grid: 8 x 1, backend: NCCL
# CUDECOMP:	Total time min/max/avg/std [ms]: 8.199168/31.298561/16.058521/4.876711
# CUDECOMP:	           min/max/avg/std [ms]: 8.199168/31.298561/16.058521/4.8CCL INFO NET/OFI Libfabric provider associates MRs with endpoints
# Hangs indefinitely
