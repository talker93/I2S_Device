from TLV320ADC6140 import TLV320ADC6140
import time

adc = TLV320ADC6140()

adc.i2c_init(1, 0x4c)

time.sleep(1)

reg = []

# select page 0
# adc.set(0x00, adc.reg0x00['page0'])

time.sleep(0.01)

for idx in range(120):
    cache = [idx, adc.get(idx)]
    reg.append(cache)
    print(cache)
