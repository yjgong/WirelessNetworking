#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: DVB-T Signal Detector
# Author: Yujing Gong
# Description: For the course Wireless Networking
# Generated: Sat Apr 30 17:47:53 2016
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

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sip
import sys
import time


class signal_detector(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "DVB-T Signal Detector")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("DVB-T Signal Detector")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "signal_detector")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.threshold = threshold = -70
        self.samp_rate = samp_rate = 2048000
        self.freq = freq = 525200000
        self.fft_size = fft_size = 1024

        ##################################################
        # Blocks
        ##################################################
        self._threshold_range = Range(-100, 0, 1, -70, 200)
        self._threshold_win = RangeWidget(self._threshold_range, self.set_threshold, "Threshold", "counter_slider", float)
        self.top_layout.addWidget(self._threshold_win)
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, "Waterfall")
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, "Spectrum")
        self.tab_widget_2 = Qt.QWidget()
        self.tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_2)
        self.tab_grid_layout_2 = Qt.QGridLayout()
        self.tab_layout_2.addLayout(self.tab_grid_layout_2)
        self.tab.addTab(self.tab_widget_2, "Result")
        self.top_layout.addWidget(self.tab)
        self._samp_rate_range = Range(1024000, 8192000, 512000, 2048000, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, "Sample rate", "counter_slider", float)
        self.top_layout.addWidget(self._samp_rate_win)
        self._freq_range = Range(478000000, 862000000, 1000000, 525200000, 200)
        self._freq_win = RangeWidget(self._freq_range, self.set_freq, "Frequency", "counter_slider", float)
        self.top_layout.addWidget(self._freq_win)
        self._fft_size_range = Range(512, 8192, 512, 1024, 200)
        self._fft_size_win = RangeWidget(self._fft_size_range, self.set_fft_size, "FFT_SIZE", "counter_slider", float)
        self.top_layout.addWidget(self._fft_size_win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(20, 0)
        self.rtlsdr_source_0.set_if_gain(10, 0)
        self.rtlsdr_source_0.set_bb_gain(5, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(8000000, 0)
          
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	fft_size, #size
        	firdes.WIN_RECTANGULAR, #wintype
        	freq, #fc
        	samp_rate*4, #bw
        	"Waterfall", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.001)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        
        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0.set_intensity_range(-110, -30)
        
        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	fft_size, #size
        	firdes.WIN_RECTANGULAR, #wintype
        	freq, #fc
        	samp_rate*4, #bw
        	"Frequency", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, (window.rectangular(fft_size)), True, 1)
        self.detector_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.detector_0.set_update_time(1)
        self.detector_0.set_title("Signal Detector")
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        units = ["", "", "", "", "",
                 "", "", "", "", ""]
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.detector_0.set_min(i, -120)
            self.detector_0.set_max(i, 0)
            self.detector_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.detector_0.set_label(i, "Data {0}".format(i))
            else:
                self.detector_0.set_label(i, labels[i])
            self.detector_0.set_unit(i, units[i])
            self.detector_0.set_factor(i, factor[i])
        
        self.detector_0.enable_autoscale(False)
        self._detector_0_win = sip.wrapinstance(self.detector_0.pyqwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._detector_0_win)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_size)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(threshold, threshold, threshold)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, 1, 0)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(fft_size, 1.0/fft_size, 4000)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_size)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, fft_size*fft_size)
        self.Result = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.Result.set_update_time(0.1)
        self.Result.set_title("Signal Detector")
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        units = ["", "", "", "", "",
                 "", "", "", "", ""]
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.Result.set_min(i, 0)
            self.Result.set_max(i, 1)
            self.Result.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.Result.set_label(i, "Data {0}".format(i))
            else:
                self.Result.set_label(i, labels[i])
            self.Result.set_unit(i, units[i])
            self.Result.set_factor(i, factor[i])
        
        self.Result.enable_autoscale(False)
        self._Result_win = sip.wrapinstance(self.Result.pyqwidget(), Qt.QWidget)
        self.tab_layout_2.addWidget(self._Result_win)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_divide_xx_0, 1))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_vector_to_stream_0, 0))    
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_nlog10_ff_0, 0))    
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_moving_average_xx_0, 0), (self.detector_0, 0))    
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_moving_average_xx_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.Result, 0))    
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_divide_xx_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_0_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "signal_detector")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.blocks_threshold_ff_0.set_hi(self.threshold)
        self.blocks_threshold_ff_0.set_lo(self.threshold)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate*4)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate*4)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate*4)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.freq, self.samp_rate*4)
        self.rtlsdr_source_0.set_center_freq(self.freq, 0)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.analog_const_source_x_0.set_offset(self.fft_size*self.fft_size)
        self.blocks_moving_average_xx_0.set_length_and_scale(self.fft_size, 1.0/self.fft_size)


def main(top_block_cls=signal_detector, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
