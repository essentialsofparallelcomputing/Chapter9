#!/bin/sh

cd CloverLeaf/CloverLeaf_MPI
make clean
if [ `which icc |wc -l` = 1 ]; then
  make COMPILER=INTEL
else
  make COMPILER=GNU
fi
NUM_CPUS=36
AVAIL_CPUS=`grep '^CPUS' | cut -d'\t' -f1`
if [ ${AVAIL_CPUS} -lt ${NUM_CPUS} ]; then
   NUM_CPUS=${AVAIL_CPUS}
fi

PROB=clover_bm64

sed -e '1,$s/end_step=2955/end_step=500/' InputDecks/$PROB.in > clover.in
mpirun -n ${NUM_CPUS} --bind-to core ./clover_leaf 2>&1 | tee $PROB.out

#likwid-mpirun -np ${NUM_CPUS} -g MEM_DP ./clover_leaf 2>&1 | tee $PROB_likwid.out

