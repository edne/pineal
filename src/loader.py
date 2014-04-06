from imports import *
from visuals import *

class Loader(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		
		self.parent = parent
		self.visuals = parent.visuals
		
		self.path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
		#print self.path
		self._stop = False
		#self.load()
		self.headertime = 0
		
	
	def run(self):
		while not self._stop:
			self.load()
			
			time.sleep(0.01)
	
	def load(self):
		names = list()
		for filename in glob(os.path.join(self.path,'*.py')):
			name = os.path.basename(os.path.splitext(filename)[0])
			if not ' ' in name:
				names.append(name)
		
		for v in self.visuals:
			if not v.name in names:
				self.visuals.remove(v)
		
		# in visuals: se esiste v con v.name non in names: rimuovi v
		
		for name in names:
			v = self.visuals.get(name)
			
			
			path = os.path.join(os.path.dirname(__file__),VISUALS_PATH)
			filename = os.path.join(path, name+'.py')
			
			header = os.path.join(
				os.path.dirname(__file__),'header.py'
			)
			
			if not v:
				v = Visual(self.parent, name)
				self.visuals.add(v)
				v.mtime = 0
				#self.visuals.names.append(v)
			
			mtime = os.path.getmtime(filename)
			headertime = os.path.getmtime(header)
			
			if mtime != v.mtime or headertime != self.headertime:
			#if True:
				#print "loading "+name
				v.mtime = mtime
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
				
				if not v.lock:
					v.load(code)
	
	def stop(self):
		self._stop = True
