"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pmt
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, num_samples_to_count=128):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Selector Control',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.num_samples_to_count = num_samples_to_count
        self.portName = 'messageOutput'
        self.message_port_register_out(pmt.intern(self.portName))
        self.state = True
        self.counter = 0

    def work(self, input_items, output_items):
        self.counter = self.counter + len(output_items[0])

        if (self.counter > self.num_samples_to_count):
            PMT_msg = pmt.from_bool(self.state)
            self.message_port_pub(pmt.intern(self.portName), PMT_msg)
            self.state = not(self.state)
            self.counter = 0

        output_items[0][:] = input_items[0]
        return len(output_items[0])
