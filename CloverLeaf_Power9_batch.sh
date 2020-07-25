#!/bin/sh

cd CloverLeaf/CloverLeaf_CUDA
make clean
make COMPILER=GNU NV_ARCH=VOLTA

PROB=clover_bm64

sed -e '1,$s/end_step=2955/end_step=500/' $PROB.in > clover.in
./clover_leaf 2>&1 | tee $PROB.out

rm gpu_monitoring.log
nvidia-smi dmon -i 0 --select pumct -c 65 --options DT --filename gpu_monitoring.log &
./clover_leaf 2>&1 | tee $PROB.out

#likwid-perfctr -C 0 -g FLOPS_DP ./clover_leaf 2>&1 | tee $PROB_likwid.out

