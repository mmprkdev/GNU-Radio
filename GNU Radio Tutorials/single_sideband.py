#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.6.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sip



class single_sideband(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "single_sideband")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.tuning = tuning = 17e3
        self.samp_rate = samp_rate = 192e3
        self.reverse = reverse = (-1)
        self.fine_tuning = fine_tuning = 1.5e3
        self.carrier_freq = carrier_freq = 16e3
        self.audio_tone = audio_tone = 1e3
        self.audio_samp_rate = audio_samp_rate = 48000
        self.audio_gain_tx = audio_gain_tx = 10
        self.audio_gain_rx = audio_gain_rx = 0.5
        self.audio_ = audio_ = 0

        ##################################################
        # Blocks
        ##################################################

        self._tuning_range = Range(11e3, 21e3, 100, 17e3, 200)
        self._tuning_win = RangeWidget(self._tuning_range, self.set_tuning, "Tuning", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tuning_win)
        # Create the options list
        self._reverse_options = [-1, 1]
        # Create the labels list
        self._reverse_labels = ['Upper', 'Lower']
        # Create the combo box
        self._reverse_tool_bar = Qt.QToolBar(self)
        self._reverse_tool_bar.addWidget(Qt.QLabel("Sideband" + ": "))
        self._reverse_combo_box = Qt.QComboBox()
        self._reverse_tool_bar.addWidget(self._reverse_combo_box)
        for _label in self._reverse_labels: self._reverse_combo_box.addItem(_label)
        self._reverse_callback = lambda i: Qt.QMetaObject.invokeMethod(self._reverse_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._reverse_options.index(i)))
        self._reverse_callback(self.reverse)
        self._reverse_combo_box.currentIndexChanged.connect(
            lambda i: self.set_reverse(self._reverse_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._reverse_tool_bar)
        self._fine_tuning_range = Range(0, 3e3, 10, 1.5e3, 200)
        self._fine_tuning_win = RangeWidget(self._fine_tuning_range, self.set_fine_tuning, "Fine Tuning", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._fine_tuning_win)
        self._audio_gain_tx_range = Range(0, 20, 1, 10, 200)
        self._audio_gain_tx_win = RangeWidget(self._audio_gain_tx_range, self.set_audio_gain_tx, "Audio Gain Tx", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._audio_gain_tx_win)
        self._audio_gain_rx_range = Range(0, 1, .05, 0.5, 200)
        self._audio_gain_rx_win = RangeWidget(self._audio_gain_rx_range, self.set_audio_gain_rx, "Audio Gain Rx", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._audio_gain_rx_win)
        self.qtgui_freq_sink_x_2 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            audio_samp_rate, #bw
            "Demod Audio", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_2.set_update_time(0.10)
        self.qtgui_freq_sink_x_2.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_2.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2.enable_autoscale(False)
        self.qtgui_freq_sink_x_2.enable_grid(False)
        self.qtgui_freq_sink_x_2.set_fft_average(1.0)
        self.qtgui_freq_sink_x_2.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2.enable_control_panel(False)
        self.qtgui_freq_sink_x_2.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_2.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_win = sip.wrapinstance(self.qtgui_freq_sink_x_2.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_2_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "AM single sideband", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "AM Double Sideband", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(4, firdes.low_pass(1.0,samp_rate,3000,100), tuning, samp_rate)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\mmprk\\Music\\fishing_boats.wav', True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, 4)
        self.blocks_multiply_xx_2 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(audio_gain_rx)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(reverse)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(audio_gain_tx)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (carrier_freq+300),
                (carrier_freq+3000),
                200,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_2_0 = analog.sig_source_f(audio_samp_rate, analog.GR_COS_WAVE, fine_tuning, 1, 0, 0)
        self.analog_sig_source_x_2 = analog.sig_source_f(audio_samp_rate, analog.GR_SIN_WAVE, fine_tuning, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, carrier_freq, 1, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_2, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_sig_source_x_2_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.band_pass_filter_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.qtgui_freq_sink_x_2, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_float_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "single_sideband")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.tuning)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.carrier_freq+300), (self.carrier_freq+3000), 200, window.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1.0,self.samp_rate,3000,100))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)

    def get_reverse(self):
        return self.reverse

    def set_reverse(self, reverse):
        self.reverse = reverse
        self._reverse_callback(self.reverse)
        self.blocks_multiply_const_vxx_1.set_k(self.reverse)

    def get_fine_tuning(self):
        return self.fine_tuning

    def set_fine_tuning(self, fine_tuning):
        self.fine_tuning = fine_tuning
        self.analog_sig_source_x_2.set_frequency(self.fine_tuning)
        self.analog_sig_source_x_2_0.set_frequency(self.fine_tuning)

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.analog_sig_source_x_0.set_frequency(self.carrier_freq)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.carrier_freq+300), (self.carrier_freq+3000), 200, window.WIN_HAMMING, 6.76))

    def get_audio_tone(self):
        return self.audio_tone

    def set_audio_tone(self, audio_tone):
        self.audio_tone = audio_tone

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.analog_sig_source_x_2.set_sampling_freq(self.audio_samp_rate)
        self.analog_sig_source_x_2_0.set_sampling_freq(self.audio_samp_rate)
        self.qtgui_freq_sink_x_2.set_frequency_range(0, self.audio_samp_rate)

    def get_audio_gain_tx(self):
        return self.audio_gain_tx

    def set_audio_gain_tx(self, audio_gain_tx):
        self.audio_gain_tx = audio_gain_tx
        self.blocks_multiply_const_vxx_0.set_k(self.audio_gain_tx)

    def get_audio_gain_rx(self):
        return self.audio_gain_rx

    def set_audio_gain_rx(self, audio_gain_rx):
        self.audio_gain_rx = audio_gain_rx
        self.blocks_multiply_const_vxx_2.set_k(self.audio_gain_rx)

    def get_audio_(self):
        return self.audio_

    def set_audio_(self, audio_):
        self.audio_ = audio_




def main(top_block_cls=single_sideband, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
