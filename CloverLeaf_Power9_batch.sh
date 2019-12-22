#!/bin/sh

cd CloverLeaf/CloverLeaf_CUDA
make clean
make COMPILER=GNU NV_ARCH=VOLTA

PROB=clover_bm512_short

cp InputDecks/$PROB.in clover.in
./clover_leaf |& tee $PROB.out

likwid-perfctr -C 0 -g FLOPS_DP ./clover_leaf |& tee $PROB_likwid.out

