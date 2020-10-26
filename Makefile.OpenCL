All: BabelStream_OpenCL Roofline_OpenCL mixbench_OPENCL

.PHONY: BabelStream_OpenCL Roofline_OpenCL mixbench_OPENCL

BabelStream_OpenCL:
	cd BabelStream && make -f OpenCL.make && ./ocl-stream

Roofline_OpenCL:
	cd cs-roofline-toolkit/Empirical_Roofline_Tool-1.1.0 && \
	  git clean -fd && git checkout */*.py ert && \
	  cp ../../config.Vega20_gpu Config && \
          2to3 -w ert Python Scripts && \
          sed -i -e 's!len(msec_med)/2!len(msec_med)//2!' Scripts/preprocess.py && \
          sed -i -e "s!subprocess.PIPE!subprocess.PIPE, encoding='utf8'!" Python/ert_utils.py && \
          sed -i -e "/META_DATA/s!\] ==!\].strip() ==!" -e '/len(lines.i/s!\]) ==!\].strip()) ==!' Python/ert_core.py && \
	  ./ert Config/config.Vega20_gpu && \
	  ps2pdf Results.Vega20_gpu/Run.001/roofline.ps && evince roofline.pdf

mixbench_OPENCL:
	cd mixbench/mixbench-opencl && mkdir build && cd build && cmake .. && make && ./mixbench-ocl-ro

clean:
	cd mixbench/mixbench-opencl && rm -rf build
	cd BabelStream; make clean
