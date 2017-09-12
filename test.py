import json
import random
import sys
import os
import math

#import direct.directbase.DirectStart

from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.ActorInterval import *
from direct.interval.IntervalGlobal import *

#from direct.interval.IntervalGlobal import Sequence

class Character(ShowBase):

	SCALE = 1
	POS = (0, 0, 0.4)
	HPR = (-90, 0, 0)
	RATE = 1.5

	def __init__(self, path):

		self.keyRead = True
		self.speed = 0
		self.vector = list(self.HPR)
		#======ANIMATION LIST=====================
		self.char = Actor(path+'male.egg', {
			'walkcy_back'	: path+'male-start_walk_stop_backward_l.egg',
			'walkcy_forw'	: path+'male-start_walk_stop_forward_l.egg',
			'step_back'		: path+'male-step_back_r.egg',
			'fists'			: path+'male-wrists_fist.egg',
			'hold_arms'		: path+'male-wrists_hold_arms.egg'})

		#print(Actor.listJoints(self.char))
				
		#======SCALE POSITION ROTATE SET==========
		self.char.setScale(self.SCALE)
		self.char.setPos(self.POS)
		self.char.setHpr(self.HPR)

		#======MAKING INTERVALS===================
		self.startI = self.char.actorInterval(
			'walkcy_forw',
			loop=0,
			constrainedLoop=0,
			startFrame=0,
			endFrame=10,
			playRate=1,
			)
		self.fistI = self.char.actorInterval(
			'fists',
			loop=0,
			constrainedLoop=0,
			startFrame=0,
			endFrame=4,
			playRate=1)

		#======SET CAMERA POS=====================		

		#======RENDER ON==========================

		self.char.reparentTo(render)

		taskMgr.add(self.moveTask, 'MoveTask')
		taskMgr.add(self.spinCameraTask, "SpinCameraTask")

		if self.keyRead:
			self.accept('f', self.fisttest)
			self.accept('a', self.key_a)
			self.accept('d', self.key_d)
			self.accept('w', self.key_w)
			self.accept('s', self.key_s)

	def moveTask(self, task):
		hpr_speed = 5
		charHpr = newHpr = list(self.char.getHpr())

		if charHpr[0] > self.vector[0]:
			newHpr[0] = charHpr[0] - hpr_speed

		elif charHpr[0] < self.vector[0]:
			newHpr[0] = charHpr[0] + hpr_speed

		self.char.setHpr(tuple(newHpr))

		return task.cont

	# Define a procedure to move the camera.
	def spinCameraTask(self, task):
		angleDegrees = task.time * 6.0
		angleRadians = angleDegrees * (math.pi / 180.0)
		camera.setPos(20 * math.sin(angleRadians), -20.0 * math.cos(angleRadians), 3)
		camera.setHpr(angleDegrees, 0, 0)
		return Task.cont
		
	def key_a(self):
		self.vector[0] = 90

	def key_d(self):
		self.vector[0] = -90

	def key_w(self):
		self.vector[0] = 0

	def key_s(self):
		self.vector[0] = 180

	def swapKeyRead(self):
		if self.keyRead:
			self.keyRead = False
			taskMgr.remove('MoveTask')
		else:
			self.keyRead = True
			taskMgr.add(self.moveTask, 'MoveTask')

	def fisttest(self):
		self.fistI.start()

	def swap_left(self):
		print('swap left')

	def swap_right(self):
		print('swap right')
		
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

		self.accept('q', self.char01.swapKeyRead)


	

arenapath = r'models/arenas/arena3/'
charpath = r'models/human/'

app = Window(arenapath, charpath)
app.run()