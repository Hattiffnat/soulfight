from math import pi, sin, cos
import json

#import direct.directbase.DirectStart

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
#from direct.interval.IntervalGlobal import Sequence

class Character(ShowBase):

	SCALE = 1
	POS = (0, 0, 0.4)
	HPR = (-90, 0, 0)
	RATE = 1.5

	def __init__(self, path):

		#======ANIMATION LIST=====================
		self.char = Actor(path+'male.egg', {
			'walk_loop' : path+'male-walk_loop.egg',
			'walk_start' : path+'male-walk_start.egg'
			})

		#======SCALE POSITION ROTATE SET==========
		self.char.setScale(self.SCALE, self.SCALE, self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		#======INPUT ANIMATIONS VARIABLES=========
		self.start = self.char.getAnimControl('walk_start')
		self.loop = self.char.getAnimControl('walk_loop')

		#======ANIMATION PLAY RATE SET============
		self.start.setPlayRate(self.RATE)
		self.loop.setPlayRate(self.RATE)

		#======RENDER ON==========================
		self.char.reparentTo(render)

	def walk(self):
		if self.start.getPlayRate() < 0:
			self.start.setPlayRate(self.RATE)
		self.start.play()

	def loopwalk(self):
		if not(self.start.isPlaying() or self.loop.isPlaying()):
			self.loop.play()

	def stopwalk(self):
		self.start.setPlayRate(self.RATE * (-1))
		self.start.play()
		
class Environment(ShowBase):

	def __init__(self, path):
		
		self.loadmodel(path)

		self.lights = []
		self.loadlights(path)

		print("Envirement loaded")

	def loadmodel(sefl, path):

		solid = loader.loadModel(path + 'solid.egg')

		with open(path + 'data.txt', 'r') as datafile:
			data = json.loads(datafile.read())

		scale = data[0]
		pos = data[1]
		hpr = data[2]	

		solid.setScale(tuple(scale))
		solid.setPos(tuple(pos))
		solid.setHpr(tuple(hpr))

		solid.reparentTo(render)

	def loadlights(self, path):

		lights_params = []
		with open(path + 'lights.txt', 'r') as lights_file:
			for line in lights_file:
				if line[0] == '#': continue
				lights_params.append(tuple(json.loads(line)))

		for light_param in lights_params:

			if   light_param[0] == 'pl':		
				 self.typelight = PointLight('pl')
				 self.lamp = render.attachNewNode(self.typelight)
				 self.lamp.setPos(tuple(light_param[2]))
				 print('point light loaded: '+str(light_param))

			elif light_param[0] == 'dl':
				 self.typelight = DirectionalLight('dl')
				 self.lamp = render.attachNewNode(self.typelight)
				 self.lamp.setHpr(tuple(light_param[2]))
				 print('directional light loaded: '+str(light_param))

			self.lights.append(self.typelight)

			self.typelight.setColor(VBase4(tuple(light_param[1])))
			render.setLight(self.lamp)

class Window(ShowBase):

	def __init__(self, arenapath, charpath):

		ShowBase.__init__(self)

		self.env = Environment(arenapath)

		self.char01 = Character(charpath)

		self.accept('w', self.char01.walk)
		self.accept('w-repeat', self.char01.loopwalk)
		self.accept('w-up', self.char01.stopwalk)

arenapath = r'models/arenas/arena3/'
charpath = r'models/human/'

app = Window(arenapath, charpath)
app.run()