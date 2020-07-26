#!/bin/sh

cd CloverLeaf/CloverLeaf_MPI
make clean
if [ `which icc |wc -l` = 1 ]; then
  make COMPILER=INTEL
else
  make COMPILER=GNU
fi

PROB=clover_bm64

sed -e '1,$s/end_step=2955/end_step=500/' InputDecks/$PROB.in > clover.in
mpirun -n 36 --bind-to core ./clover_leaf 2>&1 | tee $PROB.out

likwid-mpirun -np 36 -g MEM_DP ./clover_leaf 2>&1 | tee $PROB_likwid.out

