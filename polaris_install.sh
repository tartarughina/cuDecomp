cmake .. \
-DCUDECOMP_BUILD_FORTRAN=OFF \
-DCUDECOMP_BUILD_EXTRAS=ON \
-DCMAKE_INSTALL_PREFIX=/home/tartarughina/cuDecomp \

# To then add UM and UMT
# -DCUDECOMP_ENABLE_UM=ON \
# -DCUDECOMP_ENABLE_UMT=ON \
# The UM will swap within cudecompMalloc the cudaMalloc with the Managed version
# The UMT in this case will add additional MemAdvise within this function and change the code in the examples by adding a Prefetch
