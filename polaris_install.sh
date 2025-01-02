module load craype-accel-nvidia80

mkdir build

cd build

cmake .. \
-DCUDECOMP_BUILD_FORTRAN=OFF \
-DCUDECOMP_BUILD_EXTRAS=ON \
-DCUDECOMP_ENABLE_NVSHMEM=OFF \
-DCMAKE_INSTALL_PREFIX=$HOME/cuDecomp

cmake --build .
cmake --install .
