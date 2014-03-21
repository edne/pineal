from imports import *

class Server(threading.Thread):
	def __init__(self, parent):
		threading.Thread.__init__(self)
		
		self.parent = parent
		
		address = (IP, PORT)
		self.s = OSC.OSCServer(address)
		
		for msg in GLOBAL_MSG:
			self.s.addMsgHandler('/'+msg, self.global_handler)
		
	
	def test_handler(self, addr, tags, data, source):
		print "---"
		print "received new osc msg from %s" % OSC.getUrlStr(source)
		print "with addr : %s" % addr
		print "typetags %s" % tags
		print "data %s" % data
		print "---"
	
	def global_handler(self, addr, tags, data, source):
		for v in self.parent.visuals:
			v.box.__dict__[addr[1:]] = data[0]
	
	def local_handler(self, addr, tags, data, source):
		(name,msg) = addr[1:].split('/')
		self.parent.visuals.get(name).box.__dict__[msg] = data[0]
	
	def register(self, v):
		for msg in LOCAL_MSG:
			self.s.addMsgHandler('/'+v.name+'/'+msg, self.local_handler)
			v.box.__dict__[msg] = 0.0
		
		for msg in GLOBAL_MSG:
			v.box.__dict__[msg] = 0.0
	
	def run(self):
		self.s.serve_forever()
	
	def stop(self):
		self.s.close()
		self.join()
