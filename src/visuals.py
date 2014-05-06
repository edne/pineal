from imports import *

class Visuals(list):
	def __init__(self, parent):
		list.__init__(self)
	
	def add(self, v):
		self.append(v)
		#v.tex = self.tex
	
	def remove(self, v):
		list.remove(self, v)
		del v
	
	def get(self, name):
		for v in self:
			if name == v.name:
				return v
		return None
	
	def update(self):
		for v in self:
			v.update()
	

class Visual():
	def __init__(self, parent, name):
		
		self.parent = parent
		self.name = name
		
		self.old_code = ""
		self.new_code = ""
		self.header_lines = 0
		self.valid = True
		self.invalid = False
		self.lock = False
		
		self.box = Box()
		self.box._mem = dict()
		self.box.amp = 0
		self.box.bass = 0
		self.box.high = 0
		self.box.note = 0
		self.box.band = list()
		self.box.band += [0]*9
	
	def load(self, code):
		if self.lock:
			self.filetime = 0  # ask a reload
			return
		self.lock = True
		
		if code != self.new_code:			
			if code != self.old_code:
				self.new_code = code  # anche se e' sbagliato
			
			self.valid = True
			try:
				exec(code, self.box.__dict__)
			except Exception as e:
				print "load:"
				print self.error_log(e)
				self.lock = False
				self.load(self.old_code)
				self.valid = False
				self.invalid = True
		
		self.lock = False
			
	
	def update(self, size=None):
		while self.lock:
			None
		
		self.lock = True
		try:
			self.loop()
		except Exception as e:
			print "loop:"
			print self.error_log(e)
			
			self.lock = False
			self.load(self.old_code)
			self.loop()
			self.valid = False  # new_code e' ancora quello sbagliato
			self.invalid = True
			
		
		if self.valid:
			self.old_code = self.new_code
			if self.invalid:
				print "ok!                          "
				self.invalid = False
		
		self.lock = False
	
	def error_log(self, e):
		#return str(e)
		
		log = self.name + '.py\n'
		log = str(log)+str(e)
		
		if hasattr(e, 'lineno'):
			if e.lineno >= self.header_lines:
				lineno = e.lineno-self.header_lines
			else:
				lineno = e.lineno
				log = str(log)+'\nheader.py'
			log = str(log)+'\nat line: '+str(lineno)
		
		if hasattr(e, 'text'):
			log = str(log)+'\n'+e.text
		
		return log
	
	def loop(self):
		try:
			if type(self.box.time) == float:
				self.box.dt = time.time() - self.box.time
			else:
				self.box.dt = 0
		except:
			self.box.dt = 0
		self.box.time = time.time()
		
		glMatrixMode(GL_MODELVIEW)
		
		#self.box.textures = self.tex
		glPushMatrix()
		self.box.loop()
		glPopMatrix()
		
	
class Box:
	def loop(self):
		None
	
	
