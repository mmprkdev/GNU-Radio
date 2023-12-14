"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

from operator import index
import numpy as np
import pmt
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, threshold=1.0, report_period=128):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Threshold Detector',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.threshold = threshold
        self.report_period = report_period

        self.timer = 0
        self.readyForTag = True

    def work(self, input_items, output_items):
        # Remember that input_items[0] accesses port 0 of the block.
        # input_items[0][0] accesses the first sample of port 0. So this
        # loop is using index to access each sample going through port 0 input port.
        # The amplitude of the sample is the only value stored by a sample.

        for index in range(len(input_items[0])):
            if (input_items[0][index] >= self.threshold and self.readyForTag == True):
                # define the key as 'detect'
                key = pmt.intern('detect')
                # get the detection value
                value = pmt.from_float(np.round(float(input_items[0][index]),2))
                # tag index to be written
                writeIndex = self.nitems_written(0) + index
                # add the tag object (key, value pair)
                self.add_item_tag(0, writeIndex, key, value)
                # the tag has been written, set the state
                self.readyForTag = False

            # increase the timer by 1
            if (self.readyForTag == False):
                self.timer = self.timer + 1

            # set the flag to write
            if (self.timer >= self.report_period):
                # reset timer
                self.timer = 0
                # reset readyForTag state
                self.readyForTag = True

        output_items[0][:] = input_items[0]
        return len(output_items[0])
