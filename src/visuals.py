from imports import *

class Visuals(list):
	def __init__(self, parent):
		list.__init__(self)
	
	def add(self, v):
		self.append(v)
	
	def remove(self, v):
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
	def __init__(self, parent, name, size=RESOLUTION):
		
		self.parent = parent
		self.name = name
		
		self.w = size[0]
		self.h = size[1]
		
		self.old_code = ""
		self.new_code = ""
		self.header_lines = 0
		self.valid = True
		self.invalid = False
		self.lock = False
		
		self.box = Box()
		
		self.parent.server.register(self)
	
	def load(self, code):
		if code == self.new_code:  # se modifico librerie non ricarica
			return
		
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
		
		
		#del surface
		self.lock = False
	
	def error_log(self, e):
		#return str(e)
		
		log = self.name + '.py\n'
		log += str(e)
		
		if hasattr(e, 'lineno'):
			if e.lineno >= self.header_lines:
				lineno = e.lineno-self.header_lines
			else:
				lineno = e.lineno
				log += '\nheader.py'
			log +='\nat line: '+str(lineno)
		
		if hasattr(e, 'text'):
			log +='\n'+e.text
		
		return log
	
	def loop(self):
		self.box.time = time.time()
		self.box.loop()
		
	
class Box:
	def loop(self):
		None
	
	
