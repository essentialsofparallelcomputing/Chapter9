#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <assert.h>
#include "timer.h"
#include "malloc2D.h"

void Host_to_Device_Pageable( int N, double *copy_time )
{
   float *x_host, *x_device;
   struct timespec tstart;

// Allocate space for arrays on the CPU
   x_host = (float*)malloc(N*sizeof(float));
   cudaMalloc((void **)&x_device, N*sizeof(float));

   cpu_timer_start(&tstart);
   for(int i = 1; i <= 1000; i++ ){
      cudaMemcpy(x_device, x_host, N*sizeof(float), cudaMemcpyHostToDevice); 
   }
   cudaDeviceSynchronize();

   *copy_time = cpu_timer_stop(tstart)/1000.0;

   free( x_host );
   cudaFree( x_device );
}

void Host_to_Device_Pinned( int N, double *copy_time )
{
   float *x_host, *x_device;
   struct timespec tstart;

// Allocate space for arrays on the CPU
   cudaError_t status = cudaMallocHost((void**)&x_host, N*sizeof(float));
   if (status != cudaSuccess)
         printf("Error allocating pinned host memory\n");
   cudaMalloc((void **)&x_device, N*sizeof(float));

   cpu_timer_start(&tstart);
   for(int i = 1; i <= 1000; i++ ){
      cudaMemcpy(x_device, x_host, N*sizeof(float), cudaMemcpyHostToDevice); 
   }
   cudaDeviceSynchronize();

   *copy_time = cpu_timer_stop(tstart)/1000.0;

   cudaFreeHost( x_host );
   cudaFree( x_device );
}

void H2D_Pageable_Experiments( double **bandwidth, int n_experiments, int max_array_size ){
   long long array_size;
   double copy_time;

   for(int j=0; j<n_experiments; j++){
      array_size = 1;
      for(int i=0; i<max_array_size; i++ ){

         Host_to_Device_Pageable( array_size, &copy_time );

         double byte_size=4.0*array_size;
         bandwidth[j][i] = byte_size/( copy_time*1024.0*1024.0*1024.0 );

         array_size = array_size*2;
      }
   }
}

void H2D_Pinned_Experiments( double **bandwidth, int n_experiments, int max_array_size ){
   long long array_size;
   double copy_time;

   for(int j=0; j<n_experiments; j++){
      array_size = 1;
      for(int i=0; i<max_array_size; i++ ){

         Host_to_Device_Pinned( array_size, &copy_time );

         double byte_size=4.0*array_size;
         bandwidth[j][i] = byte_size/( copy_time*1024.0*1024.0*1024.0 );

         array_size = array_size*2;
      }
   }
}

void Calculate_Mean_and_Variance( double **bandwidth, double *mean_bandwidth, double *variance_bandwidth, int max_array_size, int n_experiments ){

   for(int i=0; i<max_array_size; i++ ){
      mean_bandwidth[i]   = 0.0f;
      variance_bandwidth[i] = 0.0f;
   }

   for(int j=0; j<n_experiments; j++){
      for(int i=0; i<max_array_size; i++ ){
         mean_bandwidth[i] += bandwidth[j][i]/n_experiments;
      }
    }

    for(int j=0; j<n_experiments; j++){
       for(int i=0; i<max_array_size; i++ ){
          variance_bandwidth[i] += (bandwidth[j][i]-mean_bandwidth[i])*(bandwidth[j][i]-mean_bandwidth[i])/n_experiments;
       }
    }
}

void main()
{
   const int max_array_size = 28; // Max array size
   const int n_experiments  =  8; // Number of experiments to base mean and standard deviation on 
   long long array_size;
   double** bandwidth;
   double* mean_bandwidth;
   double* variance_bandwidth;
   FILE   *fp;

   bandwidth          = (double**)malloc2D(n_experiments,max_array_size);
   mean_bandwidth     = (double*)malloc(max_array_size*sizeof(double));
   variance_bandwidth = (double*)malloc(max_array_size*sizeof(double));

   H2D_Pageable_Experiments( bandwidth, n_experiments, max_array_size );    
   Calculate_Mean_and_Variance( bandwidth, mean_bandwidth, variance_bandwidth, max_array_size, n_experiments );

   fp = fopen("h2d_bandwidth_pageable.csv","w");
   printf("h2d_bandwidth_pageable\n");
   array_size=1;
   fprintf( fp, " Array Size (B), Bandwidth Mean (GB/s), Bandwidth Variance (GB/s)\n" );
   printf( " Array Size (B), Bandwidth Mean (GB/s), Bandwidth Variance (GB/s)\n" );
   for(int i=0; i<max_array_size; i++ ){
      double byte_size=4.0*array_size;
      fprintf( fp, " %lf, %lf, %lf\n", byte_size, mean_bandwidth[i], variance_bandwidth[i] );
      printf( " %lf, %lf, %lf\n", byte_size, mean_bandwidth[i], variance_bandwidth[i] );
      array_size=array_size*2;
   }
   fclose( fp );

   H2D_Pinned_Experiments( bandwidth, n_experiments, max_array_size );    
   Calculate_Mean_and_Variance( bandwidth, mean_bandwidth, variance_bandwidth, max_array_size, n_experiments );

   fp = fopen("h2d_bandwidth_pinned.csv","w");
   printf("\nh2d_bandwidth_pinned\n");
   fprintf( fp, " Array Size (B), Bandwidth Mean (GB/s), Bandwidth Variance (GB/s)\n" );
   printf( " Array Size (B), Bandwidth Mean (GB/s), Bandwidth Variance (GB/s)\n" );
   array_size=1;
   for(int i=0; i<max_array_size; i++ ){
      double byte_size=4.0*array_size;
      fprintf( fp, " %lf, %lf, %lf\n", byte_size, mean_bandwidth[i], variance_bandwidth[i] );
      printf( " %lf, %lf, %lf\n", byte_size, mean_bandwidth[i], variance_bandwidth[i] );
      array_size=array_size*2;
   }
   fclose( fp );

   free( bandwidth );
   free( mean_bandwidth );
   free( variance_bandwidth );
}
