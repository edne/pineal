from pineal.config import TITLE

from multiprocessing import Process
from time import sleep
import math

from thirdparty.OSC import OSCClient, OSCMessage
import pyo


class Audio(Process):
    """Do the audio analysis"""
    def __init__(self, backend='portaudio'):
        Process.__init__(self)

        self.oscClient = OSCClient()
        self.oscClient.connect( ('localhost', 1420) )

        #backend = 'jack'
        self.s = pyo.Server(
            audio = backend,
            jackname = TITLE,
            nchnls = 2
        )
        if backend=='jack':
            self.s.setInputOffset(2)

        self._stop = False

    def run(self):
        print 'starting pineal.audio'
        self.s.boot()
        self.s.start()

        src = pyo.Input(chnl=[0,1])

        self._amp = pyo.Follower(src)
        self._bass = pyo.Follower(pyo.Biquad(src, 110, type=0))
        self._high = pyo.Follower(pyo.Biquad(src, 1000, type=1))

        self._pitch = pyo.Yin(src)
        self._note = 0.0

        try:
            while not self._stop:
                self.update()
                sleep(0.03)
        except KeyboardInterrupt:
            None

        self.s.stop()
        del self.s

    def stop(self):
        print 'stopping pineal.audio'
        self._stop = True

    def update(self):
        if self._pitch.get()>1:
            self._note = math.log(self._pitch.get()/16.35,2)%1.0

        self.oscClient.send( OSCMessage('/amp', float(self._amp.get())) )
        self.oscClient.send( OSCMessage('/bass', float(self._bass.get())) )
        self.oscClient.send( OSCMessage('/high', float(self._high.get())) )
        self.oscClient.send( OSCMessage('/note', float(self._note)) )
