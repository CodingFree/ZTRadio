#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu May  5 16:36:43 2016
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.radio_freq = radio_freq = 107.8
        self.my_transition = my_transition = 1e6
        self.my_quadrature = my_quadrature = 500e3
        self.my_freq = my_freq = 107.8
        self.my_dec_wbfm = my_dec_wbfm = 1
        self.my_cutoff = my_cutoff = 100e3

        ##################################################
        # Blocks
        ##################################################
        _radio_freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._radio_freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_radio_freq_sizer,
        	value=self.radio_freq,
        	callback=self.set_radio_freq,
        	label='radio_freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._radio_freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_radio_freq_sizer,
        	value=self.radio_freq,
        	callback=self.set_radio_freq,
        	minimum=100.0,
        	maximum=200,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_radio_freq_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_f(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-180,
        	ref_scale=10.0,
        	sample_rate=48e3,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(radio_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=50,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(int(samp_rate/500e3), firdes.low_pass(
        	1, samp_rate, my_cutoff, my_transition, firdes.WIN_HAMMING, 6.76))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0, ))
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=my_quadrature,
        	audio_decimation=my_dec_wbfm,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.my_cutoff, self.my_transition, firdes.WIN_HAMMING, 6.76))
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_radio_freq(self):
        return self.radio_freq

    def set_radio_freq(self, radio_freq):
        self.radio_freq = radio_freq
        self._radio_freq_slider.set_value(self.radio_freq)
        self._radio_freq_text_box.set_value(self.radio_freq)
        self.rtlsdr_source_0.set_center_freq(self.radio_freq, 0)

    def get_my_transition(self):
        return self.my_transition

    def set_my_transition(self, my_transition):
        self.my_transition = my_transition
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.my_cutoff, self.my_transition, firdes.WIN_HAMMING, 6.76))

    def get_my_quadrature(self):
        return self.my_quadrature

    def set_my_quadrature(self, my_quadrature):
        self.my_quadrature = my_quadrature

    def get_my_freq(self):
        return self.my_freq

    def set_my_freq(self, my_freq):
        self.my_freq = my_freq

    def get_my_dec_wbfm(self):
        return self.my_dec_wbfm

    def set_my_dec_wbfm(self, my_dec_wbfm):
        self.my_dec_wbfm = my_dec_wbfm

    def get_my_cutoff(self):
        return self.my_cutoff

    def set_my_cutoff(self, my_cutoff):
        self.my_cutoff = my_cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.my_cutoff, self.my_transition, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
