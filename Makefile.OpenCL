All: BabelStream_OpenCL Roofline_OpenCL

.PHONY: BabelStream_OpenCL Roofline_OpenCL

BabelStream_OpenCL:
	cd BabelStream && make -f OpenCL.make && ./ocl-stream

Roofline_OpenCL:
	cd cs-roofline-toolkit/Empirical_Roofline_Tool-1.1.0 && \
	   cp ../../config.Vega20_gpu Config && ./ert Config/config.Vega20_gpu && \
	   ps2pdf Results.config.V100_gpu/Run.001/roofline.ps && xpdf roofline.ps

mixbench_OPENCL:
	cd mixbench && make OPENCL_INSTALL_PATH=`oclinfo`/.. && ./mixbench-opencl-ro

clean:
	cd BabelStream; make clean
	cd mixbench; make clean
