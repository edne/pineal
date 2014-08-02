from multiprocessing import Process
from threading import Thread
import thirdparty.bottle as bottle
from thirdparty.OSC import OSCClient, OSCMessage, OSCServer


class Web(Process):
    def __init__(self):
        Process.__init__(self)

        self.server = OSCServer( ('localhost', 1421) )
        self.server.addMsgHandler('/add', self.add)
        self.server.addMsgHandler('/remove', self.remove)

        self.client = OSCClient()
        self.client.connect( ('localhost', 1420) )

        bottle.route('/')(self.root)
        bottle.route('/<filepath:path>')(self.server_static)
        bottle.route('/<visual>/<var>', method='POST')(self.post)

        self._stop = False

    def run(self):
        print 'starting pineal.web'
        bottleThread = Thread(
            target = bottle.run,
            kwargs = { 'host': 'localhost', 'port': 42080 }
        )
        bottleThread.setDaemon(True)
        bottleThread.start()

        try:
            while not self._stop:
                self.server.handle_request()
        except KeyboardInterrupt:
            None

    def stop(self):
        print 'stopping pineal.web'
        self._stop = True

    def add(self, path, tags, args, source):
        print 'add'

    def remove(self, path, tags, args, source):
        print 'remove'

    ## HTTP routing
    def root(self):
        return bottle.static_file('index.html', root='webapp')

    def server_static(self, filepath):
        return bottle.static_file(filepath, root='webapp')

    def post(self, visual, var):
        value = bottle.request.forms.get('value')
        print 'posted'
        print value
        self.client.send( OSCMessage('/'+visual+'/'+var, float(value)) )
    ##
