# -*- coding: utf-8 -*-
import json
import socket
import ssl
import struct

__author__ = 'Dariusz Aniszewski, Polidea'


class PushSender():
    ssl_connection = None
    notifications = []
    sandbox = False
    sandbox_host = ("gateway.sandbox.push.apple.com", 2195)
    production_host = ("gateway.push.apple.com", 2195)
    verbose = True

    def __init__(self, certificate_file, sandbox=False, verbose=True):
        self.ssl_connection = ssl.wrap_socket(socket.socket(), certfile=certificate_file)
        self.sandbox = sandbox
        self.verbose = verbose
        if self.verbose:
            print "Initiate PushSender"
            print "Using cert: %s" % certificate_file
            print "Using sandbox: %s" % sandbox

    def __connect(self):
        if self.sandbox:
            host = self.sandbox_host
        else:
            host = self.production_host
        self.ssl_connection.connect(host)
        if self.verbose:
            print "Connected to %s at port %s" % (host[0], host[1])

    def __disconnect(self):
        self.ssl_connection.close()
        if self.verbose:
            print "Connection closed"

    def __write(self, data):
        self.ssl_connection.write(data)

    def __cleanup(self):
        self.notifications = []

    def add_notification(self, payload_dict, device_token):
        if None in [payload_dict, device_token]:
            raise ValueError("wrong params")
        self.notifications.append((payload_dict, device_token))

    def send_notifications(self):
        if len(self.notifications) == 0:
            if self.verbose:
                print "Nothing to push"
            return
        self.__connect()
        for notification in self.notifications:
            payload = json.dumps(notification[0])
            if self.verbose:
                print "Sending %s to %s" % (payload, notification[1])
            token = bytes(notification[1].decode('hex'))
            format = "!BH32sH%ds" % len(payload)
            push = struct.pack(format, 0, 32, token, len(payload), payload)
            self.__write(push)
        self.__disconnect()
        self.__cleanup()
