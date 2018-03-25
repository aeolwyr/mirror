#!/usr/bin/env python3
from gi.repository import Gio

class Client(Gio.Application):
    def __init__(self):
        self.connection = Gio.SocketClient().connect_to_host('127.0.0.1', 1111)
        self.stream = self.connection.get_output_stream()
        
        # read the metadata from the header
        buf = self.connection.get_input_stream().read_bytes(22)
        params = buf.get_data()[9:].split(b' ')

        self.max_x = int(params[0])
        self.max_y = int(params[1])
        self.max_pressure = int(params[2])

    # action argument follows the minitouch convention
    def send(self, action, x, y):
        msg = '{} 0 {} {} {}\nc\n'.format(action,
                int(x * self.max_x),
                int(y * self.max_y),
                self.max_pressure)
        self.stream.write_all(msg.encode('ascii'))
