#!/usr/bin/env python2

from gnuradio import gr
from gnuradio import audio
from gnuradio import analog

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        sample_rate = 32000
        ampl = 1

        src0 = analog.sig_source_f(sample_rate, analog.GR_SIN_WAVE, 1000, ampl)
        src1 = analog.sig_source_f(sample_rate, analog.GR_SIN_WAVE, 12000, ampl)
        dst = audio.sink(sample_rate, "")
        self.connect(src0, (dst, 0))
        self.connect(src1, (dst, 1))

if __name__ == '__main__':
    try:
        my_top_block().run()
    except [[KeyboardInterrupt]]:
        pass