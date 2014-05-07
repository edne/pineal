from imports import *

class Loader(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
		self.path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
		#print self.path
		self._stop = False
		#self.load()
		self.headertime = 0
		
	
	def run(self):
		while not self._stop:
			self.load()
			
			#time.sleep(0.01)
	
	def load(self):
		names = list()
		for filename in glob(os.path.join(self.path,'*.py')):
			name = os.path.basename(os.path.splitext(filename)[0])
			if not ' ' in name:
				names.append(name)
		
		for v in visuals.get():
			if not v.name in names:
				v.remove()
		
		
		for name in names:
			v = visuals.get(name)
			
			
			path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
			filename = os.path.join(path, name+'.py')
			
			header = os.path.join(
				os.path.dirname(__file__),'header.py'
			)
			
			if not v:
				v = visuals.Visual(name)
				visuals.add(v)
				v.filetime = 0
			
			try:
				filetime = getmtime(filename)
				headertime = getmtime(header)
			except OSError:
				continue
			
			if (
				filetime != v.filetime or
				headertime != self.headertime
				):
			#if True:
				print "loading            "+name+".py"
				v.filetime = filetime
				self.headertime = headertime
				try:
					
					f = open(header, "r")
					code = f.read()
					f.close()
					
					f = open(header)
					v.header_lines = sum(1 for line in f)
					f.close()
					
					f = open(filename, "r")
					code += f.read()
					f.close()
				except IOError as e:
					print e
					return
				
				v.load(code)
	
	def stop(self):
		self._stop = True

thread = Loader()

def start():
	thread.start()

def stop():
	thread.stop()
