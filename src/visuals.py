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
		
		self.tex = dict()
		path = os.path.join(os.path.dirname(__file__),IMAGES_PATH)
		for filename in glob(os.path.join(path,'*.png')):
			name = os.path.basename(os.path.splitext(filename)[0])
			if not ' ' in name:
				#print name
				self.tex[name] = self.load_tex(name)
		
		self.box = Box()
		self.box._mem = dict()
		self.box.amp = 0
		self.box.bass = 0
		self.box.high = 0
		self.box.note = 0
		self.box.band = list()
		self.box.band += [0]*9
	
	def load(self, code):
		if code == self.new_code:
			print "something is wrong"
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
		try:
			if type(self.box.time) == float:
				self.box.dt = time.time() - self.box.time
			else:
				self.box.dt = 0
		except:
			self.box.dt = 0
		self.box.time = time.time()
		#self.box.time_rad = self.box.time%(2*math.pi)

		
		self.box.textures = self.tex
		#glBindTexture(GL_TEXTURE_2D, self.tex['alquemix'])
		self.box.loop()
	
	def load_tex(self, filename):
		path = os.path.join(os.path.dirname(__file__),IMAGES_PATH)
		filename = os.path.join(path,filename+'.png')
		
		img = Image.open(filename)
		img_data = np.array(list(img.getdata()), np.uint8)

		texture = glGenTextures(1)
		glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		glBindTexture(GL_TEXTURE_2D, texture)

		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		# jpg
		#glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
		# png
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
		return texture
	
class Box:
	def loop(self):
		None
	
	
