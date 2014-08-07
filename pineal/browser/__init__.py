from multiprocessing import Process
from webkit import WebView
import gtk


class Browser(Process):
    def __init__(self):
        Process.__init__(self)

        self.win = gtk.Window()
        self.win.resize(300,150)
        #self.win.connect('destroy', gtk.main_quit)

        scroller = gtk.ScrolledWindow()
        self.win.add(scroller)

        self.web = WebView()
        scroller.add(self.web)
        self.win.show_all()

    def run(self):
        print 'starting pineal.browser'
        self.web.open('http://127.0.0.1:42080')
        try:
            gtk.main()
        except KeyboardInterrupt:
            None

    def stop(self):
        print 'stopping pineal.browser'
