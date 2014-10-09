from multiprocessing import Process
from threading import Thread

from pineal.config import OSC_CORE, OSC_GUI, HTTP
from thirdparty.OSC import OSCClient, OSCMessage, OSCServer
import thirdparty.bottle as bottle

#from thirdparty.bottle_websocket import websocket, GeventWebSocketServer
#from gevent import monkey
#monkey.patch_all()


class Web(Process):
    """Run the webserver for the browser interface"""
    def __init__(self):
        Process.__init__(self)

        self.oscServer = OSCServer(OSC_GUI)
        self.oscServer.addMsgHandler('/add', self.add)
        self.oscServer.addMsgHandler('/remove', self.remove)
        self.oscServer.addMsgHandler('/change', self.change)

        self.oscClient = OSCClient()
        self.oscClient.connect(OSC_CORE)

        bottle.route('/')(self.root)
        bottle.route('/<filepath:path>')(self.server_static)
        bottle.route('/<visual>/<var>', method='POST')(self.post)
        bottle.route('/polling', method='POST')(self.polling)
        #bottle.get('/websocket', apply=[websocket])(self.websocket)

        self.msg = []
        self._stop = False

    def run(self):
        print 'starting pineal.web'
        bottleThread = Thread(
            target = bottle.run,
            kwargs = {
                'quiet': True,
                'host': HTTP[0],
                'port': HTTP[1],
                #'server': GeventWebSocketServer
                #'server': 'gevent'
            }
        )
        bottleThread.setDaemon(True)
        bottleThread.start()

        try:
            while not self._stop:
                self.oscServer.handle_request()
        except KeyboardInterrupt:
            None

    def stop(self):
        print 'stopping pineal.web'
        self._stop = True

    ## OSC handling
    def add(self, path, tags, args, source):
        self.msg.append(' '.join(['add']+args))

    def remove(self, path, tags, args, source):
        self.msg.append(' '.join(['remove']+args))

    def change(self, path, tags, args, source):
        self.msg.append(' '.join(['change']+[str(arg) for arg in args]) )
    ##

    ## HTTP routing
    def root(self):
        return bottle.static_file('index.html', root='webapp')

    def server_static(self, filepath):
        return bottle.static_file(filepath, root='webapp')

    def post(self, visual, var):
        value = bottle.request.forms.get('value')
        self.oscClient.send( OSCMessage('/'+visual+'/'+var, float(value)) )

    def polling(self):
        if self.msg:
            return self.msg.pop(0)
    ##

    def websocket(self, ws):
        while True:
            if self.msg:
                ws.send(self.msg.pop(0))
