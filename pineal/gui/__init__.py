from multiprocessing import Process
from threading import Thread
from time import sleep
import gtk

from pineal.gui.guiOsc import GuiOsc


class VarSlider(gtk.Frame):
    def __init__(self, gui, visual, var):
        gtk.Frame.__init__(self, var)
        self.gui = gui
        self.visual = visual
        self.var = var

        self.adjustment = gtk.Adjustment(
            lower = 0.0,
            upper = 100.0,
            step_incr = 1.0,
            page_incr = 5.0
        )
        self.adjustment.connect('value-changed', self.changed)

        scale = gtk.HScale(self.adjustment)
        scale.set_draw_value(False)
        scale.set_size_request(200,20)
        scale.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self.add(scale)
        self.show_all()

    def changed(self, adjustment):
        value = adjustment.get_value()/100
        self.gui.guiOsc.send(self.visual, self.var, value)

    def change(self, value):
        self.adjustment.set_value(value*100)


class VisualFrame(gtk.Frame):
    def __init__(self, gui, visual):
        gtk.Frame.__init__(self, visual)
        self.gui = gui
        self.visual = visual

        self.box = gtk.VBox()
        self.add(self.box)
        self.show_all()
        self.variables = {}

    def add_var(self, var):
        varSlider = VarSlider(self.gui, self.visual, var)
        self.variables[var] = varSlider
        self.box.add(varSlider)
        self.box.show_all()


def menu_item(k, v):
    item = gtk.MenuItem(k)

    if type(v) == dict:
        d = v
        menu = gtk.Menu()
        item.set_submenu(menu)
        for k,v in d.items():
            menu.append(menu_item(k,v))
    else:
        item.connect('activate', v)  # v is a callback

    return item


class Menu(gtk.MenuBar):
    def __init__(self, gui):
        gtk.MenuBar.__init__(self)
        self.gui = gui

        mdict = {
            'File': {
                'Visuals': {
                    'Folder': self.cb_visuals_folder,
                },
                'Exit': self.cb_exit,
            },
        }
        for k,v in mdict.items():
            self.append(menu_item(k,v))

    def cb_exit(self, item):
        print 'cb exit'

    def cb_visuals_folder(self, item):
        print 'cb visuals folder'


class Gui(Process):
    """Display a gui"""
    def __init__(self):
        Process.__init__(self)

        self.win = gtk.Window()
        self.win.set_title('Pineal Loop Project')
        self.win.resize(200,1)

        self.win.connect('delete-event', self.quit)

        vbox = gtk.VBox()
        self.win.add(vbox)

        vbox.add(Menu(self))

        self.box = gtk.HBox()
        vbox.add(self.box)

        self.win.show_all()

        self.visuals = {}

    def run(self):
        print 'starting pineal.gui'
        self.guiOsc = GuiOsc(self)
        self.guiOsc.start()

        try:
            while True:
                gtk.main_iteration()
                sleep(0.01)  # don't ask me why
        except KeyboardInterrupt:
            None

        self.guiOsc.stop()

    def stop(self):
        print 'stopping pineal.gui'

    def quit(self, widget, event):
        return True  # if True gui wan't close on user signal
        #return False

    def add(self, visual, var):
        with gtk.gdk.lock:
            if visual not in self.visuals.keys():
                self.visuals[visual] = VisualFrame(self, visual)
                self.box.add(self.visuals[visual])

            if var not in self.visuals[visual].variables.keys():
                self.visuals[visual].add_var(var)

            self.box.show_all()

    def remove(self, visual, var):
        None

    def change(self, visual, var, value):
        self.visuals[visual].variables[var].change(value)
