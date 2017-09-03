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
	RATE = 1.5

	def __init__(self, path):

		#======ANIMATION LIST=====================
		self.char = Actor(path+'male.egg', {
			'walk_loop' : path+'male-walk_loop.egg',
			'walk_start' : path+'male-walk_start.egg'
			})

		#======SCALE POSITION ROTATE APPLY========
		self.char.setScale(self.SCALE, self.SCALE, self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		#======INPUT ANIMATIONS VARIABLES=========
		self.start = self.char.getAnimControl('walk_start')
		self.loop = self.char.getAnimControl('walk_loop')

		#======ANIMATION PLAY RATE SET============
		self.start.setPlayRate(self.RATE)
		self.loop.setPlayRate(self.RATE)

		#======RENDER APPLY=======================
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

class Window(ShowBase):

	def __init__(self, arenapath, charpath):
		ShowBase.__init__(self)
		self.loadEnv(arenapath)
		self.char01 = Character(charpath)

		self.accept('w', self.char01.walk)
		self.accept('w-repeat', self.char01.loopwalk)
		self.accept('w-up', self.char01.stopwalk)

	def loadEnv(self, arenapath):
		self.scene = loader.loadModel(arenapath)
		self.scene.reparentTo(render)


location = r'models/arenas/arena2.egg'
char = r'models/human/'

app = Window(location, char)
app.run()