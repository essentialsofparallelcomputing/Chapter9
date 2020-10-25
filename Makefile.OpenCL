All: BabelStream_OpenCL Roofline_OpenCL mixbench_OPENCL

.PHONY: BabelStream_OpenCL Roofline_OpenCL mixbench_OPENCL

BabelStream_OpenCL:
	cd BabelStream && make -f OpenCL.make && ./ocl-stream

Roofline_OpenCL:
	cd cs-roofline-toolkit/Empirical_Roofline_Tool-1.1.0 && \
	  cp ../../config.Vega20_gpu Config && \
          2to3 -w ert Python Scripts && \
          sed -i -e 's!len(msec_med)/2!len(msec_med)//2!' Scripts/preprocess.py && \
          sed -i -e "s!subprocess.PIPE!subprocess.PIPE, encoding='utf8'!" Python/ert_utils.py && \
          sed -i -e "/META_DATA/s!\] ==!\].strip() ==!" -e '/len(lines.i/s!\]) ==!\].strip()) ==!' Python/ert_core.py && \
	  ./ert Config/config.Vega20_gpu && \
	  ps2pdf Results.config.V100_gpu/Run.001/roofline.ps && evince roofline.ps

mixbench_OPENCL:
	cd mixbench && make OPENCL_INSTALL_PATH=`oclinfo`/.. && ./mixbench-opencl-ro

clean:
	cd BabelStream; make clean
	cd mixbench; make clean
