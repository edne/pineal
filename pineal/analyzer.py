from config import TITLE, AUDIO_PORTS
import math, time, threading
import pyo


class Analyzer(threading.Thread):
    def __init__(self, visuals):
        self.visuals = visuals
        threading.Thread.__init__(self)

        self.s = pyo.Server(
            audio="jack",
            jackname=TITLE,
            nchnls = 4
        )
        self.s.boot()

        self._stop = False

    def run(self):
        self.s.start()

        src = pyo.Input(chnl=AUDIO_PORTS)

        self._amp = pyo.Follower(src)
        self._bass = pyo.Follower(pyo.Biquad(src, 110, type=0))
        self._high = pyo.Follower(pyo.Biquad(src, 1000, type=1))

        self._pitch = pyo.Yin(src)
        self._note = 0

        self._band = list()
        self._norm_band = [0]*9
        c = 4186.01*2
        for i in xrange(9):
            lowpassed = pyo.Follower(pyo.Biquad(src, c, type=0))
            highpassed = pyo.Follower(pyo.Biquad(lowpassed, c/2, type=1))
            band = pyo.Follower(highpassed)/(2**(i-1))
            self._band.append(band)
            c /= 2
        self._band.reverse()

        while not self._stop:
            self.update()
            time.sleep(0.1)

    def stop(self):
        self._stop = True
        self.s.stop()

    def update(self):
        for v in self.visuals.values():
            if self._pitch.get()>1:
                self._note = math.log(self._pitch.get()/16.35,2)%1.0

        for i in xrange(9):
            self._norm_band[i] = self._band[i].get()

        m = max(self._norm_band)
        if m>0:
            for i in xrange(9):
                self._norm_band[i] = self._amp.get()*self._band[i].get()/m

    def band(self, a, b=None):
        if b:
            return sum(self._norm_band[a:b])
        else:
            return self._norm_band[a]

    def amp(self):
        return self._amp.get()

    def bass(self):
        return self._bass.get()

    def high(self):
        return self._high.get()

    def note(self):
        return self._note
