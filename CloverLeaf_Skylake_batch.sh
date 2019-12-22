#!/bin/sh

cd CloverLeaf/CloverLeaf_MPI
make clean
make COMPILER=INTEL

PROB=clover_bm64

sed -e '1,$s/end_step=2955/end_step=500/' InputDecks/$PROB.in > clover.in
mpirun -n 36 --bind-to core ./clover_leaf |& tee $PROB.out

likwid-mpirun -np 36 -g MEM_DP ./clover_leaf |& tee $PROB_likwid.out

