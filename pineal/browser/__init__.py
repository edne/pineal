from pineal.config import TITLE_BROWSER, HTTP
from multiprocessing import Process

try:
    from webkit import WebView
    import gtk
except ImportError:
    print 'missing webkit OR gtk: try to run with `--no-browser`'
    print 'You can open: `http://' + HTTP[0] + ':' + str(HTTP[1]) + '` in your \
browser'


class BrowserWidget(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)

        self.web = WebView()
        self.add(self.web)
        self.show_all()

    def run(self):
        print 'starting pineal.browser'
        self.web.open( 'http://' + HTTP[0] + ':' + str(HTTP[1]) )


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
