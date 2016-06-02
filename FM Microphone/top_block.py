#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Jun  2 21:27:51 2016
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
from gnuradio import audio
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
        self.samp_rate = samp_rate = 48e3
        self.my_transition = my_transition = 1000
        self.my_freq = my_freq = 29530e3
        self.my_cutoff = my_cutoff = 1000

        ##################################################
        # Blocks
        ##################################################
        _my_transition_sizer = wx.BoxSizer(wx.VERTICAL)
        self._my_transition_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_my_transition_sizer,
        	value=self.my_transition,
        	callback=self.set_my_transition,
        	label='my_transition',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._my_transition_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_my_transition_sizer,
        	value=self.my_transition,
        	callback=self.set_my_transition,
        	minimum=1,
        	maximum=1e4,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_my_transition_sizer)
        _my_freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._my_freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_my_freq_sizer,
        	value=self.my_freq,
        	callback=self.set_my_freq,
        	label='my_freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._my_freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_my_freq_sizer,
        	value=self.my_freq,
        	callback=self.set_my_freq,
        	minimum=29000e3,
        	maximum=30000e3,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_my_freq_sizer)
        _my_cutoff_sizer = wx.BoxSizer(wx.VERTICAL)
        self._my_cutoff_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_my_cutoff_sizer,
        	value=self.my_cutoff,
        	callback=self.set_my_cutoff,
        	label='my_cutoff',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._my_cutoff_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_my_cutoff_sizer,
        	value=self.my_cutoff,
        	callback=self.set_my_cutoff,
        	minimum=1,
        	maximum=1e4,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_my_cutoff_sizer)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=my_freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=1,
        	average=False,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=12,
                decimation=5,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate*0.8)
        self.osmosdr_sink_0.set_center_freq(my_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, my_cutoff, my_transition, firdes.WIN_HAMMING, 6.76))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((10, ))
        self.audio_source_0 = audio.source(48000, "pulse", True)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=32000,
        	quad_rate=640000,
        	tau=75e-6,
        	max_dev=75e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_tx_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate*0.8)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.my_cutoff, self.my_transition, firdes.WIN_HAMMING, 6.76))

    def get_my_transition(self):
        return self.my_transition

    def set_my_transition(self, my_transition):
        self.my_transition = my_transition
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.my_cutoff, self.my_transition, firdes.WIN_HAMMING, 6.76))
        self._my_transition_slider.set_value(self.my_transition)
        self._my_transition_text_box.set_value(self.my_transition)

    def get_my_freq(self):
        return self.my_freq

    def set_my_freq(self, my_freq):
        self.my_freq = my_freq
        self.osmosdr_sink_0.set_center_freq(self.my_freq, 0)
        self.wxgui_fftsink2_0.set_baseband_freq(self.my_freq)
        self._my_freq_slider.set_value(self.my_freq)
        self._my_freq_text_box.set_value(self.my_freq)

    def get_my_cutoff(self):
        return self.my_cutoff

    def set_my_cutoff(self, my_cutoff):
        self.my_cutoff = my_cutoff
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.my_cutoff, self.my_transition, firdes.WIN_HAMMING, 6.76))
        self._my_cutoff_slider.set_value(self.my_cutoff)
        self._my_cutoff_text_box.set_value(self.my_cutoff)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
