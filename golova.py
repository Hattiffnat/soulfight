from math import pi, sin, cos

from panda3d.core import loadPrcFile, loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
 
class Character(ShowBase):

	SCALE = 0.07
	POS = (5, 0, 0.4)
	HPR = (-90, 0, 0)

	def __init__(self, path):

		self.char = Actor(path+'male.egg', {
			'walk_loop' : path+'male-walk_loop.egg',
			'walk_start' : path+'male-walk_start.egg'
			})
		self.char.setScale(self.SCALE, self.SCALE, self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		self.start = self.char.getAnimControl('walk_start')
		self.loop = self.char.getAnimControl('walk_loop')

		self.char.reparentTo(render)

	def walk(self):
		if self.start.isPlaying() or self.loop.isPlaying():
			self.loop.play()
		else:
			self.start.play()

	def stopwalk(self):
		if self.start.isPlaying():
			self.start.stop()
		if self.loop.isPlaying():
			self.loop.stop()

			

class Window(ShowBase):

	def __init__(self, arenapath, charpath):
		ShowBase.__init__(self)
		self.loadEnv(arenapath)
		self.char01 = Character(charpath)

		self.accept('w-repeat', self.char01.walk)
		self.accept('w-up', self.char01.stopwalk)

	def loadEnv(self, arenapath):
		self.scene = loader.loadModel(arenapath)
		self.scene.reparentTo(render)


location = r'models/arenas/arena2.egg'
char = r'models/human/'

app = Window(location, char)
app.run()