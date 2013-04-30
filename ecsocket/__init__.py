#!/usr/bin/env python
"""
ECSocket module

This module provides a simple abstraction for communicating with the Ecelerity
console via a local socket connection.

Example:
    >>> s = ECSocket()
    >>> s.command('pid')
    '1234'
    >>> s.close()

"""

import socket
import struct
import sys

class ECSocket(object):
    def __init__(self, socketfile='/tmp/2025'):
        """Return a connection object.

        Instantiate a connection to the Ecelerity console socket.

        """
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(socketfile)

    def command(self, command):
        """Pass a command and receive the results.

        A command is passed into the console and the resulting output is
        returned.

        >>> s.command('version')
        "####... <<version-string>>> "

        """
        self.sock.send(struct.pack('!HH', 1, len(command)) + command)
        type = struct.unpack('!H', self.sock.recv(2))[0]
        if (type == 1):
            size = int(struct.unpack('!H', self.sock.recv(2))[0])
        elif (type == 2):
            size = int(struct.unpack('!L', self.sock.recv(4))[0])

        return self.sock.recv(size)

    def close(self):
        """Close the socket connection

        Call to close the connection when all communication is completed.
        (Alternatively the connection will close upon termination of the
        parent program.

        """
        self.sock.close()

if __name__ == '__main__':
    print "This is a module that should be imported."
    sys.exit(1)
