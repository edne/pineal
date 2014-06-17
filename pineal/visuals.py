from imports import *
import graphic

def init():
	global l
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

def names():
	for v in get():
		yield v.name

class Visual():
	def __init__(self, name):
		self.name = name

		self.lock = False  # to be removed
		self.stack = list()
		self.code = None

		self.box = Box()

	def load(self, code):
		self.stack.append(code)

		if not self.code:
			self.code = code

	def remove(self):
		remove(self)

	def update(self):
		if not self.code: return
		if len(self.stack)==0: return

		if self.code != self.stack[-1]:
			self.code = self.stack[-1]

		try:
			#exec("from pineal.drawing import *", self.box.__dict__)
			exec(self.code, self.box.__dict__)
			self.loop()
		except Exception as e:
			print self.error_log(e)

			self.stack.remove(self.code)
			if len(self.stack)==0:
				print "%s.py is BROKEN" % self.name
			else:
				self.code = self.stack[-1]
				self.update() # WARNING recursion!


	def error_log(self, e):
		log = self.name + '.py'
		#log += ' at line: '+str(lineno)+"\n"
		log += str(e)

		if hasattr(e, 'text'):
			log += "\n"+e.text

		return log

	def loop(self):
		self.box.time = time.time()
		if self.box.last_time:
			self.box.dt = self.box.last_time - self.box.time
		self.box.last_time = self.box.time

		for k in self.box.var.keys():
			if not k in self.box.__dict__.keys():
				self.box.__dict__[k] = self.box.var[k]

		self.box.loop()


class Box:
	def __init__(self):
		self.amp = 0
		self.bass = 0
		self.high = 0
		self.note = 0

		self.time = 0
		self.last_time = 0
		self.dt = 0

		self.PRE = False

		self.var = dict()
	def loop(self):
		None

def reciver(name, key, value):
	for v in get():
		if name=="*" or name==v.name:
			v.box.__dict__[key] = value  # this is NOT safe (if used with OSC)
