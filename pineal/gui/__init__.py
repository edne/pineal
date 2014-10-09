from multiprocessing import Process
from threading import Thread
from time import sleep
import gobject
import gtk
from thirdparty.OSC import OSCClient, OSCServer, OSCMessage

from pineal.config import OSC_CORE, OSC_GUI


class VarSlider(gtk.Frame):
    def __init__(self, gui, visual, var):
        gtk.Frame.__init__(self, var)
        self.gui = gui
        self.visual = visual
        self.var = var

        adjustment = gtk.Adjustment(
            lower = 0.0,
            upper = 100.0,
            step_incr = 1.0,
            page_incr = 5.0
        )
        adjustment.connect('value-changed', self.changed)

        scale = gtk.VScale(adjustment)
        scale.set_inverted(True)
        scale.set_draw_value(False)
        #scale.set_increments(0.01, 0.2)
        scale.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.add(scale)
        self.show_all()

    def changed(self, adjustment):
        value = adjustment.get_value()/100
        self.gui.guiOsc.client.send(
            OSCMessage('/'+self.visual+'/'+self.var, float(value))
        )


class VisualFrame(gtk.Frame):
    def __init__(self, gui, visual):
        gtk.Frame.__init__(self, visual)
        self.gui = gui
        self.visual = visual

        self.hbox = gtk.HBox()
        self.add(self.hbox)
        self.show_all()
        self.variables = {}

    def add_var(self, var):
        varSlider = VarSlider(self.gui, self.visual, var)
        self.variables[var] = varSlider
        self.hbox.add(varSlider)
        self.hbox.show_all()


class GuiOsc(Thread):
    def __init__(self, gui):
        Thread.__init__(self)
        self.gui = gui

        self.server = OSCServer(OSC_GUI)
        self.server.addMsgHandler('/add', self.add)
        self.server.addMsgHandler('/remove', self.remove)
        self.server.addMsgHandler('/change', self.change)

        self.client = OSCClient()
        self.client.connect(OSC_CORE)

        self._stop = False

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self._stop = True

    def add(self, path, tags, args, source):
        self.gui.add(*args)

    def remove(self, path, tags, args, source):
        None

    def change(self, path, tags, args, source):
        None

    def send(self, visual, var, value):
        self.client.send( OSCMessage('/'+visual+'/'+var, float(value)) )


class Gui(Process):
    """Display a gui for the sliders"""
    def __init__(self):
        Process.__init__(self)

        self.win = gtk.Window()
        self.win.set_title('')
        self.win.resize(1,200)

        self.win.connect('delete-event', self.quit, None)
        self.win.show_all()

        self.box = gtk.HBox()
        self.win.add(self.box)
        self.box.show()

        self.visuals = {}

    def run(self):
        print 'starting pineal.gui'
        self.guiOsc = GuiOsc(self)
        self.guiOsc.start()

        try:
            while True:
                gtk.main_iteration()
                sleep(0.01)
        except KeyboardInterrupt:
            None

        self.guiOsc.stop()

    def stop(self):
        print 'stopping pineal.gui'

    def quit(self, widget, event, data):
        return True  # if True gui wan't close on user signal

    def add(self, visual, var):
        with gtk.gdk.lock:
            if visual not in self.visuals.keys():
                self.visuals[visual] = VisualFrame(self, visual)
                self.box.add(self.visuals[visual])

            if var not in self.visuals[visual].variables.keys():
                self.visuals[visual].add_var(var)

            self.box.show_all()
