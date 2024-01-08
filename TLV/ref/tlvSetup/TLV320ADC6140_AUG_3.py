import RPi.GPIO as GPIO
from smbus import SMBus
import time

class TLV320ADC6140:
    # init default values
    # bus_num: i2c bus number
    # addr: i2c address, normally 0x4c
    def __init__(self, bus_num=1, addr=0x4c, standby_pin=4):
        # i2c connection init
        self.bus_num = bus_num
        self.addr = addr
        self.bus = SMBus(self.bus_num)

        # RaspberryPi GPIO init
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.standby_pin = standby_pin
        GPIO.setup(self.standby_pin, GPIO.OUT)

        # register map init
        self.reg_mp = {
            "PAGE_CFG" : 0x00,
            "SW_RESET" : 0x01,
            "SLEEP_CFG" : 0x02,
            "SHDN_CFG" : 0x05,
            "ASI_CFG0" : 0x07,
            "ASI_CFG1" : 0x08,
            "ASI_CFG2" : 0x09,
            "ASI_CH1" : 0x0b,
            "ASI_CH2" : 0x0c,
            "ASI_CH3" : 0x0d,
            "ASI_CH4" : 0x0e,
            "ASI_CH5" : 0x0f,
            "ASI_CH6" : 0x10,
            "ASI_CH7" : 0x11,
            "ASI_CH8" : 0x12,
            "MST_CFG0" : 0x13,
            "MST_CFG1" : 0x14,
            "ASI_STS" : 0x15,
            "CLK_SRC" : 0x16,
            "PDMCLK_CFG" : 0x1f,
            "PDMIN_CFG" : 0x20,
            "GPIO_CFG0" : 0x21,
            "GPO_CFG0" : 0x22,
            "GPO_CFG1" : 0x23,
            "GPO_CFG2" : 0x24,
            "GPO_CFG3" : 0x25,
            "GPO_VAL" : 0x29,
            "GPIO_MON" : 0x2a,
            "GPI_CFG0" : 0x2b,
            "GPI_CFG1" : 0x2c,
            "GPI_MON" : 0x2f,
            "INT_CFG" : 0x32,
            "INT_MASK0" : 0x33,
            "INT_LTCH0" : 0x36,
            "BIAS_CFG" : 0x3b,
            "CH1_CFG0" : 0x3c,
            "CH1_CFG1" : 0x3d,
            "CH1_CFG2" : 0x3e,
            "CH1_CFG3" : 0x3f,
            "CH1_CFG4" : 0x40,
            "CH2_CFG0" : 0x41,
            "CH2_CFG1" : 0x42,
            "CH2_CFG2" : 0x43,
            "CH2_CFG3" : 0x44,
            "CH2_CFG4" : 0x45,
            "CH3_CFG0" : 0x46,
            "CH3_CFG1" : 0x47,
            "CH3_CFG2" : 0x48,
            "CH3_CFG3" : 0x49,
            "CH3_CFG4" : 0x4a,
            "CH4_CFG0" : 0x4b,
            "CH4_CFG1" : 0x4c,
            "CH4_CFG2" : 0x4d,
            "CH4_CFG3" : 0x4e,
            "CH4_CFG4" : 0x4f,
            "CH5_CFG2" : 0x52,
            "CH5_CFG3" : 0x53,
            "CH5_CFG4" : 0x54,
            "CH6_CFG2" : 0x57,
            "CH6_CFG3" : 0x58,
            "CH6_CFG4" : 0x59,
            "CH7_CFG2" : 0x5c,
            "CH7_CFG3" : 0x5d,
            "CH7_CFG4" : 0x5e,
            "CH8_CFG2" : 0x61,
            "CH8_CFG3" : 0x62,
            "CH8_CFG4" : 0x63,
            "DSP_CFG0" : 0x6b,
            "DSP_CFG1" : 0x6c,
            "DRE_CFG0" : 0x6d,
            "AGC_CFG0" : 0x70,
            "IN_CH_EN" : 0x73,
            "ASI_OUT_CH_EN" : 0x74,
            "PWR_CFG" : 0x75,
            "DEV_STS0" : 0x76,
            "DEV_STS1" : 0x77
        }

    # I2C util function
    # reg_addr: register address
    # val: value to be written
    # return: True if success, False if failed
    def set(self, reg_addr, val):
        try:
            self.bus.write_byte_data(self.addr, reg_addr, val)
            return True
        except:
            return False

    # I2C util function
    # reg_addr: register address
    # return: value read from register
    def get(self, reg_addr):
        val = self.bus.read_byte_data(self.addr, reg_addr)
        return val
    
    # I2C get common status for channels and mode
    # return: channel status, mode status
    def get_status(self):
        # select page 0
        self.set(0x00, 0x00)
        time.sleep(0.01)
        return self.get(0x76), self.get(0x77)

    # I2C get value of all registers
    # return: list of indice and values of all registers
    def get_all_status(self):
        # select page 0
        self.set(0x00, 0x00)
        time.sleep(0.01)
        reg = []
        for reg_name, addr in self.reg_mp.items():
            cache = [reg_name, addr, self.get(reg_addr=addr)]
            reg.append(cache)
        return reg

    # RPi GPIO pull down
    def shutdown(self):
        GPIO.output(self.standby_pin, GPIO.LOW)
        time.sleep(0.1)

    # RPi GPIO pull up
    def startup(self):
        GPIO.output(self.standby_pin, GPIO.HIGH)
        time.sleep(0.1)
    
    # SW sleep
    # SLEEP_CFG, DEV_STS1
    def sleep(self):
        self.set(self.reg_mp['SLEEP_CFG'], 0b10010000)
        time.sleep(0.01)
        # wait until entered sleep mode
        while (self.get(self.reg_mp['DEV_STS1']) != 0b10000000):
            time.sleep(0.01)
            print("trying to sleep...")
        print("slept...")

    # SW wake
    # SLEEP_CFG, DEV_STS1
    def wake(self):
        self.set(self.reg_mp['SLEEP_CFG'], 0b10000001)
        time.sleep(0.001)
        while (self.get(self.reg_mp['DEV_STS1']) != 0b11000000):
            time.sleep(0.01)
            print("trying to awake...")
        print("waked...")

    # set output type
    # ASI_CFG0
    # Normally using 32 bit
    # Don't forget to change the slot_idx when using 16 bit
    # e.g TDM, slot_idx=0/2, for 16 bit
    # e.g I2S, slot_idx=0/32, for 16 bit
    def set_output_type(self, protocol, word_length):
        protocol_lookup = {
            "TDM" : 0,
            "I2S" : 1,
            "LJ"  : 2
        }
        word_length_lookup = {
            16 : 0,
            20 : 1,
            24 : 2,
            32 : 3
        }
        val = (protocol_lookup[protocol] << 6) | (word_length_lookup[word_length] << 4)
        self.set(self.reg_mp['ASI_CFG0'], val)
    
    # set output slot
    # ASI_CH1, ASI_CH2, ASI_CH3, ASI_CH4
    # For TDM: slot ranges from 0 to 63
    # For I2S: slot ranges from 0 to 31 for left channel, 32 to 63 for right channel
    def set_output_slot(self, channel, output, slot_idx):
        channel_lookup = {
            1 : "ASI_CH1",
            2 : "ASI_CH2",
            3 : "ASI_CH3",
            4 : "ASI_CH4"
        }
        output_lookup = {
            "SDOUT" : 0,
            "SDOUT2" : 1
        }
        val = (output_lookup[output] << 6) | (slot_idx)
        self.set(self.reg_mp[channel_lookup[channel]], val)

    # master mode setting
    # MST_CFG0: ASI master mode configuration 1
    # MST_CFG1: ASI master mode configuration 2
    # GPIO_CFG0: GPIO mode and output drive
    def set_master(self, samplerate="48kHz", mclk="24.576MHz", ratio_bck_fsync="64"):
        divider_samplerate_lookup = {
            "44.1kHz" : 0,
            "48kHz" : 1
        }
        MCLK_lookup = {
            "12MHz" : 0,
            "12.288MHz" : 1,
            "13MHz" : 2,
            "16MHz" : 3,
            "19.2MHz" : 4,
            "19.68MHz" : 5,
            "24MHz" : 6,
            "24.576MHz" : 7
        }
        val = (1<<7) | (divider_samplerate_lookup[samplerate] << 3) | (MCLK_lookup[mclk])
        self.set(self.reg_mp["MST_CFG0"], val)
        
        sample_rate_lookup = {
            "48kHz" : 4, # 44.1/48kHz
            "96kHz" : 5, # 88.2/96kHz
            "192kHz" : 6, # 176.4/192kHz
            "384kHz" : 7 # 352.8/384kHz
        }
        ratio_bck_fsync_lookup = {
            "16" : 0,
            "24" : 1,
            "32" : 2,
            "48" : 3,
            "64" : 4,
            "96" : 5,
            "128" : 6,
            "192" : 7,
            "256" : 8,
            "384" : 9,
            "512" : 10,
            "1024" : 11,
            "2048" : 12

        }
        val = (sample_rate_lookup[samplerate] << 4) | (ratio_bck_fsync_lookup[ratio_bck_fsync])
        self.set(self.reg_mp["MST_CFG1"], val)

        # set GPIO1 to be MCLK input
        # self.set(self.reg_mp['GPIO_CFG0'], 0b10100000)

    # set ADC GPIO mode and output drive
    # GPIO_CFG0: GPIO mode and output drive
    def set_adc_gpio(self, mode, output_drive="high_z"):
        mode_lookup = {
            "Disabled" : 0,
            "GPO" : 1,
            "IRQ" : 2,
            "SDOUT2" : 3,
            "PDMCLK" : 4,
            "MICBIAS" : 8,
            "GPI" : 9,
            "MCLK" : 10,
            "SDIN" : 11
        }
        output_drive_lookup = {
            "high_z" : 0,
            "active_low_weak_high" : 1
        }
        val = (mode_lookup[mode] << 4) | (output_drive_lookup[output_drive])
        self.set(self.reg_mp['GPIO_CFG0'], val)

    # set mic bias and vref for adc
    # BIAS_CFG
    def set_mic_bias(self, mic_bias, adc_vref):
        mic_bias_lookup = {
            "VREF" : 0,
            "VREF1096" : 1,
            "AVDD" : 6
        }
        adc_vref_lookup = {
            "2.75V" : 0, # supports 2Vrms for diff input or 1Vrms for single-ended input
            "2.5V" : 1, # supports 1.818Vrms for diff input or 0.909Vrms for single-ended input
            "1.375V" : 2 # supports 1.375Vrms for diff input or 0.5Vrms for single-ended input
        }
        val = (mic_bias_lookup[mic_bias] << 4) | (adc_vref_lookup[adc_vref])
        self.set(self.reg_mp["BIAS_CFG"], val)
    
    # configure inputs
    # CH1_CFG0, CH2_CFG0, CH3_CFG0, CH4_CFG0
    def set_input(self, channel, in_type, config, coupling, impedance, dre_agc):
        input_type_lookup = {
            "MIC" : 0,
            "LINEIN" : 1
        }
        diff_lookup = {
            "DIFF" : 0,
            "SINGLE" : 1,
            "PDM" : 2
        }
        dc_lookup = {
            "AC" : 0,
            "DC" : 1
        }
        impedance_lookup = {
            "2.5" : 0,
            "10" : 1,
            "20" : 2
        }
        dre_agc_lookup = {
            "OFF" : 0,
            "ON" : 1
        }
        channel_lookup = {
            1 : "CH1_CFG0",
            2 : "CH2_CFG0",
            3 : "CH3_CFG0",
            4 : "CH4_CFG0"
        }
        val = (input_type_lookup[in_type] << 7) | (diff_lookup[config] << 5) | (dc_lookup[coupling] << 4) | (impedance_lookup[impedance] << 2) | (dre_agc_lookup[dre_agc])
        self.set(self.reg_mp[channel_lookup[channel]], val)
    
    # set analog gain
    # CH1_CFG1, CH2_CFG1, CH3_CFG1, CH4_CFG1
    def set_analog_gain(self, channel, analog_gain_db):
        assert (analog_gain_db >= 0 and analog_gain_db <= 42), "Gain out of range"
        channel_lookup = {
            1 : "CH1_CFG1",
            2 : "CH2_CFG1",
            3 : "CH3_CFG1",
            4 : "CH4_CFG1"
        }
        val = (analog_gain_db << 2)
        self.set(self.reg_mp[channel_lookup[channel]], val)

    # input channel enabling
    # IN_CH_EN
    def set_input_enable(self, channel_list):
        channel_lookup = {
            1 : 7,
            2 : 6,
            3 : 5,
            4 : 4
        }
        val = 0
        for channel in channel_list:
            val |= (1 << channel_lookup[channel])
        self.set(self.reg_mp["IN_CH_EN"], val)

    # output channel enabling
    # OUT_CH_EN
    def set_output_enable(self, channel_list):
        channel_lookup = {
            1 : 7,
            2 : 6,
            3 : 5,
            4 : 4
        }
        val = 0
        for channel in channel_list:
            val |= (1 << channel_lookup[channel])
        self.set(self.reg_mp["ASI_OUT_CH_EN"], val)

    # set power
    # PWR_CFG
    def set_power(self, mic_bias, adc, pll, dyn, dyn_maxch_sel="defaultOr12"):
        mic_bias_lookup = {
            "OFF" : 0,
            "ON" : 1
        }
        adc_lookup = {
            "OFF" : 0,
            "ON" : 1
        }
        pll_lookup = {
            "OFF" : 0,
            "ON" : 1
        }
        vref_lookup = {
            "OFF" : 0,
            "ON" : 1
        }
        dyn_lookup = {
            "OFF" : 0,
            "ON" : 1
        }
        dyn_maxch_sel_lookup = {
            "defaultOr12" : 0,
            "1234" : 1,
            "123456" : 2,
            "12345678" : 3
        }
        val = (mic_bias_lookup[mic_bias] << 7) | (adc_lookup[adc] << 6) | (pll_lookup[pll] << 5) | (dyn_lookup[dyn] << 4) | (dyn_maxch_sel_lookup[dyn_maxch_sel] << 2)
        self.set(self.reg_mp["PWR_CFG"], val)
        
