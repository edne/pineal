from pineal.config import TITLE, BACKEND

from multiprocessing import Process
from time import sleep
import math
from sys import exit

from pineal.config import OSC_CORE
from thirdparty.OSC import OSCClient, OSCMessage
import pyo


class Audio(Process):
    """Do the audio analysis"""
    def __init__(self):
        Process.__init__(self)

        self.oscClient = OSCClient()
        self.oscClient.connect(OSC_CORE)

        self.s = pyo.Server(
            audio = BACKEND,
            jackname = TITLE,
            nchnls = 2
        )
        if BACKEND=='jack':
            self.s.setInputOffset(2)

        self._stop = False

    def run(self):
        print 'starting pineal.audio'
        #self.s.gui()
        self.s.boot()
        self.s.start()

        try:
            src = pyo.Input(chnl=[0,1])
            print 'Pyo is working properly!\n'
        except pyo.PyoServerStateException:
            print(
                'Pyo is not working, '
                'stop antying is using Pulseaudio, or simply use Jack'
            )
            exit(1)

        self._amp = pyo.Follower(src)
        self._bass = pyo.Follower(pyo.Biquad(src, 110, type=0))
        self._high = pyo.Follower(pyo.Biquad(src, 1000, type=1))

        self._band = []
        do = 16.3516
        for i in xrange(12):
            f1 = pyo.Follower(pyo.Biquad(src, do*2**i, type=0))
            f2 = pyo.Follower(pyo.Biquad(f1, do*2**(i+1), type=1))
            band = f2 * (do*2**(i+3))
            self._band.append(band)

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

        self.oscClient.send( OSCMessage('/audio/amp', float(self._amp.get())) )
        self.oscClient.send( OSCMessage('/audio/bass', float(self._bass.get())) )
        self.oscClient.send( OSCMessage('/audio/high', float(self._high.get())) )
        self.oscClient.send( OSCMessage(
            '/audio/band', [float(b.get()) for b in self._band]
        ))
        self.oscClient.send( OSCMessage('/audio/note', float(self._note)) )
