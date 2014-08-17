from pineal.config import TITLE_BROWSER
from webkit import WebView
from multiprocessing import Process
import gtk


class BrowserWidget(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)

        self.web = WebView()
        self.add(self.web)
        self.show_all()

    def run(self):
        print 'starting pineal.browser'
        self.web.open('http://127.0.0.1:42080')


class Browser(Process):
    """Display a browser window for the web interface"""
    def __init__(self):
        Process.__init__(self)

        self.win = gtk.Window()
        self.win.set_title(TITLE_BROWSER)
        self.win.resize(300,200)
        self.win.connect('delete-event', self.quit, None)

        self.browser = BrowserWidget()
        self.win.add(self.browser)

        self.win.show_all()

    def run(self):
        self.browser.run()

        try:
            gtk.main()
        except KeyboardInterrupt:
            None

    def stop(self):
        print 'stopping pineal.browser'

    def quit(self, widget, event, data):
        return True
