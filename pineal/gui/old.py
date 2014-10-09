from pineal.config import TITLE_OVERVIEW, TITLE
from pineal.browser import BrowserWidget
from multiprocessing import Process
import subprocess as sp
import gtk


def win_id(title):
    cmd = 'xwininfo -name %s -int' % title
    out = sp.Popen(cmd.split(), stdout=sp.PIPE).communicate()[0].split('\n')

    if 'error' in out[0]:
        return 0

    row = [r for r in out if 'id:' in r][0].split()
    wid = long([row[i+1] for i,w in enumerate(row) if w=='id:'][0])
    return wid


class Overview(gtk.Socket):
    def __init__(self):
        gtk.Socket.__init__(self)
        self.show()

    def run(self):
        wid = win_id(TITLE_OVERVIEW)
        if wid:
            self.add_id(win_id(TITLE_OVERVIEW))
            self.set_usize(600,450)
            self.show()


class Editor(gtk.Socket):
    def __init__(self):
        gtk.Socket.__init__(self)
        #self.show()

    def run(self):
        xid = self.get_id()
        sp.Popen(['gvim', '--socketid', str(xid)])
        #sp.Popen(['emacs', '--parent-id', str(xid)])


class Gui(Process):
    """Display in a window the overview, a text editor and the browser"""
    def __init__(self):
        Process.__init__(self)

        self.win = gtk.Window()
        self.win.set_title(TITLE)
        self.win.resize(300,150)
        #self.win.connect("destroy", lambda w: gtk.main_quit())
        self.win.connect('delete-event', self.quit, None)

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        self.overview = Overview()
        hbox.pack_end(self.overview, False, False)
        vbox.pack_start(hbox, False, False)

        self.browser = BrowserWidget()
        vbox.add(self.browser)

        hpaned = gtk.HPaned()
        self.editor = Editor()
        hpaned.pack1(self.editor, True,True)

        hpaned.pack2(vbox, False,False)

        self.win.add(hpaned)

        self.win.show_all()

    def run(self):
        self.browser.run()
        self.overview.run()
        self.editor.run()

        self.win.set_focus_child(self.browser)

        try:
            gtk.main()
        except KeyboardInterrupt:
            None

    def stop(self):
        print 'stopping pineal.browser'

    def quit(self, widget, event, data):
        dialog = gtk.MessageDialog(
            self.win, gtk.DIALOG_MODAL,
            gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,
            "Are you sure?"
        )
        dialog.set_title("Quitting")

        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_YES:
            gtk.main_quit()
            return False
        else:
            return True
