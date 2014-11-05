from time import sleep
import gtk

from pineal.osc import Osc
from pineal.config import OSC_GUI, OSC_CORE

from pineal.gui.widgets import VisualFrame, Menu


class Gui(object):
    """Display a gui"""
    def __init__(self):
        self.win = gtk.Window()
        self.win.set_title('Pineal Loop Project')
        self.win.resize(200,1)
        self.win.connect('delete-event', self.quit)

        vbox = gtk.VBox()
        menu = Menu(self)
        self.box = gtk.HBox()

        self.win.add(vbox)
        vbox.add(menu)
        vbox.add(self.box)

        self.win.show_all()

        self.visuals = {}
        self._stop = False

    def run(self):
        print 'starting pineal.gui'
        self.osc = Osc(OSC_GUI, OSC_CORE)
        self.osc.listen('add', self.cb_add)
        self.osc.start()

        try:
            while not self._stop:
                gtk.main_iteration()
                sleep(0.01)  # don't ask me why
        except KeyboardInterrupt:
            self.osc.stop()

    def stop(self):
        print 'stopping pineal.gui'
        self._stop = True

    def quit(self, widget, event):
        return not self._stop

    def cb_add(self, path, tags, args, source):
        visual, var, value = args

        with gtk.gdk.lock:
            if visual not in self.visuals.keys():
                self.visuals[visual] = VisualFrame(self, visual)
                self.box.add(self.visuals[visual])

            if var not in self.visuals[visual].variables.keys():
                self.visuals[visual].add_var(var)
                self.visuals[visual].variables[var].change(value)

            self.box.show_all()
