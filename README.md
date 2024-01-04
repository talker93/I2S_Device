# What is this for?
This is the code base for the XMOS ADC module.

# What files it contain?
`audiohw_nov_9.xc` is the main program for I2C communications, which is used for ADC/DAC peripheral configuration.
`main_dev` is the core program manipulating most applications, we do nothing except expand the number limit for ADC channels.
`Makefile` and `xua_conf_nov_9.h` is used for configuring modules on/off during compilation. Most of time, modify `Makefile` instead of `xua_conf_nov_9.h` cause the previous one owns higher priority.

