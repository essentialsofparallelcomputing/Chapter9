#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <cuda.h>
#include <cuda_runtime.h>
#include <assert.h>
#include "timer.h"

void Host_to_Device_Pageable( int N, double *copy_time )
{
   float *x_host, *x_device;
   long long i;
   struct timespec tstart;

// Allocate space for an array on the CPU
   x_host = (float*)malloc(N*sizeof(float));
// Allocate space for an array on the GPU
   cudaMalloc((void **)&x_device, N*sizeof(float));

   cpu_timer_start(&tstart);
   for( i = 1; i <= 1000; i++ ){
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
   long long i;
   struct timespec tstart;

// Allocate space for an array on the CPU
   cudaError_t status = cudaMallocHost((void**)&x_host, N*sizeof(float));
   if (status != cudaSuccess)
         printf("Error allocating pinned host memory\n");
// Allocate space for an array on the GPU
   cudaMalloc((void **)&x_device, N*sizeof(float));

   cpu_timer_start(&tstart);
   for( i = 1; i <= 1000; i++ ){
      cudaMemcpy(x_device, x_host, N*sizeof(float), cudaMemcpyHostToDevice); 
   }
   cudaDeviceSynchronize();

   *copy_time = cpu_timer_stop(tstart)/1000.0;

   cudaFreeHost( x_host );
   cudaFree( x_device );
}

void H2D_Pageable_Experiments( float *bandwidth, int n_experiments, int max_array_size ){
   int i, j;
   long long array_size;
   float byte_size;
   double copy_time;

   for( j=0; j<n_experiments; j++){
      array_size = 1;
      for( i=0; i<max_array_size; i++ ){

         Host_to_Device_Pageable( array_size, &copy_time );

         byte_size=4.0f*array_size;
         bandwidth[i+j*max_array_size] = byte_size/( copy_time*1024.0f*1024.0f*1024.0f );

         array_size = array_size*2;
      }
   }
}

void H2D_Pinned_Experiments( float *bandwidth, int n_experiments, int max_array_size ){
   int i, j;
   long long array_size;
   float byte_size;
   double copy_time;

   for( j=0; j<n_experiments; j++){
      array_size = 1;
      for( i=0; i<max_array_size; i++ ){

         Host_to_Device_Pinned( array_size, &copy_time );

         byte_size=4.0f*array_size;
         bandwidth[i+j*max_array_size] = byte_size/( copy_time*1024.0f*1024.0f*1024.0f );

         array_size = array_size*2;
      }
   }
}

void Calculate_Mean_and_Variance( float *bandwidth, float *mean_bandwidth, float *variance_bandwidth, int max_array_size, int n_experiments ){
   int i, j;

   for( i=0; i<max_array_size; i++ ){
      mean_bandwidth[i]   = 0.0f;
      variance_bandwidth[i] = 0.0f;
   }

   for( j=0; j<n_experiments; j++){
      for( i=0; i<max_array_size; i++ ){
         mean_bandwidth[i] += bandwidth[i+j*max_array_size]/n_experiments;
      }
    }

    for( j=0; j<n_experiments; j++){
       for( i=0; i<max_array_size; i++ ){
          variance_bandwidth[i] += (bandwidth[i+j*max_array_size]-mean_bandwidth[i])*(bandwidth[i+j*max_array_size]-mean_bandwidth[i])/n_experiments;
       }
    }
}

void main()
{
   const int max_array_size = 20; // Max array size
   const int n_experiments  =  2; // Number of experiments to base mean and standard deviation on 
   long long array_size;
   int i;
   float byte_size;
   float* bandwidth;
   float* mean_bandwidth;
   float* variance_bandwidth;
   FILE   *fp;

   bandwidth          = (float*)malloc(n_experiments*max_array_size*sizeof(float));
   mean_bandwidth     = (float*)malloc(max_array_size*sizeof(float));
   variance_bandwidth = (float*)malloc(max_array_size*sizeof(float));

   H2D_Pageable_Experiments( bandwidth, n_experiments, max_array_size );    
   Calculate_Mean_and_Variance( bandwidth, mean_bandwidth, variance_bandwidth, max_array_size, n_experiments );

   fp = fopen("h2d_bandwidth_pageable.csv","w");
   array_size=1;
   fprintf( fp, " Array Size (B), Bandwidth Mean (GB/s), Bandwidth Variance (GB/s)\n" );
   for( i=0; i<max_array_size; i++ ){
      byte_size=4.0f*array_size;
      fprintf( fp, " %f, %f, %f\n", byte_size, mean_bandwidth[i], variance_bandwidth[i] );
      array_size=array_size*2;
   }
   fclose( fp );

   H2D_Pinned_Experiments( bandwidth, n_experiments, max_array_size );    
   Calculate_Mean_and_Variance( bandwidth, mean_bandwidth, variance_bandwidth, max_array_size, n_experiments );

   fp = fopen("h2d_bandwidth_pinned.csv","w");
   fprintf( fp, " Array Size (B), Bandwidth Mean (GB/s), Bandwidth Variance (GB/s)\n" );
   array_size=1;
   for( i=0; i<max_array_size; i++ ){
      byte_size=4.0f*array_size;
      fprintf( fp, " %f, %f, %f\n", byte_size, mean_bandwidth[i], variance_bandwidth[i] );
      array_size=array_size*2;
   }
   fclose( fp );

   free( bandwidth );
   free( mean_bandwidth );
   free( variance_bandwidth );
}
