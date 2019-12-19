#!/bin/sh
cd mixbench
make clean
make CUDA_INSTALL_PATH=${CUDA_PATH}
#make CUDA_INSTALL_PATH=${CUDA_INSTALL_PATH}
#make CUDA_INSTALL_PATH=${CUDA_PATH}  OCL_LIB_PATH=${CUDA_PATH}/lib64
./mixbench-cuda-ro >& mixbench.out
#./mixbench-ocl-ro >& mixbench.out
cd ..
