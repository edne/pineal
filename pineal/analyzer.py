from imports import *
from pyo import *

class Analyzer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
		self.s = Server(
			audio="jack",
			jackname=TITLE,
			nchnls = 4
		).boot()
		
		self.update()
		
		self._stop = False
	
	def run(self):
		self.s.start()
		
		src = Input(chnl=AUDIO_PORTS)
		
		self.amp = Follower(src)
		self.bass = Follower(Biquad(src, 110, type=0))
		self.high = Follower(Biquad(src, 1000, type=1))
		
		self.pitch = Yin(src)
		
		self.band = list()
		c = 4186.01*2
		for i in xrange(9):
			lowpassed = Follower(Biquad(src, c, type=0))
			highpassed = Follower(Biquad(lowpassed, c/2, type=1))
			band = Follower(highpassed)/(2**(i-1))
			self.band.append(band)
			c /= 2
		self.band.reverse()
		
		#p = Pattern(self.update, 1.0/30)
		#p.play()
		
		while not self._stop:
			self.update()
			time.sleep(0.1)
		
	def stop(self):
		self._stop = True
		self.s.stop()
	
	def update(self):
		for v in visuals.get():
			v.box.amp = self.amp.get()
			v.box.bass = self.bass.get()
			v.box.high = self.high.get()
			
			if self.pitch.get()>1:
				v.box.note = math.log(self.pitch.get()/16.35,2)%1.0
			
			
			for i in xrange(9):
				v.box.band[i] = self.band[i].get()
			
			m = max(v.box.band)
			if m>0:
				for i in xrange(9):
					v.box.band[i] = v.box.amp*self.band[i].get()/m


thread = Analyzer()  # better use the server outside?


def start():
	thread.start()

def stop():
	thread.stop()

def update():
	thread.update()