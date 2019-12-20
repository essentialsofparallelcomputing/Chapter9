CC=nvcc
OPT=-O2


%.o : %.c
	${CC} -c ${OPT} $<

pci_bw : PCI_Bandwidth_Benchmark.o malloc2D.o timer.o
	${CC} ${OPT} $^ -o $@

clean:
	rm -rf *.o
