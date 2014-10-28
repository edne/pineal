import gtk

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
        self.gui.guiOsc.send_change(self.visual, self.var, value)

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

    if callable(v):
        item.connect('activate', v)  # v is a callback
    else:
        d = v
        menu = gtk.Menu()
        item.set_submenu(menu)
        for k,v in d.items():
            menu.append(menu_item(k,v))

    return item


class Menu(gtk.MenuBar):
    def __init__(self, gui):
        gtk.MenuBar.__init__(self)
        self.gui = gui

        mdict = {
            'File': {
                #'Visuals': {
                #    'Folder': self.cb_visuals_folder,
                #},
                'Exit': self.cb_exit,
            },
        }
        for k,v in mdict.items():
            self.append(menu_item(k,v))

    def cb_exit(self, item):
        self.gui.guiOsc.send_cmd('exit')
        #self.gui.stop()


