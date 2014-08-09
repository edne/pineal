from pineal.config import TITLE_OVERVIEW, TITLE_BROWSER
from multiprocessing import Process
import subprocess as sp
from webkit import WebView
import gtk


def win_id(title):
    cmd = 'xwininfo -name %s -int' % title
    out = sp.Popen(cmd.split(), stdout=sp.PIPE).communicate()[0].split('\n')

    if 'error' in out[0]:
        return 0

    row = [r for r in out if 'id:' in r][0].split()
    wid = long([row[i+1] for i,w in enumerate(row) if w=='id:'][0])
    return wid


class Browser(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)

        self.web = WebView()
        self.add(self.web)
        self.show_all()

    def run(self):
        print 'starting pineal.browser'
        self.web.open('http://127.0.0.1:42080')


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
    def __init__(self):
        Process.__init__(self)

        self.win = gtk.Window()
        self.win.set_title(TITLE_BROWSER)
        self.win.resize(300,150)
        self.win.connect("destroy", lambda w: gtk.main_quit())

        vbox = gtk.VBox()
        hbox = gtk.HBox()

        self.overview = Overview()
        hbox.pack_end(self.overview, False, False)
        vbox.pack_start(hbox, False, False)

        self.browser = Browser()
        vbox.add(self.browser)

        hpaned = gtk.HPaned()
        self.editor = Editor()
        hpaned.add(self.editor)

        hpaned.add(vbox)

        self.win.add(hpaned)

        self.win.show_all()

    def run(self):
        self.browser.run()
        self.overview.run()
        self.editor.run()

        try:
            gtk.main()
        except KeyboardInterrupt:
            None

    def stop(self):
        print 'stopping pineal.browser'
