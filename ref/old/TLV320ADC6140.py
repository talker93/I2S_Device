import smbus
import time

class TLV320ADC6140:

    def b2d(self, str_bin):
        b0 = int(str_bin[0]) << 7
        b1 = int(str_bin[1]) << 6
        b2 = int(str_bin[2]) << 5
        b3 = int(str_bin[3]) << 4
        b4 = int(str_bin[4]) << 3
        b5 = int(str_bin[5]) << 2
        b6 = int(str_bin[6]) << 1
        b7 = int(str_bin[7])
        return (b0+b1+b2+b3+b4+b5+b6+b7)

    def i2c_init(self, busNum, addr):
        # I2C connection Init
        self.addr = addr
        self.bus = smbus.SMBus(busNum)

    def set(self, reg_addr, val):
        self.bus.write_byte_data(self.addr, reg_addr, val)
        return True

    def get(self, reg_addr):
        val = self.bus.read_byte_data(self.addr, reg_addr)
        return val

    def __init__(self):
        # page selection
        self.reg0x00 = {
            "page0" : self.b2d("00000000"),
            "page1" : self.b2d("00000001"),
            "page2" : self.b2d("00000010"),
            "page3" : self.b2d("00000011")
        }
        # reset
        self.reg0x01 = {
            "reset" : self.b2d("00000001")
        }
        # sleep config
        self.reg0x02 = {
            # 1000: internally generate 1.8v areg supply
            # 0001: device is not in sleep
            "Areg&SleepEnz" : self.b2d("10000001")
        }
        # data format setting
        self.reg0x07 = {
            # TDM/I2S -> 00/01, 16/20/24/32bit --> 00/01/10/11, standard polarity --> 0000
            "TDM16BIT" : self.b2d("00000000"),
            "TDM32BIT" : self.b2d("00110000"),
            "I2S16BIT" : self.b2d("01000000"),
            "I2S32BIT" : self.b2d("01110000")
        }
        # output port setting channel 0
        self.reg0x0b = {
            # primaryOut/SecondaryOut --> 00/01, leftSlot0/rightSlot0/tdmSlot1/tdmSlot2 --> 000000/100000/000001/000010
            "primaryLeft" : self.b2d("00000000"),
            "primaryRight" : self.b2d("00100000"),
            "secondaryLeft" : self.b2d("01000000"),
            "secondaryRight" : self.b2d("01100000"),
            "PrimaryTdmSlot0" : self.b2d("00000000"),
            "PrimaryTdmSlot1" : self.b2d("00000001"),
            "PrimaryTdmSlot2" : self.b2d("00000010"),
            "PrimaryTdmSlot3" : self.b2d("00000011"),
            "SecondaryTdmSlot0" : self.b2d("01000000"),
            "SecondaryTdmSlot1" : self.b2d("01000001"),
            "SecondaryTdmSlot2" : self.b2d("01000010"),
            "SecondaryTdmSlot3" : self.b2d("01000011")
        }
        # output port setting channel 1
        self.reg0x0c = {
            # primaryOut/SecondaryOut --> 00/01, leftSlot0/rightSlot0/tdmSlot1/tdmSlot2 --> 000000/100000/000001/000010
            "primaryLeft" : self.b2d("00000000"),
            "primaryRight" : self.b2d("00100000"),
            "secondaryLeft" : self.b2d("01000000"),
            "secondaryRight" : self.b2d("01100000"),
            "PrimaryTdmSlot0" : self.b2d("00000000"),
            "PrimaryTdmSlot1" : self.b2d("00000001"),
            "PrimaryTdmSlot2" : self.b2d("00000010"),
            "PrimaryTdmSlot3" : self.b2d("00000011"),
            "SecondaryTdmSlot0" : self.b2d("01000000"),
            "SecondaryTdmSlot1" : self.b2d("01000001"),
            "SecondaryTdmSlot2" : self.b2d("01000010"),
            "SecondaryTdmSlot3" : self.b2d("01000011")
        }
        # output port setting channel 1
        self.reg0x0d = {
            # primaryOut/SecondaryOut --> 00/01, leftSlot0/rightSlot0/tdmSlot1/tdmSlot2 --> 000000/100000/000001/000010
            "primaryLeft" : self.b2d("00000000"),
            "primaryRight" : self.b2d("00100000"),
            "secondaryLeft" : self.b2d("01000000"),
            "secondaryRight" : self.b2d("01100000"),
            "PrimaryTdmSlot0" : self.b2d("00000000"),
            "PrimaryTdmSlot1" : self.b2d("00000001"),
            "PrimaryTdmSlot2" : self.b2d("00000010"),
            "PrimaryTdmSlot3" : self.b2d("00000011"),
            "SecondaryTdmSlot0" : self.b2d("01000000"),
            "SecondaryTdmSlot1" : self.b2d("01000001"),
            "SecondaryTdmSlot2" : self.b2d("01000010"),
            "SecondaryTdmSlot3" : self.b2d("01000011")
        }
        # output port setting channel 1
        self.reg0x0e = {
            # primaryOut/SecondaryOut --> 00/01, leftSlot0/rightSlot0/tdmSlot1/tdmSlot2 --> 000000/100000/000001/000010
            "primaryLeft" : self.b2d("00000000"),
            "primaryRight" : self.b2d("00100000"),
            "secondaryLeft" : self.b2d("01000000"),
            "secondaryRight" : self.b2d("01100000"),
            "PrimaryTdmSlot0" : self.b2d("00000000"),
            "PrimaryTdmSlot1" : self.b2d("00000001"),
            "PrimaryTdmSlot2" : self.b2d("00000010"),
            "PrimaryTdmSlot3" : self.b2d("00000011"),
            "SecondaryTdmSlot0" : self.b2d("01000000"),
            "SecondaryTdmSlot1" : self.b2d("01000001"),
            "SecondaryTdmSlot2" : self.b2d("01000010"),
            "SecondaryTdmSlot3" : self.b2d("01000011")
        }
        # output port setting GPIO
        self.reg0x21 = {
            "disabled" : self.b2d("00000000"),
            # "SDOUT2" : self.b2d("00110000")
            "SDOUT2" : self.b2d("00110010")
        }
        # mic bias and adc fullscale setting
        self.reg0x3b = {
            # MicBias: VREF/VREF*1.096/AVDD --> 0000/0001/0110, ADC_FullScale: VREF2.75/VREF2.5/VREF1.375 --> 0000/0001/0010
            "AVDD&VREF275" : self.b2d("01100000"),
            "AVDD&VREF1375" : self.b2d("01100010")
        }
        # Input config channel 0
        self.reg0x3c = {
            # intput type: mic/lineIn --> 0/1, diff/single/pdm --> 00/01/10, ac/dc --> 0/1, impedance: 2.5k/10k/20k --> 00/01/10, AGC and DRE: disabled/enabled --> 00/01
            "MIC&DIFF" : self.b2d("00000000"),
            "MIC&SINGLE" : self.b2d("00100000"),
            "LINE&DIFF" : self.b2d("10000000"),
            "LINE&SINGLE" : self.b2d("10100000")
        }
        # Input config channel 1
        self.reg0x41 = {
            # intput type: mic/lineIn --> 0/1, diff/single/pdm --> 00/01/10, ac/dc --> 0/1, impedance: 2.5k/10k/20k --> 00/01/10, AGC and DRE: disabled/enabled --> 00/01
            "MIC&DIFF" : self.b2d("00000000"),
            "MIC&SINGLE" : self.b2d("00100000"),
            "LINE&DIFF" : self.b2d("10000000"),
            "LINE&SINGLE" : self.b2d("10100000")
        }
        # Input config channel 2
        self.reg0x46 = {
            # intput type: mic/lineIn --> 0/1, diff/single/pdm --> 00/01/10, ac/dc --> 0/1, impedance: 2.5k/10k/20k --> 00/01/10, AGC and DRE: disabled/enabled --> 00/01
            "MIC&DIFF" : self.b2d("00000000"),
            "MIC&SINGLE" : self.b2d("00100000"),
            "LINE&DIFF" : self.b2d("10000000"),
            "LINE&SINGLE" : self.b2d("10100000")
        }
        # Input config channel 3
        self.reg0x4b = {
            # intput type: mic/lineIn --> 0/1, diff/single/pdm --> 00/01/10, ac/dc --> 0/1, impedance: 2.5k/10k/20k --> 00/01/10, AGC and DRE: disabled/enabled --> 00/01
            "MIC&DIFF" : self.b2d("00000000"),
            "MIC&SINGLE" : self.b2d("00100000"),
            "LINE&DIFF" : self.b2d("10000000"),
            "LINE&SINGLE" : self.b2d("10100000")
        }
        # Input Config Gain channel 0
        self.reg0x3d = {
            "0db" : self.b2d("00000000"),
            "10db" : self.b2d("00101000"),
            "32db" : self.b2d("10000000")
        }
        # Input Config Gain channel 1
        self.reg0x42 = {
            "0db" : self.b2d("00000000"),
            "10db" : self.b2d("00101000"),
            "32db" : self.b2d("10000000")
        }
        # Input Config Gain channel 2
        self.reg0x47 = {
            "0db" : self.b2d("00000000"),
            "10db" : self.b2d("00101000"),
            "32db" : self.b2d("10000000")
        }
        # Input Config Gain channel 3
        self.reg0x4c = {
            "0db" : self.b2d("00000000"),
            "10db" : self.b2d("00101000"),
            "32db" : self.b2d("10000000")
        }
        # input channel enabling
        self.reg0x73 = {
            "1234" : self.b2d("11110000"),
            "1" : self.b2d("10000000"),
            "12" : self.b2d("11000000"),
            "123" : self.b2d("11100000")
        }
        # output channel enabling
        self.reg0x74 = {
            "1234" : self.b2d("11110000"),
            "1" : self.b2d("10000000"),
            "12" : self.b2d("11000000"),
            "123" : self.b2d("11100000")
        }
        # power config
        self.reg0x75 = {
            # micPwrDown/Up --> 0/1, adcPowerDown/Up --> 0/1, pllPowerDown/Up --> 0/1, dynamicPowerDown/Up --> 0/1, dynamicPowerDownUpChannel1-2/1-4 --> 00/01/11
            "NONE" : self.b2d("00000000"),
            "ADC" : self.b2d("01000000"),
            "ADC&PLL" : self.b2d("01100000"),
            "MIC&ADC&PLL" : self.b2d("11100000"),
            "MIC&ADC&PLL&DYN&DYNCH2" : self.b2d("11110000"),
            "MIC&ADC&PLL&DYN&DYNCH4" : self.b2d("11110100"),
            "MIC&ADC&PLL&DYN&DYNCH8" : self.b2d("11111100"),
        }
        # device status power up/down, channel 1-8
        self.reg0x76 = {
            "1" : self.b2d("10000000"),
            "12" : self.b2d("11000000"),
            "1234" : self.b2d("11110000")
        }
        # device status  sleep/active
        self.reg0x77 = {
            "active&off" : self.b2d("11000000"),
            "active" : self.b2d("11100000")
        }
