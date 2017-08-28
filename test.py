from math import pi, sin, cos

#import direct.directbase.DirectStart

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
 
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

	SCALE = 2
	POS = (0, 0, 0)
	HPR = (0, 0, 0)
	RATE = 1

	def __init__(self, path):
		#======LOAD MODEL=========================
		self.map = loader.loadModel(path)
		
		#======SCALE POSITION ROTATE SET==========
		self.map.setScale(self.SCALE, self.SCALE, self.SCALE)
		self.map.setPos(self.POS)
		self.map.setHpr(self.HPR)

		#======RENDER ON==========================
		self.map.reparentTo(render)


class Window(ShowBase):

	def __init__(self, arenapath, charpath):

		ShowBase.__init__(self)

		self.env = Environment(arenapath)

		self.char01 = Character(charpath)

		self.plight = PointLight('pl1')
		self.plight.setColor(VBase4(1, 1, 1, 1))
		self.lamp = render.attachNewNode(self.plight)
		self.lamp.setPos(0, 0, 10)
		render.setLight(self.lamp)

		self.accept('w', self.char01.walk)
		self.accept('w-repeat', self.char01.loopwalk)
		self.accept('w-up', self.char01.stopwalk)


location = r'models/arenas/arena3/arena3.egg'
char = r'models/human/'

app = Window(location, char)
app.run()