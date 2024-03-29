// Copyright 2022 XMOS LIMITED.
// This Software is subject to the terms of the XMOS Public Licence: Version 1.

/*
void i2s_frame_slave_4b_loop_part_2(
    int32_t out_samps[],
    int32_t in_samps[],
    out buffered port:32 ?p_dout,
    in buffered port:32 ?p_din,
    out buffered port:32 p_lrclk
    );
*/

#define NSTACKWORDS     (8)
#define FUNCTION_NAME   i2s_frame_slave_4b_loop_part_2

#define out_array       r0
#define inp_array       r1
#define out_port        r2
#define inp_port        r3
#define lr_clock        r4
#define a               r5
#define b               r6
#define c               r7
#define d               r8
#define e               r9
#define f               r10

.text
.issue_mode dual
.align 4

.cc_top FUNCTION_NAME.function,FUNCTION_NAME

FUNCTION_NAME:
    dualentsp NSTACKWORDS
  // Store registers r4 upwards to the stack.
    stw    lr_clock, sp[0]
    std    a, b, sp[1]
    std    c, d, sp[2]
    std    e, f, sp[3]

  // Retrieve final argument to the function.
    ldw    lr_clock, sp[9]

  // We stashed the 3rd and 4th even samples for transmission earlier.
  // Retrieve these and immediately transmit the 3rd.
  { ldw    b, out_array[2] ;                          }
  { ldw    a, out_array[0] ; out    res[out_port], b  }

  // Output the 4th even sample
  // Load the odd samples we intend to send
  // Input the 1st even sample
  { ldw    d, out_array[7] ;                          }
  { ldw    c, out_array[5] ;                          }
  { ldw    b, out_array[3] ; in     f, res[inp_port]  }
  { ldw    a, out_array[1] ; out    res[out_port], a  }

  // Bit-reverse the odd samples
  { bitrev d, d            ; bitrev c, c              }
  { bitrev b, b            ; bitrev a, a              }

  // Zip the odd samples as required to send in parallel on a 4b port
  // (abcd) (efgh) (ijkl) (mnop) -> aeim bfjn cgko dhlp
    zip    a, c, 0
    zip    b, d, 0
    zip    a, b, 0
    zip    c, d, 0  

  // Output the first two odd samples
  // Input the remaining even samples
  {                        ; in     e, res[inp_port]  }
  {                        ; out    res[out_port], d  }
  {                        ; in     d, res[inp_port]  }
  {                        ; out    res[out_port], c  }
  {                        ; in     c, res[inp_port]  }

  // Unzip the recieved even samples as required
  // aeim bfjn cgko dhlp -> (abcd) (efgh) (ijkl) (mnop)
    unzip  e, f, 0
    unzip  c, d, 0
    unzip  d, f, 0
    unzip  c, e, 0 

  // Bit-reverse and store the recieved even samples. 
  {                        ; bitrev f, f              }
  { stw    f, inp_array[6] ; bitrev e, e              } 
  { stw    e, inp_array[4] ; bitrev d, d              } 
  { stw    d, inp_array[2] ; bitrev c, c              } 
  { stw    c, inp_array[0] ;                          }

  // Output the remaining odd samples. At this point, we have transmitted all
  // 8 samples, and must call the send callback to recieve the next batch.
  // Input the first two odd samples. As we are returning from this function
  // in order to call the send callback, we must store these recieved samples in
  // memory to pick up later.
  // Input value of the lr_clock and return it
  {                        ; out    res[out_port], b  }
  {                        ; in     f, res[inp_port]  }
  { stw    f, inp_array[1] ; out    res[out_port], a  }
  {                        ; in     e, res[inp_port]  }
  { stw    e, inp_array[3] ; in     r0, res[lr_clock] }

  // Restore registers and return.
    ldw    lr_clock, sp[0]
    ldd    a, b, sp[1]
    ldd    c, d, sp[2]
    ldd    e, f, sp[3]
    retsp NSTACKWORDS


.L_func_end:
.cc_bottom FUNCTION_NAME.function

.globl FUNCTION_NAME
.type FUNCTION_NAME,@function
.set FUNCTION_NAME.nstackwords,NSTACKWORDS;  .global FUNCTION_NAME.nstackwords
.set FUNCTION_NAME.maxcores,1;               .global FUNCTION_NAME.maxcores
.set FUNCTION_NAME.maxtimers,0;              .global FUNCTION_NAME.maxtimers
.set FUNCTION_NAME.maxchanends,0;            .global FUNCTION_NAME.maxchanends