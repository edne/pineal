from threading import Thread
import gtk
from thirdparty.OSC import OSCClient, OSCServer, OSCMessage, OSCClientError
import socket
from pineal.config import OSC_CORE, OSC_GUI

class GuiOsc(Thread):
    def __init__(self, gui):
        Thread.__init__(self)
        self.gui = gui

        self.server = OSCServer(OSC_GUI)
        self.server.addMsgHandler('/add', self.add)
        self.server.addMsgHandler('/error', self.error)

        self.client = OSCClient()
        self.client.connect(OSC_CORE)

    def run(self):
        try:
            self.server.serve_forever()
        except socket.error:
            pass

    def stop(self):
        self.server.server_close()

    def add(self, path, tags, args, source):
        self.gui.add(*args)

    def error(self, path, tags, args, source):
        name, log = args
        if log:
            print name, log

    def send_change(self, visual, var, value):
        try:
            self.client.send(
                OSCMessage('/visual/'+visual+'/'+var, float(value))
            )
        except OSCClientError:  # sometime rises a 'connection refused'
            pass
