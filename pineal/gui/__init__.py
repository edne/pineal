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


class Overview(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.show()

    def run(self):
        socket = gtk.Socket()
        self.add(socket)
        wid = win_id(TITLE_OVERVIEW)
        if wid:
            socket.add_id(win_id(TITLE_OVERVIEW))
            socket.set_usize(600,450)
            socket.show()


class Gui(Process):
    def __init__(self):
        Process.__init__(self)

        self.win = gtk.Window()
        self.win.set_title(TITLE_BROWSER)
        self.win.resize(300,150)
        self.win.connect("destroy", lambda w: gtk.main_quit())

        self.vbox = gtk.VBox()

        self.browser = Browser()
        self.vbox.add(self.browser)

        self.overview = Overview()
        self.vbox.add(self.overview)

        self.win.add(self.vbox)
        self.win.show_all()

    def run(self):
        self.browser.run()
        self.overview.run()

        try:
            gtk.main()
        except KeyboardInterrupt:
            None

    def stop(self):
        print 'stopping pineal.browser'
