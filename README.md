# Chapter 9 GPU architectures and concepts
This is from Chapter 9 of Parallel and High Performance Computing, Robey and Zamora,
Manning Publications, available at http://manning.com

The book may be obtained at
   http://www.manning.com/?a_aid=ParallelComputingRobey

Copyright 2019-2020 Robert Robey, Yuliana Zamora, and Manning Publications
Emails: brobey@earthlink.net, yzamora215@gmail.com

See License.txt for licensing information.

# Measuring the BabelStream GPU stream benchmark
   Build with make
      cd BabelStream && make -f CUDA.make
   Run with ./cuda-stream
   OpenCL version
      cd BabelStream && make -f OpenCL.make
   Run with
      ./ocl-stream

# Roofline performance model for GPUs
   cd cs-roofline-toolkit/Empirical_Roofline_Tool-1.1.0
   cp ../../config.V100_gpu Config
   Run with 
      ./ert Config/config.V100_gpu
   View results with
      ps2pdf Results.config.Vega20_gpu/Run.001/roofline.ps
      xpdf roofline.pdf
   Radeon card
      cd cs-roofline-toolkit/Empirical_Roofline_Tool-1.1.0
      cp ../../config.Vega20_gpu Config && ./ert Config/config.Vega20_gpu
      ps2pdf Results.config.V100_gpu/Run.001/roofline.ps
      xpdf roofline.ps

# Mixbench performance tool
   cd mixbench && make CUDA_INSTALL_PATH=`nvcc`/..
   Run with
      ./mixbench-cuda-ro
   OpenCL version
      cd mixbench && make OPENCL_INSTALL_PATH=`oclinfo`/..
   Run with
      ./mixbench-opencl-ro

# PCI Bandwidth Benchmark (Book: listing 9.1 - 9.2)
   Build with make
      cd PCI_Bandwidth_Benchmark && make
   Run with
      ./PCI_Bandwidth_Benchmark

# Cloverleaf
   ./CloverLeaf_Ivybridge_batch.sh
   ./CloverLeaf_Skylake_batch.sh
   ./CloverLeaf_Power9_batch.sh

# Power plot (Book: listing 9.3)
   python power_plot.py
