#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ask Tx
# Author: Adrian Crespo
# Generated: Sun Jun 12 20:01:05 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ham
import numpy
import osmosdr
import time
import wx


class ask_tx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Ask Tx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 192000
        self.gain = gain = 25
        self.center_freq = center_freq = 441000000

        ##################################################
        # Blocks
        ##################################################
        _gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	label='gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_gain_sizer,
        	value=self.gain,
        	callback=self.set_gain,
        	minimum=0,
        	maximum=25,
        	num_steps=25,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=10,
                decimation=1,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate * 10)
        self.osmosdr_sink_0.set_center_freq(center_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(gain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(20, (numpy.convolve(numpy.array(filter.firdes.gaussian(1, 20, 1.0, 4*20)),numpy.array((1,) * 20))))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.ham_varicode_tx_0 = ham.varicode_tx()
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(([0,1]), 1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.9, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "/home/student/kichot.txt", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.ham_varicode_tx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))    
        self.connect((self.ham_varicode_tx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))    
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate * 10)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)
        self.osmosdr_sink_0.set_gain(self.gain, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_sink_0.set_center_freq(self.center_freq, 0)


def main(top_block_cls=ask_tx, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
