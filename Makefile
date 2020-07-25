#All: Makefile.CUDA Makefile.OpenCL CloverLeaf_Ivybridge CloverLeaf_Skylake
All: CloverLeaf_Ivybridge CloverLeaf_Skylake

.PHONY: Makefile.CUDA Makefile.OpenCL

Makefile.CUDA:
	make -f Makefile.CUDA

Makefile.OpenCL:
	make -f Makefile.OpenCL

CloverLeaf_Ivybridge:
	./CloverLeaf_Ivybridge_batch.sh

CloverLeaf_Skylake:
	./CloverLeaf_Skylake_batch.sh

clean:
	make -f Makefile.CUDA clean
	make -f Makefile.OpenCL clean
