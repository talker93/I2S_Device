// Copyright 2019-2021 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.

//This program takes the coeffs for normal mic_array and generates a version for mic_dual
//It removes the repetition which mic_dual inner loop doesn't need and 8-byte aligns them so we can use stdd/ldd.
//Bonus: we also save just over 1kB of memory..

//To make this do:
// cp fir_coefs.xc fir_coefs.c; cc make_mic_dual_stage_3_coefs.c fir_coefs.c; rm fir_coefs.c; ./a.out

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
#include "fir_coefs.h"                    //From lib_mic_array to access const int g_third_stage_div_6_fir[378]

#define NUM_PHASES 6
#define NUM_TAPS 32

int main(void){
  int * phase_coeff_ptrs[NUM_PHASES];

  int final_stage_coeffs_copy[3][32]; 

  //Copy non 8 byte aligned coefficients and setup nice array of pointers for each phase of coefficients
  const size_t phase_coeff_size = (NUM_TAPS * sizeof(int));
  int * g_third_stage_div_6_fir_ptr = (int * )g_third_stage_div_6_fir; 
  phase_coeff_ptrs[0] = (int * )&g_third_stage_div_6_fir_ptr[0 * 63];
  memcpy(&final_stage_coeffs_copy[0], &g_third_stage_div_6_fir_ptr[1 * 63], phase_coeff_size);
  phase_coeff_ptrs[1] = (int * )&final_stage_coeffs_copy[0];
  phase_coeff_ptrs[2] = (int * )&g_third_stage_div_6_fir_ptr[2 * 63];
  memcpy(&final_stage_coeffs_copy[1], &g_third_stage_div_6_fir_ptr[3 * 63], phase_coeff_size);
  phase_coeff_ptrs[3] = (int * )&final_stage_coeffs_copy[1];
  phase_coeff_ptrs[4] = (int * )&g_third_stage_div_6_fir_ptr[4 * 63];
  memcpy(&final_stage_coeffs_copy[2], &g_third_stage_div_6_fir_ptr[5 * 63], phase_coeff_size);
  phase_coeff_ptrs[5] = (int * )&final_stage_coeffs_copy[2];
  //   //for (int i=0; i<6; i++) printf("ptr %d: 0x%p\n", i, phase_coeff_ptrs[i]);

  char array_text[65536] = {0}; //Should only need around 3kB or so but we have loads..
  char tmp[1024];

  time_t timer;
  struct tm* tm_info;
  time(&timer);
  tm_info = localtime(&timer);
  char year[5];
  strftime(year, 5, "%Y", tm_info);
  char copyright_string[52] = {
    47, 47, 32, 67, 111, 112, 121, 114, 105, 103, 104, 116, 32, 40, 99, 41, 32,
    37, 115, 44, 32, 88, 77, 79, 83, 32, 76, 116, 100, 44, 32, 65, 108, 108, 32,
    114, 105, 103, 104, 116, 115, 32, 114, 101, 115, 101, 114, 118, 101, 100, 10,
    0
  };
  sprintf(tmp, copyright_string, year);
  strcat(array_text, tmp);
  strcat(array_text, "// Autogenerated by make_mic_dual_stage_3_coeffs.c\n\n");

  sprintf(tmp, "const int [[aligned(8)]] g_third_stage_div_6_fir_dual[%d] = {\n", NUM_TAPS * NUM_PHASES);

  strcat(array_text, tmp);
  for(int ph=NUM_PHASES-1;ph>=0;ph--){
    sprintf(tmp, "// Phase %d\n", ph);
    strcat(array_text, tmp);
    for(int i=0;i<NUM_TAPS;i++){
      int * ptr = (int *)phase_coeff_ptrs[NUM_PHASES - 1 - ph] + i;
      sprintf(tmp, "0x%08x, ", *ptr);
      strcat(array_text, tmp);
    }
    strcat(array_text,"\n");
  }
  strcat(array_text, "};\n");

  char out_file_name[] = "fir_coefs_dual.xc";
  printf("Writing new copied coeffs to %s\n", out_file_name);

  //write to file
  FILE *fptr;
  fptr = fopen(out_file_name,"wt");
  if(fptr == NULL)
  {
     printf("Error trying to write file %s!", out_file_name);   
     exit(1);             
  }
  fprintf(fptr, "%s", array_text);
  fclose(fptr);

}
