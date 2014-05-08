from imports import *
import graphic

l = list()

def add(v):
	l.append(v)
	
def remove(v):
	l.remove(v)
	del v
	
def get(name=''):
	if name:
		for v in l:
			if name == v.name:
				return v
		return None
	else:
		return l

def update():
	for v in l:
		v.update()

def names():
	for v in l:
		yield v.name

class Visual():
	def __init__(self, name):
		self.name = name
		
		self.old_code = ""
		self.new_code = ""
		self.header_lines = 0
		self.valid = True
		self.invalid = False
		self.lock = False
		
		self.box = Box()
		self.var = dict()
		
	
	def load(self, code):
		if code != self.new_code:			
			if code != self.old_code:
				self.new_code = code  # anche se e' sbagliato
			
			self.valid = True
			try:
				exec(code, self.box.__dict__)
				
			except Exception as e:
				print "load:"
				print self.error_log(e)
				self.load(self.old_code)
				self.valid = False
				self.invalid = True
	
	def remove(self):
		remove(self)
	
	def update(self, size=None):
		self.lock = True
		try:
			self.loop()
		except Exception as e:
			print "loop:"
			print self.error_log(e)
			
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
		
		
		if hasattr(self.box, 'var') and isinstance(self.box.var, dict):
			for k in self.box.var.keys():
				if not k in self.var.keys():
					self.var[k] = self.box.var[k]
			
			for k in self.var.keys():
				if not k in self.box.var.keys():
					del self.var[k]
			
			self.box.__dict__.update(self.var)
		
		graphic.draw(self.box.loop)
		
	
class Box:
	def __init__(self):
		self.amp = 0
		self.bass = 0
		self.high = 0
		self.note = 0
		self.band = list()
		self.band += [0]*9
	def loop(self):
		None
	
	
