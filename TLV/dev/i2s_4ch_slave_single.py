from TLV320ADC6140_AUG_3 import TLV320ADC6140


def setup_adc(adc):
    # RPI-GPIO enable
    adc.shutdown()
    adc.startup()

    # ADC awake
    adc.sleep()
    adc.wake()

    # Data Format
    adc.set_output_type(protocol="I2S", word_length=32)

    # Output Slot
    adc.set_output_slot(channel=1, output="SDOUT", slot_idx=0)
    adc.set_output_slot(channel=2, output="SDOUT", slot_idx=32)
    adc.set_output_slot(channel=3, output="SDOUT2", slot_idx=0)
    adc.set_output_slot(channel=4, output="SDOUT2", slot_idx=32)

    # Maseter mode setup
    # adc.set_master(samplerate="48kHz", mclk="24.576MHz", ratio_bck_fsync="64")

    # GPIO1 enable
    # adc.set_adc_gpio(mode="MCLK")
    adc.set_adc_gpio(mode="SDOUT2")

    # BIAS for mic and adc
    adc.set_mic_bias(mic_bias="AVDD", adc_vref="2.75V")

    # Input Mode
    adc.set_input(channel=1, in_type="MIC", config="SINGLE", coupling="AC", impedance="2.5", dre_agc="OFF")
    adc.set_input(channel=2, in_type="MIC", config="SINGLE", coupling="AC", impedance="2.5", dre_agc="OFF")
    adc.set_input(channel=3, in_type="MIC", config="SINGLE", coupling="AC", impedance="2.5", dre_agc="OFF")
    adc.set_input(channel=4, in_type="MIC", config="SINGLE", coupling="AC", impedance="2.5", dre_agc="OFF")

    # Gain, unit in db
    adc.set_analog_gain(channel=1, analog_gain_db=12)
    adc.set_analog_gain(channel=2, analog_gain_db=12)
    adc.set_analog_gain(channel=3, analog_gain_db=12)
    adc.set_analog_gain(channel=4, analog_gain_db=12)
    
    # Input channel enable
    adc.set_input_enable(channel_list=[1,2,3,4])

    # Output channel enable
    adc.set_output_enable(channel_list=[1,2,3,4])

    # Set mic bias, adc and pll
    adc.set_power(mic_bias="ON", adc="ON", pll="ON", dyn="OFF")


if __name__ == "__main__":
    # init device with address, range: 0x4c~0x4f
    adc1 = TLV320ADC6140(addr=0x4c)
    setup_adc(adc1)
