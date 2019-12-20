#include <stdlib.h>
#include "malloc2D.h"

float **malloc2D(int jmax, int imax)
{
   // first allocate a block of memory for the row pointers and the 2D array
   float **x = (float **)malloc(jmax*sizeof(float *) + jmax*imax*sizeof(float));

   // Now assign the start of the block of memory for the 2D array after the row pointers
   x[0] = (float *)x + jmax;

   // Last, assign the memory location to point to for each row pointer
   for (int j = 1; j < jmax; j++) {
      x[j] = x[j-1] + imax;
   }

   return(x);
}
