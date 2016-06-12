#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ask
# Author: Adrian Crespo
# Generated: Sun Jun 12 20:15:37 2016
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
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import ham
import osmosdr
import time
import wx


class ask(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Ask")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1.2e6
        self.offset = offset = 50000
        self.gain = gain = 50
        self.freq = freq = 441e6
        self.decim = decim = 5
        self.corr = corr = 0

        ##################################################
        # Blocks
        ##################################################
        _corr_sizer = wx.BoxSizer(wx.VERTICAL)
        self._corr_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_corr_sizer,
        	value=self.corr,
        	callback=self.set_corr,
        	label='corr',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._corr_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_corr_sizer,
        	value=self.corr,
        	callback=self.set_corr,
        	minimum=-100,
        	maximum=100,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_corr_sizer)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate / decim,
        	v_scale=0.25,
        	v_offset=0,
        	t_scale=0.001,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.osmosdr_source_1 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_1.set_time_source("gpsdo", 0)
        self.osmosdr_source_1.set_sample_rate(samp_rate)
        self.osmosdr_source_1.set_center_freq(freq - offset, 0)
        self.osmosdr_source_1.set_freq_corr(corr, 0)
        self.osmosdr_source_1.set_dc_offset_mode(0, 0)
        self.osmosdr_source_1.set_iq_balance_mode(0, 0)
        self.osmosdr_source_1.set_gain_mode(False, 0)
        self.osmosdr_source_1.set_gain(1, 0)
        self.osmosdr_source_1.set_if_gain(30, 0)
        self.osmosdr_source_1.set_bb_gain(30, 0)
        self.osmosdr_source_1.set_antenna("", 0)
        self.osmosdr_source_1.set_bandwidth(2000000, 0)
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(decim, firdes.low_pass(
        	1, samp_rate, 50000, 25000, firdes.WIN_HAMMING, 6.76))
        self.ham_varicode_rx_0 = ham.varicode_rx()
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
        	maximum=50,
        	num_steps=125,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_gain_sizer)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff((samp_rate/5/9600), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(320, True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, "/dev/stdout", False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -offset, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.ham_varicode_rx_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.ham_varicode_rx_0, 0), (self.blocks_file_sink_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.osmosdr_source_1, 0), (self.blocks_multiply_xx_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.digital_clock_recovery_mm_xx_0.set_omega((self.samp_rate/5/9600))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 50000, 25000, firdes.WIN_HAMMING, 6.76))
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate / self.decim)
        self.osmosdr_source_1.set_sample_rate(self.samp_rate)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.analog_sig_source_x_0.set_frequency(-self.offset)
        self.osmosdr_source_1.set_center_freq(self.freq - self.offset, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self._gain_slider.set_value(self.gain)
        self._gain_text_box.set_value(self.gain)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_source_1.set_center_freq(self.freq - self.offset, 0)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate / self.decim)

    def get_corr(self):
        return self.corr

    def set_corr(self, corr):
        self.corr = corr
        self._corr_slider.set_value(self.corr)
        self._corr_text_box.set_value(self.corr)
        self.osmosdr_source_1.set_freq_corr(self.corr, 0)


def main(top_block_cls=ask, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
