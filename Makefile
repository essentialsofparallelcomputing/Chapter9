All: Makefile.CUDA Makefile.OpenCL

.PHONY: Makefile.CUDA Makefile.OpenCL

Makefile.CUDA:
	make -f Makefile.CUDA

Makefile.OpenCL:
	make -f Makefile.OpenCL

clean:
	make -f Makefile.CUDA clean
	make -f Makefile.OpenCL clean
