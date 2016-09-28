"""Capture of C-level stdout/stderr.

Inspired from https://github.com/minrk/wurlitzer, but using sockets in order to
support Windows.
"""

from contextlib import contextmanager
import os
from selectors import DefaultSelector, EVENT_READ
from threading import Thread
import socket
import sys


@contextmanager
def redirect(fd, callback):
    save_fd = os.dup(fd)

    s_in, s_out = socket.socketpair()
    os.dup2(s_in.fileno(), fd)
    os.close(s_in.fileno())
    s_out.setblocking(False)

    sel = DefaultSelector()
    sel.register(s_out, EVENT_READ)

    def target():
        while running:
            _, = sel.select()  # There's only one event.
            callback(s_out.recv(4096))

    running = True
    thread = Thread(target=target, daemon=True)
    thread.start()

    try:
        yield
    finally:
        running = False
        os.dup2(save_fd, fd)
        os.close(save_fd)
