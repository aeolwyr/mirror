#!/usr/bin/env python3
from gi.repository import Gio

def receive(callback):
    def receive_size(stream, result=None):
        stream.read_bytes_async(4, 0, None, receive_size_finish)

    def receive_size_finish(stream, result):
        size_bytes = stream.read_bytes_finish(result).get_data()
        size = int.from_bytes(size_bytes, byteorder='little')
        receive_data(stream, size)

    def receive_data(stream, size, memory=Gio.MemoryInputStream.new()):
        if size == 0:
            receive_size(stream)
            return
        stream.read_bytes_async(size, 0, None, receive_data_finish,
                size, memory)

    def receive_data_finish(stream, result, size, memory):
        buf = stream.read_bytes_finish(result)
        size -= buf.get_size()
        memory.add_bytes(buf)
        if size > 0:
            # there's still more data to download for this image frame
            receive_data(stream, size, memory)
            return
        callback(memory)
        receive_size(stream)

    connection = Gio.SocketClient().connect_to_host('127.0.0.1', 1313)
    # skip the header
    connection.get_input_stream().skip_async(24, 0, None, receive_size)
